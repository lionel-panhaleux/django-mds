import datetime
import io
import zipfile
import openpyxl.cell.cell
import openpyxl.styles.numbers
import xlsx_streaming
from xlsx_streaming.xlsx_template import DEFAULT_TEMPLATE
import zipstream
from bluetils.algorithms import grouper
from bluetils.formatters import excel
from django import http
from django.utils import timezone


def to_streaming_response(
    title,
    export_columns,
    serializer,
    queryset,
    template,
    tz_object,
    with_time=False,
    batch_size=500,
):
    """
    title: str, the base of the filename (appended with date (and time if with_time))
    export_columns: list of tuples (field_of_serializer, excel_header, function_to_transform_value | None)
    serializer: an ES serializer
    queryset: elastic queryset generator, queryset.scan() for example
    template: excel_template
    tz_object: a datetime.tzinfo object for formatting dates
    with_time: bool, append the time to the filename.
    """

    xlsx_streaming.set_export_timezone(tz_object)
    stream = stream_queryset_as_xlsx(
        export_columns, serializer, queryset, tz_object, template, batch_size=batch_size
    )

    openxml_mimetype = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response = http.StreamingHttpResponse(stream, content_type=openxml_mimetype)
    excel._format_response(response, title, with_time)
    return response


def stream_queryset_as_xlsx(
    export_columns,
    serializer,
    qs,
    tz_object,
    xlsx_template=None,
    batch_size=500,
    encoding="utf-8",
):
    batches = serialize_queryset_by_batch(
        export_columns, serializer, qs, tz_object, batch_size=batch_size
    )
    try:
        zip_template = zipfile.ZipFile(xlsx_template, mode="r")
    except (ValueError, AttributeError):
        zip_template = zipfile.ZipFile(DEFAULT_TEMPLATE, mode="r")

    sheet_name = xlsx_streaming.streaming.get_first_sheet_name(zip_template)
    if sheet_name is None:
        zip_template = zipfile.ZipFile(DEFAULT_TEMPLATE, mode="r")
        sheet_name = xlsx_streaming.streaming.get_first_sheet_name(zip_template)

    xlsx_sheet_string = zip_template.read(sheet_name).decode(encoding)

    zipped_stream = xlsx_streaming.streaming.zip_to_zipstream(
        zip_template, exclude=[sheet_name]
    )
    # Write the generated worksheet to the stream
    worksheet_stream = xlsx_streaming.render.render_worksheet(
        batches, xlsx_sheet_string, encoding
    )
    zipped_stream.write_iter(
        arcname=sheet_name,
        iterable=worksheet_stream,
        compress_type=zipstream.ZIP_DEFLATED,
    )
    return zipped_stream


def serialize_queryset_by_batch(export_columns, serializer, qs, tz_object, batch_size):
    for batch in grouper(qs, batch_size):
        results = serializer(batch, many=True).data
        rows = []
        for result in results:
            row = []
            for field, _header, transform in export_columns:
                value = result.get(field)
                if value and transform:
                    value = transform(value)
                    if isinstance(value, datetime.datetime):
                        # Elastic stores UTC datetimes with offset, so it's aware,
                        # but Excel seems to apply the UTC offset on aware datetimes
                        value = timezone.make_naive(value, tz_object)
                row.append(value)
            rows.append(row)
        yield rows


def excel_template(headers):
    """
    The generated sheet contains a header and one fake row generated from the fields of ``model``.
    The fake row contains values of types equivalent to the type of the model fields.
    """
    example_row = headers
    rows = [example_row]
    workbook = excel.excel(headers=headers, rows=rows, return_openpyxl_object=True)

    return io.BytesIO(openpyxl.writer.excel.save_virtual_workbook(workbook))

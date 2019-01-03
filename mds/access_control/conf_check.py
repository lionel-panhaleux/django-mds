from django.conf import settings


def conf_check_middleware(get_response):

    if not settings.AUTH_MEANS:
        raise Exception(
            "JWT authentication configuration is incomplete: "
            + "neither secret nor public key found"
        )

    def middleware(request):
        return get_response(request)

    return middleware

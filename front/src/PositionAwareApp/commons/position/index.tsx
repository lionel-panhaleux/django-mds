import { LatLngLiteral } from "leaflet";

const ZOOM_LEVEL_REGEX = /([0-9.]+)z/;

export interface IPosition {
  latlng: LatLngLiteral;
  zoom?: number;
}

export type PositionChanger = (position: IPosition) => void;

/**
 *
 * @param urlMatch coordinates as passed in the url "@48.8998564,2.4130346,15z"
 *
 * @returns null if unable to parse coordinates, or the coordinates object
 */
export function parsePosition(urlMatch: string): IPosition | null {
  if (!urlMatch) {
    return null;
  }

  const split = urlMatch.split(",");
  if (split.length < 2) {
    return null;
  }

  try {
    const latlng = {
      lat: Number.parseFloat(split[0]),
      lng: Number.parseFloat(split[1])
    };

    if (split.length >= 3 && split[2]) {
      const zoomMatch = split[2].match(ZOOM_LEVEL_REGEX);
      if (zoomMatch && zoomMatch[1]) {
        const zoom = Number.parseFloat(zoomMatch[1]);
        return { latlng, zoom };
      }
    }

    return { latlng };
  } catch (e) {
    return null;
  }
}

export function stringifyPosition(position: IPosition | null): string {
  if (!position) {
    return "";
  }

  const { latlng, zoom } = position;
  let str = `${latlng.lat},${latlng.lng}`;
  if (zoom) {
    str += `,${zoom}z`;
  }
  return str;
}

export function suffixPosition(
  newPath: string,
  oldLocation: { pathname: string }
) {
  const positionIndex = location.pathname.lastIndexOf("/@");
  if (positionIndex !== -1) {
    return newPath + location.pathname.substring(positionIndex);
  }
  return newPath;
}

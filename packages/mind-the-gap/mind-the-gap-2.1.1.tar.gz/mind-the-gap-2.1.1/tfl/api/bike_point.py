from typing import List

from tfl.api import get_tfl_json
from tfl.api.factory import from_json
from tfl.api.presentation.entities.place import Place
from tfl.api.presentation.entities.places_response import PlacesResponse

ENDPOINT = "BikePoint"


def all() -> List[Place]:

    json = get_tfl_json(ENDPOINT)
    return from_json(json)


def by_radius(lat: float, lon: float, radius: int) -> PlacesResponse:
    """
    Get all the bike status around a given coordinate
    :param lat:
    :param lon:
    :param radius: in meters
    :return:
    """
    params = {"lat": lat, "lon": lon, "radius": radius}
    json = get_tfl_json(ENDPOINT, params=params)
    return from_json(json)


def by_bounds(sw_lat: float, sw_lon: float, ne_lat: float, ne_lon: float) -> List[Place]:
    """
    Get all the bike stations given a rectangle defined by the coordinates
    :param sw_lat: Southwest latitude
    :param sw_lon: Southwest longitude
    :param ne_lat: Northeast latitude
    :param ne_lon: Northeast longitude
    :return: A list of `Place`
    """
    params = {"swLat": sw_lat, "swLon": sw_lon, "neLat": ne_lat, "neLon": ne_lon}
    json = get_tfl_json(ENDPOINT, params=params)
    return from_json(json)


def by_id(id: str) -> Place:
    json = get_tfl_json(f"{ENDPOINT}/{id}")
    return from_json(json)


def search(query: str) -> List[Place]:
    json = get_tfl_json(f"{ENDPOINT}/Search", params={"query": query})
    return from_json(json)

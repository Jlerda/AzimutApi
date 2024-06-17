from typing import Annotated
from fastapi import APIRouter, Query, HTTPException
from starlette import status
from numpy import arctan2, sin, cos, radians, arcsin, sqrt
from math import degrees

router = APIRouter()

EARTH_RADIUS_METERS = 6371000
EARTH_RADIUS_KM = 6371
UNIT_MEASURES = ['km', 'm']


@router.get("/haversine_distance/", status_code=status.HTTP_200_OK)
async def get_haversine_distance(start_lat: Annotated[float, Query(le=90, ge=-90)],
                                 start_long: Annotated[float, Query(le=180, ge=-180)],
                                 end_lat: Annotated[float, Query(le=90, ge=-90)],
                                 end_long: Annotated[float, Query(le=180, ge=-180)],
                                 unit_measure: str = 'km'):
    start_lat = radians(start_lat)
    start_long = radians(start_long)
    end_lat = radians(end_lat)
    end_long = radians(end_long)

    if unit_measure.lower() not in UNIT_MEASURES:
        raise HTTPException(status_code=404, detail='Invalid unit_measure.')

    radius = EARTH_RADIUS_KM if unit_measure == 'km' else EARTH_RADIUS_METERS
    distance = 2 * radius * arcsin(
        sqrt((1 - cos(end_lat - start_lat) + cos(start_lat) * cos(end_lat) * (1 - cos(end_long - start_long))) / 2))

    return {"distance": round(distance, 3)}


@router.get("/azimuth_angle/", status_code=status.HTTP_200_OK)
async def get_azimuth_angle(start_lat: Annotated[float, Query(le=90, ge=-90)],
                            start_long: Annotated[float, Query(le=180, ge=-180)],
                            end_lat: Annotated[float, Query(le=90, ge=-90)],
                            end_long: Annotated[float, Query(le=180, ge=-180)],
                            convert_negative_angle: bool = False):
    start_lat = radians(start_lat)
    start_long = radians(start_long)
    end_lat = radians(end_lat)
    end_long = radians(end_long)
    delta_long = end_long - start_long

    azimut = round(degrees(arctan2(
        sin(delta_long) * cos(end_lat),
        cos(start_lat) * sin(end_lat) - (sin(start_lat) * cos(end_lat) * cos(delta_long))
    )), 1)

    if azimut < 0 and convert_negative_angle:
        azimut += 360
    return {"azimuth_angle": azimut}

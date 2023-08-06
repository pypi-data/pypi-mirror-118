import requests
import os
import json
from hestia_earth.utils.tools import current_time_ms

from hestia_earth.models.log import logger

MAX_AREA_SIZE = 5000


def has_geospatial_data(site: dict, by_region=True):
    """
    Determines whether the Site has enough geospatial data to run calculations. We are checking for:
    1. If the coordinates (latitude and longitude) are present
    2. Otherwise if the `region` or `country` is present
    3. Otherwise if the `boundary` is present
    Note: this is a general pre-check only, each model can have 1 or more other checks.

    Parameters
    ----------
    site : dict
        The `Site` node.
    by_region : bool
        If we can run using the region ID (`region` or `country` fields). Defaults to true.

    Returns
    -------
    bool
        If we should run geospatial calculations on this model or not.
    """
    has_coordinates = site.get('latitude') is not None and site.get('longitude') is not None
    has_region = _site_gadm_id(site) is not None
    has_boundary = site.get('boundary') is not None
    return has_coordinates or (by_region and has_region) or has_boundary


def _site_gadm_id(site: dict): return site.get('region', site.get('country', {})).get('@id')


def _url_suffix(args: dict):
    # download in priority: with latitude, with boundary, with region/country id
    if args.get('latitude') and args.get('longitude'):
        return 'coordinates'
    if args.get('boundary'):
        return 'boundary'
    if args.get('gadm_id'):
        return 'gadm'


def _download_data(args: dict):
    # download in priority: with latitude, with boundary, with region/country id
    if args.get('latitude') and args.get('longitude'):
        args.pop('gadm_id', None)
        args.pop('boundary', None)
    if args.get('boundary'):
        args.pop('latitude', None)
        args.pop('longitude', None)
        args.pop('gadm_id', None)
    if args.get('gadm_id'):
        args.pop('latitude', None)
        args.pop('longitude', None)
        args.pop('boundary', None)
        # TODO: need this as fixtures region is bigger than 2500km2
        args['max_area'] = MAX_AREA_SIZE
    return json.dumps(args)


def download(**kwargs) -> dict:
    """
    Downloads data from Hestia Earth Engine API.

    Returns
    -------
    dict
        Data returned from the API.
    """
    # make sure we are not using an old url
    base_url = os.getenv('GEE_API_URL').replace('coordinates', '')
    url = f"{base_url}{_url_suffix(kwargs)}"
    headers = {'Content-Type': 'application/json', 'X-Api-Key': os.getenv('GEE_API_KEY')}
    now = current_time_ms()
    try:
        res = requests.post(url, _download_data(kwargs), headers=headers).json()
        error = res.get('error')
        if error:
            raise Exception(error)
        properties = res.get('features', [{'properties': {}}])[0].get('properties')
        logger.debug('model=spatial, time=%sms, properties=%s', current_time_ms() - now, properties)
        return properties
    except Exception as e:
        logger.error('model=spatial, time=%sms, error=%s', current_time_ms() - now, str(e))
        return {}

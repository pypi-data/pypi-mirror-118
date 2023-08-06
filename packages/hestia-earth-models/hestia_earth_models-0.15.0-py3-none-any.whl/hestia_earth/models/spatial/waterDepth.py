from hestia_earth.schema import MeasurementStatsDefinition, SiteSiteType

from hestia_earth.models.log import logger
from hestia_earth.models.utils.measurement import _new_measurement
from hestia_earth.models.utils.site import valid_site_type
from .utils import download, has_geospatial_data
from . import MODEL

TERM_ID = 'waterDepth'


def _measurement(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    measurement = _new_measurement(TERM_ID, MODEL)
    measurement['value'] = [value]
    measurement['statsDefinition'] = MeasurementStatsDefinition.SPATIAL.value
    return measurement


def _run(site: dict):
    field = 'first'
    value = download(collection='users/hestiaplatform/gebco_2021_tid',
                     ee_type='raster',
                     latitude=site.get('latitude'),
                     longitude=site.get('longitude'),
                     boundary=site.get('boundary'),
                     fields=field
                     ).get(field, None)

    return [_measurement(value)] if value else []


def _should_run(site: dict):
    should_run = has_geospatial_data(site) and valid_site_type(site, [SiteSiteType.SEA_OR_OCEAN.value])
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else []

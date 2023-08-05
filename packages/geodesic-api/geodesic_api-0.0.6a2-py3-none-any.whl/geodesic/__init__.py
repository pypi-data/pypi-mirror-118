# If this was checked out from a git tag, this version number may not match.
# Refer to the git tag for the correct version number
__version__ = '0.0.6a2'

from geodesic.oauth import AuthManager
from geodesic.stac import Item, Feature, FeatureCollection
from geodesic.raster import Raster, RasterCollection
from geodesic.datasets import Dataset, DatasetList, list_datasets

__all__ = [
    "authenticate",
    "Item",
    "Feature",
    "FeatureCollection",
    "Raster",
    "RasterCollection",
    "Dataset",
    "DatasetList",
    "list_datasets",
]


def authenticate():
    auth = AuthManager()
    auth.authenticate()

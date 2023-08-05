import datetime as pydatetime
from dateutil.parser import parse

from collections import defaultdict

from geodesic.client import get_client
from geodesic.stac import FeatureCollection
from geodesic.widgets import get_template_env, jinja_available

from shapely.geometry import shape

from typing import Optional, Union, List, Tuple


class Dataset:
    """Allows interaction with SeerAI datasets.

    Dataset provides a way to interact with datasets in the SeerAI.

    Args:
        **spec (dict): Dictionary with all properties in the dataset
    """

    def __init__(self, **spec):
        self.name = spec["name"]
        self.alias = spec["alias"]
        self._spec = {}
        self._spec.update(spec)
        self._client = get_client()

    @property
    def type(self):
        return self._spec["type"]

    @property
    def subtype(self):
        return self._spec["subtype"]

    @property
    def stac(self):
        if self.type != "stac":
            raise ValueError("This dataset is not a STAC dataset")
        return self._spec.get("stac", {})

    def _repr_html_(self, add_style=True):
        if not jinja_available():
            return self.__repr__()

        template = get_template_env().get_template("dataset_template.html.jinja")
        # Make this look like dataset list but with a single entry so one template can be used for both
        dataset = {self.name: self}
        return template.render(datasets=dataset)

    def query(
        self,
        bbox: Optional[List] = None,
        datetime: Union[List, Tuple] = None,
        limit: Optional[Union[bool, int]] = 10,
        intersects=None,
        **kwargs
    ):
        """ Query the dataset for items.

        Query this service's OGC Features or STAC API. Unless specified by the 'api' keyword,
        this will prefer a STAC search over a OGC Features query

        Args:
            bbox: The spatial extent for the query as a bounding box. Example: [-180, -90, 180, 90]
            datetime: The temporal extent for the query formatted as a list: [start, end].
            limit: The maximum number of items to return in the query.

        Returns:
            A :class:`geodesic.stac.FeatureCollection` with all items in the dataset matching the query.

        Examples:
            A query on the `sentinel-2-l2a` dataset with a given bouding box and time range. Additionally it
            you can apply filters on the parameters in the items.

            >>> bbox = geom.bounds
            >>> date_range = (datetime.datetime(2020, 12,1), datetime.datetime.now())
            >>> ds.query(
            ...          bbox=bbox,
            ...          datetime=date_range,
            ...          query={'properties.eo:cloud_cover': {'lte': 10}}
            ... )
        """
        api = kwargs.pop("api", None)
        # clients = self.clients

        if api is None:
            api = "stac"

        else:
            if api not in ["features", "stac"]:
                raise ValueError("query with api '{0}' not supported.".format(api))

        query_all = False
        if not limit:
            limit = 500
            query_all = True

        # Request query/body
        params = {"limit": limit}

        if api == "features":
            url = "/spacetime/api/v{version}/stac/collections/{name}/items".format(
                version=self._client._api_version, name=self.name
            )

        elif api == "stac":
            params["collections"] = [self.name]
            url = "/spacetime/api/v{version}/stac/search".format(
                version=self._client._api_version
            )

        # If the bounding box only provided.
        if bbox is not None and intersects is None:
            if api == "stac":
                params["bbox"] = bbox
            else:
                params["bbox"] = ",".join(map(str, bbox))
        # If a intersection geometry was provided
        if intersects is not None:
            # Geojson
            if isinstance(intersects, dict):
                try:
                    g = shape(intersects)
                except ValueError:
                    try:
                        g = shape(intersects['geometry'])
                    except Exception as e:
                        raise ValueError('could not determine type of intersection geometry') from e

            elif hasattr(intersects, "__geo_interface__"):
                g = intersects

            else:
                raise ValueError("intersection geometry must be either geojson or object with __geo_interface__")

            # If STAC, use the geojson
            if api == "stac":
                params["intersects"] = g.__geo_interface__
            # Bounding box is all that's supported for OAFeat
            else:
                try:
                    # Shapely
                    params["bbox"] = g.bounds
                except AttributeError:
                    # ArcGIS
                    params["bbox"] = g.extent

        # STAC search specific
        if api == "stac":
            ids = kwargs.pop("ids", None)
            if ids is not None:
                params["ids"] = ids
            query = kwargs.pop("query", None)
            if query is not None:
                for k, v in query.items():

                    gt = v.get("gt")
                    if gt is not None and isinstance(gt, pydatetime.datetime):
                        v["gt"] = gt.isoformat()
                    lt = v.get("lt")
                    if lt is not None and isinstance(lt, pydatetime.datetime):
                        v["lt"] = lt.isoformat()
                    gte = v.get("gte")
                    if gte is not None and isinstance(gte, pydatetime.datetime):
                        v["gte"] = gte.isoformat()
                    lte = v.get("lte")
                    if lte is not None and isinstance(lte, pydatetime.datetime):
                        v["lte"] = lte.isoformat()
                    eq = v.get("eq")
                    if eq is not None and isinstance(eq, pydatetime.datetime):
                        v["eq"] = eq.isoformat()
                    neq = v.get("neq")
                    if neq is not None and isinstance(neq, pydatetime.datetime):
                        v["neq"] = neq.isoformat()
                    query[k] = v

                params["query"] = query
            sortby = kwargs.pop("sortby", None)
            if sortby is not None:
                params["sortby"] = sortby

            fields = kwargs.pop("fields", None)
            if fields is not None:
                fieldsObj = defaultdict(list)
                # fields with +/-
                if isinstance(fields, list):
                    for field in fields:
                        if field.startswith("+"):
                            fieldsObj["include"].append(field[1:])
                        elif field.startswith("-"):
                            fieldsObj["exclude"].append(field[1:])
                        else:
                            fieldsObj["include"].append(field)
                else:
                    fieldsObj = fields
                params["fields"] = fieldsObj

        if datetime is not None:
            params["datetime"] = "/".join([parsedate(d).isoformat() for d in datetime])

        if api == "features":
            res = self._client.get(url, **params)
        elif api == "stac":
            res = self._client.post(url, **params)

        collection = FeatureCollection(obj=res, dataset=self, query=params)

        if query_all:
            collection.get_all()

        if api == "stac":
            collection._is_stac = True

        return collection

    @property
    def clients(self):
        return self._spec.get("clients", [])

    @property
    def bands(self):
        return Bands(item_assets=self.stac['itemAssets'], ds_name=self.alias)


def parsedate(dt):
    try:
        return parse(dt)
    except TypeError:
        return dt


class DatasetList:
    def __init__(self, datasets):
        self.ddict = {dataset.name: dataset for dataset in datasets}

    def __getitem__(self, key):
        return self.ddict[key]

    def _repr_html_(self):
        # html = style
        # html += '<div class="container">'
        # for d in self.ddict.values():
        #     html += d._repr_html_(False)
        # html += "</div>"
        # return html
        if not jinja_available():
            return self.__repr__()
        template = get_template_env().get_template("dataset_template.html.jinja")
        return template.render(datasets=self.ddict)


class Bands(dict):
    def __init__(self, item_assets=None, ds_name=None):
        self.update(item_assets)
        self._ds_name = ds_name

    def _repr_html_(self, add_style=True):
        if not jinja_available():
            return self.__repr__()
        template = get_template_env().get_template("bands_template.html.jinja")
        return template.render(bands=self)

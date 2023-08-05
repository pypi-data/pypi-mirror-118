from geodesic.client import get_client
from geodesic.datasets.dataset import Dataset, DatasetList
from typing import List, Union


def list_datasets(ids: Union[List, str] = [], search: str = None):
    client = get_client()

    url = "/entanglement/api/v1/datasets"
    params = []
    if ids:
        if isinstance(ids, str):
            ids = ids.split(",")
        # url = url + "?ids=" + ",".join(ids)
        params.append("ids=" + ",".join(ids))

    if search:
        params.append(f"search={search}")

    url = url + "?" + "&".join(params)
    resp = client.get(url)

    ds = [Dataset(**r) for r in resp["datasets"]]
    datasets = DatasetList(ds)
    return datasets

import ssl
from pathlib import Path

import truststore
from requests import Session
from requests.adapters import HTTPAdapter
from requests.utils import requote_uri

# truststore.inject_into_ssl()  # does not fit well package's usage
ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

remote_url_to_download: str = (
    "https://sigweb-rec.grandlyon.fr/qgis/plugins/dryade_n_tree_creator/version/0.1/download/dryade_n_tree_creator.zip"
)

local_file_path: Path = Path("tests/fixtures/tmp/").joinpath(
    remote_url_to_download.split("/")[-1]
)
local_file_path.parent.mkdir(parents=True, exist_ok=True)


class TruststoreAdapter(HTTPAdapter):
    """_summary_

    Source: https://stackoverflow.com/a/78265028/2556577

    Args:
        HTTPAdapter (_type_): _description_
    """

    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        return super().init_poolmanager(connections, maxsize, block, ssl_context=ctx)


with Session() as dl_session:
    dl_session.mount("https://", TruststoreAdapter())
    with dl_session.get(url=requote_uri(remote_url_to_download)) as req:
        req.raise_for_status()
        local_file_path.write_bytes(req.content)

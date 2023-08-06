import json
import typing
from starlette.responses import Response
from red_warden.helpers import RWCustomJsonEncoder


class RWJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            cls=RWCustomJsonEncoder,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")

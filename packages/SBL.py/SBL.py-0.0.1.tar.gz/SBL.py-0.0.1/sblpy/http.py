import requests

from typing import Any
from urllib.parse import quote as _uriquote

class Route:
  BASE: str = "https://smartbots.tk/api/auth"

  def __init__(
    self,
    method: str,
    path: str,
    headers: dict = {},
    json: dict = {},
    **parameters: Any
  ) -> None:
    self.path: str = path
    self.method: str = method.upper()
    url = self.BASE + self.path
    self.kwargs = {
      "headers": headers,
      "json": json
    }
    if parameters:
      url = url.format_map(
        {
          k: _uriquote(
            v
          ) if isinstance(
            v,
            str
          ) else v for k, v in parameters.items()
        }
      )
      self.url: str = url

  def go(self):
    return requests.request(
      self.method,
      self.url,
      **self.kwargs
    )

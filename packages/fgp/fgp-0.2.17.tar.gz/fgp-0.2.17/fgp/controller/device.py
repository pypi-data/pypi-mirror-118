from typing import List, Dict
from .client import Client
from fgp.model.model import FGModel
from fgp.utils.datetime_to_ms import datetime_to_ms
import urllib.parse
import datetime


class Device:

    _client: Client = None

    def __init__(self, client: Client):
        self._client = client

    def get(self, device_type: str, lookup_key: str, lookup_name: str = 'name'):
        return self._client.get(route=f'{device_type}/{lookup_name}/{lookup_key}')

    def get_many(
            self,
            device_type: str,
            device_names: str,
            extension_names: List[str]
    ) -> dict:
        data = {
            'devices': device_names,
            'extensions': extension_names
        }
        res = self._client.post(route=f'{device_type}', data=data)
        if len(res) == 0:
            return None
        return res

    def create(self, device_type: str, device_name: str, device_description: str = None):
        data = {
            "name": device_name,
            "type": device_type,
            "description": device_description
        }
        res = self._client.put(route=f'{device_type}', data=data)
        return res

    # def get_schema(self, extension_name) -> FGModel:
    #     data = self._client.get(route=f'{reference_name}')
    #     return FGModel.from_object(reference_name, data.get('links', {}).get('persistenceInfo', []))


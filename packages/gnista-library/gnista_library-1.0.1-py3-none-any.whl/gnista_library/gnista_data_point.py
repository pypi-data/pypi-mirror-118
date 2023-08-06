import json

import attr
import pandas as pd
from oauth2_client.credentials_manager import CredentialManager, ServiceInformation
from pandas import DataFrame
from structlog import get_logger

from data_point_client import AuthenticatedClient
from data_point_client.api.data_point import data_point_get_data
from data_point_client.models import GetDataResponse, GetSeriesResponse

from .gnista_connetion import GnistaConnection

log = get_logger()


class GnistaDataPoint:
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    DATE_NAME = "Date"
    VALUE_NAME = "Value"

    def __init__(self, connection: GnistaConnection):
        self.connection = connection

    def get_data_point(self, id: str) -> DataFrame:
        token = self.connection.get_access_token()
        client = AuthenticatedClient(base_url=self.connection.base_url + "/datapoint", token=token)

        byte_content = data_point_get_data.sync_detailed(client=client, data_point_id=id, window_hours=0).content
        log.debug("Received Response from gnista.io", content=byte_content)

        content_text = byte_content.decode("utf-8")
        d = json.loads(content_text)
        my_data = GetSeriesResponse.from_dict(d)
        return self._from_time_frames(time_frames=my_data.curve.to_dict())

    def _from_time_frames(self, time_frames: dict, date_format: str = DATE_FORMAT) -> DataFrame:

        if not isinstance(time_frames, dict):
            raise TypeError

        log.debug("Reading data as Pandas DataFrame")

        data_record = list()
        for date in time_frames:
            value = time_frames[date]
            data_record.append({self.DATE_NAME: date, self.VALUE_NAME: value})

        data_frame = pd.DataFrame.from_records(data_record, columns=[self.DATE_NAME, self.VALUE_NAME])

        data_frame[self.DATE_NAME] = pd.to_datetime(data_frame[self.DATE_NAME], format=date_format)

        data_frame[self.VALUE_NAME] = pd.to_numeric(data_frame[self.VALUE_NAME])

        data_frame = data_frame.set_index(data_frame[self.DATE_NAME])
        data_frame = data_frame.drop([self.DATE_NAME], axis=1)

        return data_frame

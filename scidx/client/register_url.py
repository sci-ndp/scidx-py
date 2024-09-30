from typing import Union, Optional
from datetime import datetime
import requests

class StreamProcessing:
    def __init__(self, refresh_rate: str= None, data_key: str= None):
        """
        Stream Processing Parameters:
        - refresh_rate: The refresh rate for the data stream (e.g., "5 seconds").
        - data_key: The key for the response data in the JSON file (e.g., "results").
        """
        self.refresh_rate = refresh_rate
        self.data_key = data_key

    def to_dict(self):
        return {
            "refresh_rate": self.refresh_rate,
            "data_key": self.data_key,
        }


class CSVProcessing:
    def __init__(self, delimiter: str, header_line: int, start_line: int, comment_char: str = None):
        """
        CSV Processing Parameters:
        - delimiter: The delimiter used in the CSV file (e.g., ",").
        - header_line: The line number of the header in the CSV file.
        - start_line: The line number where the data starts in the CSV file.
        - comment_char: Optional. The character used for comments in the CSV file (e.g., "#").
        """
        self.delimiter = delimiter
        self.header_line = header_line
        self.start_line = start_line
        self.comment_char = comment_char

    def to_dict(self):
        data = {
            "delimiter": self.delimiter,
            "header_line": self.header_line,
            "start_line": self.start_line,
        }
        if self.comment_char:
            data["comment_char"] = self.comment_char
        return data


class TXTProcessing:
    def __init__(self, delimiter: str, header_line: int, start_line: int):
        """
        TXT Processing Parameters:
        - delimiter: The delimiter used in the TXT file (e.g., "\\t").
        - header_line: The line number of the header in the TXT file.
        - start_line: The line number where the data starts in the TXT file.
        """
        self.delimiter = delimiter
        self.header_line = header_line
        self.start_line = start_line

    def to_dict(self):
        return {
            "delimiter": self.delimiter,
            "header_line": self.header_line,
            "start_line": self.start_line,
        }


class JSONProcessing:
    def __init__(self, info_key: str = None, additional_key: str = None, data_key: str = None):
        """
        JSON Processing Parameters:
        - info_key: Optional. The key for additional information in the JSON file.
        - additional_key: Optional. An additional key in the JSON file.
        - data_key: The key for the response data in the JSON file (e.g., "results").
        """
        self.info_key = info_key
        self.additional_key = additional_key
        self.data_key = data_key

    def to_dict(self):
        return {
            "info_key": self.info_key,
            "additional_key": self.additional_key,
            "data_key": self.data_key,
        }


class NetCDFProcessing:
    def __init__(self, group: str = None):
        """
        NetCDF Processing Parameters:
        - group: Optional. The group within the NetCDF file.
        """
        self.group = group

    def to_dict(self):
        return {
            "group": self.group,
        }


def register_url(self, resource_name: str, resource_title: str, owner_org: str,
                 resource_url: str, file_type: str, processing: Optional[Union[StreamProcessing, CSVProcessing, TXTProcessing, JSONProcessing, NetCDFProcessing]] = None,
                 notes: str = "", extras: dict = None, mapping: Optional[dict] = None, timestamp: Optional[datetime] = None) -> dict:
    """
    Create a new URL resource in the sciDX system.

    Parameters
    ----------
    resource_name : str
        The name of the resource.
    resource_title : str
        The title of the resource.
    owner_org : str
        The name of the organization.
    resource_url : str
        The URL of the resource.
    file_type : str, optional
        The type of the file (e.g., stream, CSV, TXT, JSON, NetCDF).
    processing : Union[StreamProcessing, CSVProcessing, TXTProcessing, JSONProcessing, NetCDFProcessing], optional
        The processing information specific to the file type.
    notes : str, optional
        Additional notes about the resource.
    timestamp : datetime
    extras : dict, optional
        Additional metadata to be added to the resource.
    mapping : dict, optional
        Mapping information for the dataset.

    Returns
    -------
    dict
        A dictionary containing the response from the API.
    """
    url = f"{self.api_url}/url"
    headers = self._get_headers()

    if timestamp:
        if not extras:
            extras = {}
        extras["timestamp"] = timestamp.strftime('%Y-%m-%dT%H:%M:%S')

    # Build the payload
    payload = {
        "resource_name": resource_name,
        "resource_title": resource_title,
        "owner_org": owner_org,
        "resource_url": resource_url,
        "notes": notes,
        "extras": extras or {},
        "mapping": mapping or {},
    }

    if file_type:
        payload["file_type"] = file_type
    if processing:
        payload["processing"] = processing.to_dict()

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        raise requests.exceptions.HTTPError(f"Error: {response.content.decode('utf-8')}")


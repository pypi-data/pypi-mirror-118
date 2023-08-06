import platform
import re
from collections import OrderedDict
from enum import Enum
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from marshmallow import ValidationError
from ratelimit import limits, sleep_and_retry
from requests import get
from requests.exceptions import ConnectionError

from .exceptions import APIError, CacheError
from .issue import Issue, IssueList, IssueSchema
from .publisher import Publisher, PublisherList, PublisherSchema
from .sqlite_cache import SqliteCache
from .story_arc import StoryArc, StoryArcList, StoryArcSchema
from .volume import Volume, VolumeList, VolumeSchema

MINUTE = 60


class CVType(Enum):
    VOLUME = 4050
    ISSUE = 4000
    PUBLISHER = 4010
    ARC = 4045

    def __str__(self):
        return f"{self.value}"


class Session:
    def __init__(self, api_key: str, cache: Optional[SqliteCache] = None):
        self.api_key = api_key
        self.header = {"User-Agent": f"Simyan/{platform.system()}: {platform.release()}"}
        self.api_url = "https://comicvine.gamespot.com/api/{}/"
        self.cache = cache

    @sleep_and_retry
    @limits(calls=20, period=MINUTE)
    def call(self, endpoint: List[Union[str, int]], params: Dict[str, Union[str, int]] = None) -> Dict[str, Any]:
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        params["format"] = "json"

        cache_params = ""
        if params:
            ordered_params = OrderedDict(sorted(params.items(), key=lambda x: x[0]))
            cache_params = f"?{urlencode(ordered_params)}"

        url = self.api_url.format("/".join(str(e) for e in endpoint))
        cache_key = f"{url}{cache_params}"
        cache_key = re.sub(r"(.+api_key=)(.+?)(&.+)", r"\1*****\3", cache_key)

        if self.cache:
            try:
                cached_response = self.cache.get(cache_key)
                if cached_response is not None:
                    return cached_response
            except AttributeError as e:
                raise CacheError(f"Cache object passed in is missing attribute: {repr(e)}")

        try:
            response = get(url, params=params, headers=self.header)
        except ConnectionError as e:
            raise APIError(f"Connection error: {repr(e)}")

        try:
            data = response.json()
        except JSONDecodeError as e:
            raise APIError(f"Invalid request: {repr(e)}")

        if "error" in data and data["error"] != "OK":
            raise APIError(data["error"])
        if self.cache:
            try:
                self.cache.insert(cache_key, data)
            except AttributeError as e:
                raise CacheError(f"Cache object passed in is missing attribute: {repr(e)}")

        return data

    def publisher(self, _id: int) -> Publisher:
        try:
            return PublisherSchema().load(self.call(["publisher", f"{CVType.PUBLISHER}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def publisher_list(self, params: Dict[str, Union[str, int]] = None) -> PublisherList:
        results = self._retrieve_all_responses("publishers", params)
        return PublisherList(results)

    def volume(self, _id: int) -> Volume:
        try:
            return VolumeSchema().load(self.call(["volume", f"{CVType.VOLUME}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def volume_list(self, params: Dict[str, Union[str, int]] = None) -> VolumeList:
        results = self._retrieve_all_responses("volumes", params)
        return VolumeList(results)

    def issue(self, _id: int) -> Issue:
        try:
            return IssueSchema().load(self.call(["issue", f"{CVType.ISSUE}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def issue_list(self, params: Dict[str, Union[str, int]] = None) -> IssueList:
        results = self._retrieve_all_responses("issues", params)
        return IssueList(results)

    def story_arc(self, _id: int) -> StoryArc:
        try:
            return StoryArcSchema().load(self.call(["story_arc", f"{CVType.ARC}-{_id}"])["results"])
        except ValidationError as error:
            raise APIError(error.messages)

    def story_arc_list(self, params: Dict[str, Union[str, int]] = None) -> StoryArcList:
        results = self._retrieve_all_responses("story_arcs", params)
        return StoryArcList(results)

    def _retrieve_all_responses(self, resource: str, params: Dict[str, Union[str, int]] = None):
        if params is None:
            params = {}
        response = self.call([resource], params=params)
        result = response["results"]
        while response["number_of_total_results"] > response["offset"] + response["number_of_page_results"]:
            params["offset"] = response["offset"] + response["number_of_page_results"]
            response = self.call([resource], params=params)
            result.extend(response["results"])
        return result

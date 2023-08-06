import typing as _typing
from argparse import ArgumentError

import requests as _requests

from .types import (
    ArchiverDisconnectedPV,
    ArchiverDroppedByTypeChangePV,
    ArchiverGenericReponse,
    ArchiverPausedPV,
    ArchiverSamplingMethod,
    ArchiverStatusPV,
    _make_archiver_disconnected_pv,
    _make_archiver_paused_pv,
    _make_archiver_status_pv,
)

_default_base_url = "https://10.0.38.42"


class ArchiverLoginException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ArchiverClient:
    def __init__(
        self,
        base_url: str = _default_base_url,
        username: _typing.Optional[str] = None,
        password: _typing.Optional[str] = None,
    ) -> None:

        self._mgmt_url = f"{base_url}/mgmt/bpl"
        self._retrieval_url = f"{base_url}/retrieval/bpl"
        self._retrieval_data_url = f"{base_url}/retrieval/data"
        self._authenticated = False

        self._session: _requests.Session = _requests.Session()
        self._session.verify = False
        if username and password:
            self.login(username, password)

    @property
    def authenticated(self):
        return self._authenticated

    def login(self, username: str, password: str) -> ArchiverGenericReponse:
        data = {"username": username, "password": password}

        response = self._session.post(
            f"{self._mgmt_url}/login", data=data, verify=False
        )
        self._authenticated = (
            response.status_code == 200 and "authenticated" in response.text
        )
        if not self.authenticated:
            raise ArchiverLoginException(f"failed to authenticat user {username}")

        response_json = None
        try:
            response_json = response.json()
        except ValueError:
            response_json = None

        return ArchiverGenericReponse(
            success=self.authenticated,
            status_code=response.status_code,
            text=response.text,
            json=response_json,
        )

    def logout(self):
        raise NotImplementedError()

    def resume_pv(self, pv_name: str) -> ArchiverGenericReponse:
        raise NotImplementedError()

    def delete_pv(self, pv_name: str) -> ArchiverGenericReponse:
        raise NotImplementedError()

    def pause_pv(self, pv_name: str) -> ArchiverGenericReponse:
        if not self.authenticated:
            raise ArchiverLoginException("operation requires authentication")

        if not pv_name:
            raise ValueError()

        response = self._session.get(f"{self._mgmt_url}/pauseArchivingPV?pv={pv_name}")
        success = (
            response.status_code == 200
            and (f"Successfully paused the archiving of PV {pv_name}")
            or (f"PV {pv_name} is already paused") in response.text
        )
        response_json = None
        try:
            response_json = response.json()
        except ValueError:
            response_json = None

        return ArchiverGenericReponse(
            success=success,
            status_code=response.status_code,
            text=response.text,
            json=response_json,
        )

    def change_pv_archival_parameters(
        self, pv: str, sampling_method: ArchiverSamplingMethod, sampling_period: float
    ):
        """
        /changeArchivalParameters - Change the archival parameters for a PV.
        pv: The name of the pv.
        samplingperiod: The new sampling period in seconds.
        samplingmethod: The new sampling method For now, this is one of SCAN or MONITOR.
        """
        if sampling_method < 0.01:
            raise ArgumentError(f"'sampling_period' {sampling_period} invalue range")
        if (
            type(sampling_method) != str
            and type(sampling_method) != ArchiverSamplingMethod
        ):
            raise ArgumentError(f"'sampling_method' {sampling_method} invalid type")
        if (
            sampling_method != ArchiverSamplingMethod.SCAN
            and sampling_method != ArchiverSamplingMethod.MONITOR
        ):
            raise ArgumentError(f"'sampling_method' {sampling_method} invalid option")

        # sampling_method_value = sampling_method.value

        # /changeArchivalParameters
        raise NotImplementedError()

    def get_pv_details(self, pv_name: str):
        raise NotImplementedError()

    def get_currently_disconnected_pvs(self) -> _typing.List[ArchiverDisconnectedPV]:
        return [
            _make_archiver_disconnected_pv(**pv)
            for pv in self._session.get(
                f"{self._mgmt_url}/getCurrentlyDisconnectedPVs", verify=False
            ).json()
        ]

    def get_paused_pvs_report(self) -> _typing.List[ArchiverPausedPV]:
        return [
            _make_archiver_paused_pv(**pv)
            for pv in self._session.get(
                f"{self._mgmt_url}/getPausedPVsReport", verify=False
            ).json()
        ]

    def get_matching_pvs(self, search: str, limit: int = 500) -> _typing.List[str]:
        return [
            pv
            for pv in self._session.get(
                f"{self._retrieval_url}/getMatchingPVs",
                params={"pv": search, "limit": limit},
                verify=False,
            ).json()
        ]

    def get_pv_status(self, search: str, reporttype: str = "short") -> ArchiverStatusPV:
        return [
            _make_archiver_status_pv(**pv)
            for pv in self._session.get(
                f"{self._mgmt_url}/getPVStatus",
                params={"pv": search, "reporttype": reporttype},
                verify=False,
            ).json()
        ]

    def get_pvs_by_dropped_events_type_change(
        self, limit: int = 200
    ) -> _typing.List[ArchiverDroppedByTypeChangePV]:
        return [
            ArchiverDroppedByTypeChangePV(
                pv_name=pv["pvName"], events_dropped=pv["eventsDropped"]
            )
            for pv in self._session.get(
                f"{self._mgmt_url}/getPVsByDroppedEventsTypeChange",
                params={limit: limit},
            ).json()
        ]

    def change_type_for_pv(self):
        raise NotImplementedError()


def getPVsByDroppedEventsTypeChange(
    base_url: str = _default_base_url,
) -> _typing.List[ArchiverDroppedByTypeChangePV]:
    return ArchiverClient(base_url=base_url).get_pvs_by_dropped_events_type_change()


def getCurrentlyDisconnectedPVs(
    base_url: str = _default_base_url,
) -> _typing.List[ArchiverDisconnectedPV]:
    return ArchiverClient(base_url=base_url).get_currently_disconnected_pvs()


def getPausedPVsReport(
    base_url: str = _default_base_url,
) -> _typing.List[ArchiverPausedPV]:
    return ArchiverClient(base_url=base_url).get_paused_pvs_report()


def getMatchingPVs(search: str, base_url: str = _default_base_url) -> _typing.List[str]:
    return ArchiverClient(base_url=base_url).get_matching_pvs(search=search)


def getPVStatus(search: str, base_url: str = _default_base_url):
    return ArchiverClient(base_url=base_url).get_pv_status(search=search)

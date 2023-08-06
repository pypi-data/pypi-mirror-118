from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from tfl.api.presentation.entities.additional_properties import AdditionalProperties


@dataclass
class Crowding:
    pass


@dataclass
class LineGroup:
    stationAtcoCode: str
    lineIdentifier: List[str]


@dataclass
class LineModeGroup:
    modeName: str
    lineIdentifier: List[str]


@dataclass
class Identifier:
    id: str
    name: str
    uri: str
    type: str
    crowding: Crowding
    routeType: str
    status: str


@dataclass
class RouteSection:
    id: str
    name: str
    direction: str
    originationName: str
    destinationName: str
    routeSectionNaptanEntrySequence: List[RouteSectionNaptanEntrySequence]
    lineId: Optional[str] = None
    routeCode: Optional[str] = None
    lineString: Optional[str] = None
    validTo: Optional[str] = None
    validFrom: Optional[str] = None


@dataclass
class StopPoint:
    naptanId: str
    modes: List[str]
    stationNaptan: str
    lines: List[Identifier]
    linesGroup: List[LineGroup]
    lineModeGroups: List[LineModeGroup]
    status: bool
    id: str
    commonName: str
    additionalProperties: List[AdditionalProperties]
    children: List[StopPoint]
    childrenUrl: List[str]
    lat: float
    lon: float
    platformName: Optional[str] = None
    indicator: Optional[str] = None
    stopLetter: Optional[str] = None
    smsCode: Optional[str] = None
    stopType: Optional[str] = None
    accessibilitySummary: Optional[str] = None
    fullName: Optional[str] = None
    naptanMode: Optional[str] = None
    url: Optional[str] = None
    hubNaptanCode: Optional[str] = None
    icsCode: Optional[str] = None
    placeType: Optional[str] = None
    distance: Optional[float] = None


@dataclass
class RouteSectionNaptanEntrySequence:
    ordinal: int
    stopPoint: Optional[StopPoint] = None


@dataclass
class Disruption:
    category: str
    categoryDescription: str
    description: str
    affectedRoutes: List[RouteSection]
    affectedStops: List[StopPoint]
    closureText: str
    created: Optional[str] = None
    type: Optional[str] = None
    lastUpdate: Optional[str] = None

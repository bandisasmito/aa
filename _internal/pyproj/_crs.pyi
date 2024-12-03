from collections.abc import Iterable
from typing import Any, NamedTuple, Optional

from pyproj.crs.enums import CoordinateOperationType
from pyproj.enums import ProjVersion, WktVersion

class Axis:
    name: str
    abbrev: str
    direction: str
    unit_conversion_factor: float
    unit_name: str
    unit_auth_code: str
    unit_code: str
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class AreaOfUse:
    west: float
    south: float
    east: float
    north: float
    name: str
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @property
    def bounds(self) -> tuple[float, float, float, float]: ...

class Base:
    name: str
    @property
    def remarks(self) -> str: ...
    @property
    def scope(self) -> str: ...
    def to_wkt(
        self,
        version: WktVersion | str = WktVersion.WKT2_2019,
        pretty: bool = False,
        output_axis_rule: bool | None = None,
    ) -> str: ...
    def to_json(self, pretty: bool = False, indentation: int = 2) -> str: ...
    def to_json_dict(self) -> dict: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: Any) -> bool: ...
    def is_exact_same(self, other: Any) -> bool: ...

class _CRSParts(Base):
    @classmethod
    def from_user_input(cls, user_input: Any) -> "_CRSParts": ...

class Ellipsoid(_CRSParts):
    semi_major_metre: float
    semi_minor_metre: float
    is_semi_minor_computed: float
    inverse_flattening: float
    @staticmethod
    def from_authority(auth_name: str, code: int | str) -> "Ellipsoid": ...
    @staticmethod
    def from_epsg(code: int | str) -> "Ellipsoid": ...
    @staticmethod
    def from_string(ellipsoid_string: str) -> "Ellipsoid": ...
    @staticmethod
    def from_json_dict(ellipsoid_dict: dict) -> "Ellipsoid": ...
    @staticmethod
    def from_json(ellipsoid_json_str: str) -> "Ellipsoid": ...
    @staticmethod
    def from_name(ellipsoid_name: str, auth_name: str | None = None) -> "Ellipsoid": ...

class PrimeMeridian(_CRSParts):
    longitude: float
    unit_conversion_factor: str
    unit_name: str
    @staticmethod
    def from_authority(auth_name: str, code: int | str) -> "PrimeMeridian": ...
    @staticmethod
    def from_epsg(code: int | str) -> "PrimeMeridian": ...
    @staticmethod
    def from_string(prime_meridian_string: str) -> "PrimeMeridian": ...
    @staticmethod
    def from_json_dict(prime_meridian_dict: dict) -> "PrimeMeridian": ...
    @staticmethod
    def from_json(prime_meridian_json_str: str) -> "PrimeMeridian": ...
    @staticmethod
    def from_name(
        prime_meridian_name: str, auth_name: str | None = None
    ) -> "PrimeMeridian": ...

class Datum(_CRSParts):
    type_name: str
    @property
    def ellipsoid(self) -> Ellipsoid | None: ...
    @property
    def prime_meridian(self) -> PrimeMeridian | None: ...
    @staticmethod
    def from_authority(auth_name: str, code: int | str) -> "Datum": ...
    @staticmethod
    def from_epsg(code: int | str) -> "Datum": ...
    @staticmethod
    def from_string(datum_string: str) -> "Datum": ...
    @staticmethod
    def from_json_dict(datum_dict: dict) -> "Datum": ...
    @staticmethod
    def from_json(datum_json_str: str) -> "Datum": ...
    @staticmethod
    def from_name(datum_name: str, auth_name: str | None = None) -> "Datum": ...

class CoordinateSystem(_CRSParts):
    def __init__(self) -> None: ...
    @property
    def axis_list(self) -> Iterable[Axis]: ...
    @staticmethod
    def from_string(coordinate_system_string: str) -> "CoordinateSystem": ...
    @staticmethod
    def from_json_dict(coordinate_system_dict: dict) -> "CoordinateSystem": ...
    @staticmethod
    def from_json(coordinate_system_json_str: str) -> "CoordinateSystem": ...
    def to_cf(self, rotated_pole: bool = False) -> list[dict]: ...

class Param:
    name: str
    auth_name: str
    code: str
    value: str
    unit_conversion_factor: float
    unit_name: str
    unit_auth_name: str
    unit_code: str
    unit_category: str
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class Grid:
    short_name: str
    full_name: str
    package_name: str
    url: str
    direct_download: str
    open_license: str
    available: str
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class CoordinateOperation(_CRSParts):
    method_name: str
    method_auth_name: str
    method_code: str
    accuracy: float
    is_instantiable: bool
    has_ballpark_transformation: bool
    type_name: str
    @property
    def params(self) -> Iterable[Param]: ...
    @property
    def grids(self) -> Iterable[Grid]: ...
    @property
    def area_of_use(self) -> AreaOfUse | None: ...
    @property
    def towgs84(self) -> Iterable[float]: ...
    @property
    def operations(self) -> tuple["CoordinateOperation"]: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    @staticmethod
    def from_authority(auth_name: str, code: int | str) -> "CoordinateOperation": ...
    @staticmethod
    def from_epsg(code: int | str) -> "CoordinateOperation": ...
    @staticmethod
    def from_string(ellipsoid_string: str) -> "CoordinateOperation": ...
    @staticmethod
    def from_json_dict(ellipsoid_dict: dict) -> "CoordinateOperation": ...
    @staticmethod
    def from_json(ellipsoid_json_str: str) -> "CoordinateOperation": ...
    def to_proj4(self, version: ProjVersion | int = ProjVersion.PROJ_5) -> str: ...
    @staticmethod
    def from_name(
        coordinate_operation_name: str,
        auth_name: str | None = None,
        coordinate_operation_type: (
            CoordinateOperationType | str
        ) = CoordinateOperationType.CONVERSION,
    ) -> "CoordinateOperation": ...

class AuthorityMatchInfo(NamedTuple):
    auth_name: str
    code: str
    confidence: int

class _CRS(Base):
    srs: str
    type_name: str
    def __init__(self, proj_string: str) -> None: ...
    @property
    def ellipsoid(self) -> Ellipsoid | None: ...
    @property
    def area_of_use(self) -> AreaOfUse | None: ...
    @property
    def axis_info(self) -> list[Axis]: ...
    @property
    def prime_meridian(self) -> PrimeMeridian | None: ...
    @property
    def datum(self) -> Datum | None: ...
    @property
    def sub_crs_list(self) -> Iterable["_CRS"]: ...
    @property
    def source_crs(self) -> Optional["_CRS"]: ...
    @property
    def target_crs(self) -> Optional["_CRS"]: ...
    @property
    def geodetic_crs(self) -> Optional["_CRS"]: ...
    @property
    def coordinate_system(self) -> CoordinateSystem | None: ...
    @property
    def coordinate_operation(self) -> CoordinateOperation | None: ...
    def to_proj4(self, version: ProjVersion | int = ProjVersion.PROJ_5) -> str: ...
    def to_epsg(self, min_confidence: int = 70) -> int | None: ...
    def to_authority(self, auth_name: str | None = None, min_confidence: int = 70): ...
    def list_authority(
        self, auth_name: str | None = None, min_confidence: int = 70
    ) -> list[AuthorityMatchInfo]: ...
    def to_3d(self, name: str | None = None) -> "_CRS": ...
    def to_2d(self, name: str | None = None) -> "_CRS": ...
    @property
    def is_geographic(self) -> bool: ...
    @property
    def is_projected(self) -> bool: ...
    @property
    def is_vertical(self) -> bool: ...
    @property
    def is_bound(self) -> bool: ...
    @property
    def is_compound(self) -> bool: ...
    @property
    def is_engineering(self) -> bool: ...
    @property
    def is_geocentric(self) -> bool: ...
    def equals(self, other: Any, ignore_axis_order: bool) -> bool: ...
    @property
    def is_deprecated(self) -> bool: ...
    def get_non_deprecated(self) -> list["_CRS"]: ...

def is_proj(proj_string: str) -> bool: ...
def is_wkt(proj_string: str) -> bool: ...
def _load_proj_json(in_proj_json: str) -> dict: ...
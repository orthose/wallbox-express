from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict


def string_to_float(value: str) -> float:
    return float(value.replace(",", "."))

def string_to_datetime_hms(value: str) -> float:
    return datetime.strptime(value, "%H:%M:%S")


@dataclass
class ColumnHeader:
    initial_name: str
    target_name: str
    data_conv: Callable[[Any], Any]
    data_type: type


class WallboxSchema:
    LOCATION = ColumnHeader("Location", "LOCATION", str, str)
    CHARGER = ColumnHeader("Charger", "CHARGER", str, str)
    USER = ColumnHeader("User name", "USER", str, str)
    CHARGING_TIME = ColumnHeader("Charging time (h:m:s)", "CHARGING_TIME", string_to_datetime_hms, datetime)
    ENERGY = ColumnHeader("Energy (kWh)", "ENERGY", string_to_float, float)
    CURRENCY = ColumnHeader("Currency", "CURRENCY", str, str)
    SESSION_COST = ColumnHeader("Session cost", "COST", string_to_float, float)

    @classmethod
    def get_columns(cls):
        return [
            col for col in cls.__dict__.values()
            if isinstance(col, ColumnHeader)
        ]

mapping_columns: Dict[str, str] = {
    col.initial_name: col.target_name
    for col in WallboxSchema.get_columns()
}

schema_convs: Dict[str, Callable[[Any], Any]] = {
    col.target_name: col.data_conv 
    for col in WallboxSchema.get_columns()
}

schema_types: Dict[str, type] = {
    col.target_name: col.data_type
    for col in WallboxSchema.get_columns()
}

class WallboxColumns:
    @classmethod
    def init(cls):
        for k, v in WallboxSchema.__dict__.items():
            if isinstance(v, ColumnHeader):
                setattr(cls, k, v.target_name)

WallboxColumns.init()

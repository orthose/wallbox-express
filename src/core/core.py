from core.dataframe import DataFrame
from core.schema import mapping_columns, schema_convs, WallboxSchema


def load_data(csv_file: str) -> DataFrame:
    df = DataFrame()
    df.read_csv("tests/SessionsReport.csv")
    df.rename(mapping_columns)
    df.apply_schema(schema_convs)
    return df


def agg_user(df: DataFrame) -> DataFrame:
    add = lambda x, y: x + y
    df.group_by(
        group_cols=[
            WallboxSchema.CHARGER.target_name,
            WallboxSchema.USER.target_name,
        ],
        agg_cols={
            WallboxSchema.CHARGING_TIME.target_name: add,
            WallboxSchema.ENERGY.target_name: add,
            WallboxSchema.COST.target_name: add,
        }
    )
    return df


def agg_total(df: DataFrame) -> DataFrame:
    add = lambda x, y: x + y
    df.group_by(
        group_cols=[],
        agg_cols={
            WallboxSchema.CHARGING_TIME.target_name: add,
            WallboxSchema.ENERGY.target_name: add,
            WallboxSchema.COST.target_name: add,
        }
    )
    return df

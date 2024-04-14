from core.dataframe import DataFrame
from core.exceptions import WallboxSchemaError, WallboxCurrencyError
from core.schema import mapping_columns, schema_convs, WallboxSchema


def load_data(csv_file: str, currency: str) -> DataFrame:
    df = DataFrame()
    try:
        df.read_csv(csv_file)
        df.rename(mapping_columns)
        df.apply_schema(schema_convs)
    except Exception:
        raise WallboxSchemaError
    
    currency_index = df.headers[WallboxSchema.CURRENCY.target_name] 
    if not all([row[currency_index] == currency for row in df]):
        raise WallboxCurrencyError

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

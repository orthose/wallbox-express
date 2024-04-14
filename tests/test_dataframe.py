from core.dataframe import DataFrame
from core.schema import mapping_columns, schema_convs, schema_types, WallboxSchema

def test_init():
    df = DataFrame()
    assert len(df) == 0
    assert df.columns == []
    assert df.headers == {}

def test_read_csv():
    df = DataFrame()
    df.read_csv("tests/SessionsReport.csv")
    assert len(df) == 26
    assert len(df.columns) == 26
    assert len(set(df.columns) - set(df.headers.keys())) == 0
    for col, idx in df.headers.items():
        assert col == df.columns[idx]

def test_rename():
    df = DataFrame()
    df.read_csv("tests/SessionsReport.csv")
    assert "Location" in df.headers
    assert "Charging time (h:m:s)" in df.headers
    df.rename({
        "Location": "LOCATION",
        "Charging time (h:m:s)": "CHARGING_TIME"
    })
    assert "Location" not in df.headers
    assert "Charging time (h:m:s)" not in df.headers
    assert "LOCATION" in df.headers
    assert "CHARGING_TIME" in df.headers

def test_rename_mapping_columns():
    df = DataFrame()
    df.read_csv("tests/SessionsReport.csv")
    for col in mapping_columns.keys():
        assert col in df.headers
        assert col in df.columns
    df.rename(mapping_columns)
    for c1, c2 in mapping_columns.items():
        assert c1 not in df.headers
        assert c1 not in df.columns
        assert c2 in df.headers
        assert c2 in df.columns

def test_apply_schema():
    df = DataFrame()
    df.read_csv("tests/SessionsReport.csv")
    df.rename(mapping_columns)
    for row in df:
        for val in row:
            assert isinstance(val, str) 
    df.apply_schema(schema_convs)
    for row in df:
        assert len(row) == len(schema_convs)
        for i, val in enumerate(row):
            col = df.columns[i]
            if col in schema_convs:
                assert isinstance(val, schema_types[col])

def test_group_by():
    df = DataFrame()
    df.read_csv("tests/SessionsReport.csv")
    df.rename(mapping_columns)
    df.apply_schema(schema_convs)
    
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
    
    assert df.columns == [
        WallboxSchema.CHARGER.target_name,
        WallboxSchema.USER.target_name,
        WallboxSchema.CHARGING_TIME.target_name,
        WallboxSchema.ENERGY.target_name,
        WallboxSchema.COST.target_name,
    ]
    assert len(df) == 3

def test_group_by_without_group_cols():
    df = DataFrame()
    df.read_csv("tests/SessionsReport.csv")
    df.rename(mapping_columns)
    df.apply_schema(schema_convs)
    
    add = lambda x, y: x + y
    df.group_by(
        group_cols=[],
        agg_cols={
            WallboxSchema.CHARGING_TIME.target_name: add,
            WallboxSchema.ENERGY.target_name: add,
            WallboxSchema.COST.target_name: add,
        }
    )

    assert df.columns == [
        WallboxSchema.CHARGING_TIME.target_name,
        WallboxSchema.ENERGY.target_name,
        WallboxSchema.COST.target_name,
    ]
    assert len(df) == 1
 
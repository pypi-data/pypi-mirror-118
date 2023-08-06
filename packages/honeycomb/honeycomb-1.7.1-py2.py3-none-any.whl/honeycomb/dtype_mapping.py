from collections import OrderedDict
import logging

import pandas as pd
from pandas.core.dtypes.api import (is_datetime64_any_dtype,
                                    is_datetime64_dtype,
                                    is_datetime64tz_dtype)

"""
The pandas dtype 'timedelta64[ns]' can be mapped to the hive dtype 'INTERVAL',
but 'INTERVAL' is only available as a return value from querying - it cannot
be the dtype of a full column in a table. As a result, it is not included here

The pandas dtype 'category' is for categorical variables, but hive does not
have native support for categorical types. As a result, it is not included here
"""
dtype_map = {
    'object': 'COMPLEX',
    'int64': 'BIGINT',
    'float64': 'DOUBLE',
    'bool': 'BOOLEAN',
    'datetime64[ns]': 'TIMESTAMP',
    # Pandas 1.0 types
    'string': 'STRING',
    'Int8': 'BIGINT',
    'Int16': 'BIGINT',
    'Int32': 'BIGINT',
    'Int64': 'BIGINT',
    'UInt8': 'BIGINT',
    'UInt16': 'BIGINT',
    'UInt32': 'BIGINT',
    'UInt64': 'BIGINT',
    'boolean': 'BOOLEAN'
}


def convert_to_spec_timezones(df, datetime_cols, spec_timezones):
    """
    Converts any columns with an entry in 'spec_timezones' to that timezone

    Args:
        df (pd.DataFrame): Dataframe being operated on
        datetime_cols (list<str>): List of datetime columns in the dataframe
        spec_timezones (dict<str, str>):
            Dictionary from datetime columns to the timezone they
            represent. If the column is timezone-naive, it will have the
            timezone added to its metadata, leaving the times themselves
            unmodified. If the column is timezone-aware, the timezone
            will be converted, likely modifying the stored times.
    """
    if spec_timezones:
        for col, timezone in spec_timezones.items():
            if col not in datetime_cols:
                logging.warning(
                    'Column "{}" included in timezones dictionary '
                    'but is not present in the dataframe.'.format(col))
            # If datetime is timezone-aware, use tz_convert
            if is_datetime64tz_dtype(df.dtypes[col]):
                df[col] = df[col].dt.tz_convert(timezone)
            # Else, use tz_localize
            elif is_datetime64_dtype(df.dtypes[col]):
                df[col] = df[col].dt.tz_localize(timezone)


def make_datetimes_timezone_naive(df, datetime_cols, schema):
    """
    Makes all datetimes timezone-naive. This automatically converts them to
    UTC, while dropping the timezone from their metadata. All times in the lake
    will be in UTC - Hive has limited support for timezones by design - so
    having a notion of timezone is unnecessary.

    Args:
        df (pd.DataFrame): Dataframe being operated on
        datetime_cols (list<str>): List of datetime columns in the dataframe
        schema (str): The schema of the table the df is being uploaded to
    """
    for col in datetime_cols:
        if is_datetime64tz_dtype(df.dtypes[col]):
            df[col] = df[col].dt.tz_convert(None)
        elif schema != 'experimental':
            raise TypeError('All datetime columns in non-experimental tables '
                            'must be timezone-aware.')


def special_dtype_handling(df, spec_dtypes, spec_timezones, schema):
    """
    Wrapper around functions for special handling of specific dtypes

    Args:
        Universal:
            df (pd.DataFrame): Dataframe being operated on
            spec_dtypes (dict<str:np.dtype or str>):
                a dict from column names to dtypes
            schema (str): The schema of the table the df is being uploaded to
        For datetimes:
            spec_timezones (dict<str, str>):
                Dictionary from datetime columns to the timezone they
                represent. If the column is timezone-naive, it will have the
                timezone added to its metadata, leaving the times themselves
                unmodified. If the column is timezone-aware, the timezone
                will be converted, likely modifying the stored times.

    """
    df = apply_spec_dtypes(df, spec_dtypes)

    # All datetime columns, regardless of timezone naive/aware
    datetime_cols = [col for col in df.columns
                     if is_datetime64_any_dtype(df.dtypes[col])]

    convert_to_spec_timezones(df, datetime_cols, spec_timezones)
    make_datetimes_timezone_naive(df, datetime_cols, schema)

    return df


def apply_spec_dtypes(df, spec_dtypes):
    """
    Maps specified columns in a DataFrame to another dtype

    Args:
        df (pd.DataFrame): The DataFrame to perform casting on
        spec_dtypes (dict<str:np.dtype or str>):
            a dict from column names to dtypes
    Returns:
        df (pd.DataFrame): The DataFrame with casting applied
    Raises:
        TypeError: If casting 'df' to the new types fails
    """
    if spec_dtypes is not None:
        for col_name, new_dtype in spec_dtypes.items():
            if col_name.lower() not in df.dtypes.str.lower().keys():
                raise KeyError('Additional dtype casting failed: '
                               '\'{col_name}\' not in DataFrame.'.format(
                                   col_name=col_name))
            try:
                df[col_name] = df[col_name].astype(new_dtype)
            except TypeError as e:
                raise TypeError('Casting column \'{col_name}\' to type '
                                '\'{new_dtype}\' failed.'.format(
                                    col_name=col_name,
                                    new_dtype=new_dtype)) from e
    return df


def map_pd_to_db_dtypes(df, storage_type=None):
    """
    Creates a mapping from the dtypes in a DataFrame to their corresponding
    dtypes in Hive

    Args:
        df (pd.DataFrame): The DataFrame to pull dtypes from
        storage_type (string): The format the DataFrame is to be saved as
    Returns:
        db_dtypes (pd.Series): A Series mapping column names to database dtypes
    Raises:
        TypeError: If the DataFrame contains a column of type 'category'
        TypeError: If the DataFrame contains a column of type 'timedelta64[ns]'
        TypeError:
            If the DataFrame contains a column that translates to a complex
            Hive type, and is being saved as Avro or CSV
        TypeError:
            If the DataFrame contains a column that translates to an ARRAY
            Hive type, and is being saved as Parquet
    """
    if any(df.dtypes == 'category'):
        raise TypeError('Pandas\' \'categorical\' type is not supported. '
                        'Contact honeycomb devs for further info.')
    if any(df.dtypes == 'timedelta64[ns]'):
        raise TypeError('Pandas\' \'timedelta64[ns]\' type is not supported. '
                        'Contact honeycomb devs for further info.')

    # These refer to the pandas v1.0 dtypes, NOT the base Python types
    avro_disallowed_types = ['string', 'boolean']

    pd_v1_type_cols = df.columns[
        df.dtypes.astype(str).isin(avro_disallowed_types)]
    if storage_type == 'avro' and len(pd_v1_type_cols) > 0:
        raise TypeError(
            'The following columns are using Pandas v1.0 nullable-string '
            'or nullable-boolean dtypes, which are currently not supported '
            'when using the avro filetype.'
        )
    db_dtypes = df.dtypes.copy()

    for orig_type, new_type in dtype_map.items():
        # dtypes can be compared to their string representations for equality
        db_dtypes[db_dtypes == orig_type] = new_type

    # If any of the columns are of type 'object', they will be deemed complex
    # and will require additional processing.
    # Supported 'object' types are strings, lists, and dicts
    # (Lists and dicts can be arbitrarily nested)
    if any(db_dtypes.eq('COMPLEX')):
        complex_cols = db_dtypes.index[db_dtypes.eq('COMPLEX')]
        db_dtypes = handle_complex_dtypes(
            df[complex_cols], db_dtypes)

        if any(db_dtypes.str.contains('ARRAY|STRUCT')):
            # CSV support for arrays and structs is not currently implemented.
            if storage_type in ['csv']:
                raise TypeError('Complex types are not yet supported in '
                                'the {} storage format.'.format(storage_type))

    db_dtypes = db_dtypes.to_frame(name='dtype').reset_index().rename(
        columns={'index': 'col_name'})

    return db_dtypes


def handle_complex_dtypes(df_complex, db_dtypes):
    """
    Generates the DDL for columns with complex dtypes if they are found in
    a DataFrame that a table is being created from

    Args:
        df_complex (pd.DataFrame):
           DataFrame containing all the complex columns of the DataFrame that
           the new table is being generated from.
        db_dtypes (pd.Series): A Series mapping column names to database dtypes
    Returns:
        db_dtypes (pd.Series): A Series mapping column names to database dtypes
    """
    for col in df_complex.columns:
        reduced_type = reduce_complex_type(df_complex[col])
        if reduced_type == 'string':
            db_dtypes.loc[col] = 'STRING'
        elif reduced_type == 'numeric':
            db_dtypes.loc[col] = dtype_map['float64']
        elif reduced_type == 'bool':
            db_dtypes.loc[col] = dtype_map['bool']
        elif reduced_type == 'list':
            db_dtypes.loc[col] = handle_array_col(df_complex[col])
        elif reduced_type == 'dict':
            db_dtypes.loc[col] = handle_struct_col(df_complex[col])

    return db_dtypes


def reduce_complex_type(col):
    """
    Reduces the dtype of a complex column to a type usable in base Python.
    Considers every the type of every value in the column, and coalesces it
    to a specific, single type that captures all of them, then returns that
    type as a string.

    Args:
        col (pd.Series): A column with a complex dtype
    Returns:
        string: The reduced dtype of col
    Raises:
        TypeError: If the column is of a mixed or unsupported type
    """
    python_types = col.apply(type)
    if all(python_types.isin([str, type(None)])):
        return 'string'
    elif all(python_types.isin([list, type(None)])):
        return 'list'
    elif all(python_types.isin([dict, OrderedDict, type(None)])):
        return 'dict'
    elif all(python_types.isin([int, float, type(None)])):
        return 'numeric'
    elif all(python_types.isin([bool, type(None)])):
        return 'bool'
    else:
        raise TypeError(
            'Values passed to complex column "{}" are either of '
            'unsupported types of mixed types. Currently supported '
            'complex types are "STRING", "ARRAY" (list) and '
            '"STRUCT" (dictionary). Columns must contain '
            'homogenous types.'.format(col.name))


def handle_array_col(col):
    """
    Generates the DDL for a column of type ARRAY
    Can also be used to generate DDL for nested fields, such as for
    arrays contained within structs.

    Args:
        col (pd.Series): A column of the ARRAY dtype
    Returns:
        dtype_str (string): Hive DDL for the column
    """
    array_series = pd.Series(col[~col.isna()].sum())
    # Getting type of the items the array holds
    array_dtype = dtype_map[array_series.dtype.name]

    # If array's items are themselves a complex type
    if array_dtype == 'COMPLEX':
        reduced_type = reduce_complex_type(array_series)
        if reduced_type == 'string':
            array_dtype = 'STRING'

        # If the array itself holds arrays, handle the nested field(s) first
        elif reduced_type == 'list':
            array_dtype = handle_array_col(array_series)

        # If the array holds structs, handle the nested field(s) first
        elif reduced_type == 'dict':
            array_dtype = handle_struct_col(array_series)

    dtype_str = 'ARRAY <{}>'.format(array_dtype)
    return dtype_str


def handle_struct_col(col):
    """
    Generates the DDL for a column of type STRUCT
    Can also be used to generate DDL for nested fields, such as for
    structs contained within structs.

    Args:
        col (pd.Series): A column of the STRUCT dtype
    Returns:
        dtype_str (string): Hive DDL for the column
    """
    # Gets all structs (dicts) from non-null rows of the column
    struct_df = pd.DataFrame.from_records(
        col[~col.isna()].reset_index(drop=True))
    # Treat dicts as rows of a new data set, and map types for all subfields
    struct_dtypes = map_pd_to_db_dtypes(struct_df)

    dtype_str = 'STRUCT <{}>'.format(
        ', '.join(['{}: {}'.format(row['col_name'], row['dtype'])
                   for idx, row in struct_dtypes.iterrows()]))

    return dtype_str

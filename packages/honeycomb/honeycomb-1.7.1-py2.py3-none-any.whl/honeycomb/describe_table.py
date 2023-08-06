from honeycomb import hive, meta


def describe_table(table_name, schema=None,
                   include_metadata=False):
    """
    Retrieves the description of a specific table in hive

    Args:
        table_name (str): The name of the table to be queried
        schema (str): The name of the schema to search for the table in
        include_metadata (bool):
            Whether the returned DataFrame should contain just column names,
            types, and comments, or more detailed information such as
            storage location and type, partitioning metadata, etc.

    Returns:
        desc (pd.DataFrame): A dataframe containing descriptive information
            on the specified table
    """
    table_name, schema = meta.prep_schema_and_table(table_name, schema)

    # Presto does not support the 'FORMATTED' keyword, so
    # we're locking the engine for 'DESCRIBE' queries to Hive
    desc_query = 'DESCRIBE {formatted}{schema}.{table_name}'.format(
        formatted=('FORMATTED ' if include_metadata else ''),
        schema=schema,
        table_name=table_name)
    desc = hive.run_lake_query(desc_query, engine='hive')

    if include_metadata:
        desc = desc.loc[1:].reset_index(drop=True)
    return desc

# connections_setup.py

from airflow.hooks.base_hook import BaseHook

# PostgreSQL Connection
pg_conn = {
    'conn_id': 'postgres_conn_id',
    'conn_type': 'postgres',
    'host': 'your_postgres_host',
    'schema': 'public',
    'login': 'your_postgres_username',
    'password': 'your_postgres_password',
    'port': 5432,
}
BaseHook.get_connection('postgres_conn_id').set_parameters(**pg_conn)

# Redshift Connection
redshift_conn = {
    'conn_id': 'redshift_conn_id',
    'conn_type': 'postgres',
    'host': 'your_redshift_cluster_name.xxxxxxx.us-west-2.redshift.amazonaws.com',
    'schema': 'public',
    'login': 'your_redshift_username',
    'password': 'your_redshift_password',
    'port': 5439,
}
BaseHook.get_connection('redshift_conn_id').set_parameters(**redshift_conn)

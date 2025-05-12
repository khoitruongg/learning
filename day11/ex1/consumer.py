from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.datastream import StreamExecutionEnvironment

def create_kafka_source_table(table_env):
    # Create Kafka source table
    table_env.execute_sql("""
        CREATE TABLE kafka_source (
            `key` STRING,
            `value` STRING
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'flink-topic',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'flink-group',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json',
            'json.ignore-parse-errors' = 'true'
        );
    """)

    print("Kafka source table created.")

def export_to_csv(table_env):
    # Create a FileSink to write to a CSV file using the 'filesystem' connector
    table_env.execute_sql("""
        CREATE TABLE file_sink (
            `key` STRING,
            `value` STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'file://./output/',
            'format' = 'csv',
            'csv.field-delimiter' = ',',
            'csv.ignore-parse-errors' = 'true'
        );
    """)

    print("File sink created.")

    # Insert data from kafka_source to the file_sink
    table_env.execute_sql("""
        INSERT INTO file_sink
        SELECT `key`, `value` FROM kafka_source
    """)
    print("Inserted data.")

def debug_table(table_env):
    table_env.execute_sql("""
    CREATE TABLE print_sink (
        `key` STRING,
        `value` STRING
    ) WITH (
        'connector' = 'print'
    );
    """)

    table_env.execute_sql("""
        INSERT INTO print_sink
        SELECT `key`, `value` FROM kafka_source
    """)


def main():
    # Create the StreamExecutionEnvironment and StreamTableEnvironment
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.in_streaming_mode()
    table_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # Set up Kafka source table
    create_kafka_source_table(table_env)

    # Export data to CSV
    export_to_csv(table_env)
    debug_table(table_env)

if __name__ == '__main__':
    main()

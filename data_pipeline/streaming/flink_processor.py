from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

class FlinkProcessor:
    def __init__(self):
        self.env = StreamExecutionEnvironment.get_execution_environment()
        self.settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
        self.t_env = StreamTableEnvironment.create(self.env, environment_settings=self.settings)

    def process_stream(self, input_topic, output_topic, processing_function):
        self.t_env.execute_sql(f"""
            CREATE TABLE input_table (
                message STRING
            ) WITH (
                'connector' = 'kafka',
                'topic' = '{input_topic}',
                'properties.bootstrap.servers' = 'localhost:9092',
                'format' = 'json'
            )
        """)

        self.t_env.execute_sql(f"""
            CREATE TABLE output_table (
                processed_message STRING
            ) WITH (
                'connector' = 'kafka',
                'topic' = '{output_topic}',
                'properties.bootstrap.servers' = 'localhost:9092',
                'format' = 'json'
            )
        """)

        input_table = self.t_env.from_path("input_table")
        result_table = input_table.map(processing_function).alias("processed_message")
        result_table.execute_insert("output_table").wait()

# Uso:
# def process_message(message):
#     return message.upper()
# 
# flink_processor = FlinkProcessor()
# flink_processor.process_stream("input-topic", "output-topic", process_message)
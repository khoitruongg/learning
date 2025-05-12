from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream.connectors import FlinkKafkaConsumer
import jpype

def set_up_JVM():
     # Start JVM with the necessary arguments to allow access to URLClassLoader
    jvm_path = "/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home/lib/server/libjvm.dylib"
    # Ensure that JVM is started before using Java classes
    if not jpype.isJVMStarted():
        try:
            # Start the JVM with necessary parameters
            jpype.startJVM(
                jvm_path,
                "--add-opens", "java.base/java.net=ALL-UNNAMED",
                "--illegal-access=permit"
            )
        except Exception as e:
            print(f"Error starting JVM: {e}")
            return

    from java.util import Properties
    from org.apache.flink.streaming.connectors.kafka import FlinkKafkaConsumer

def main():
    
    set_up_JVM()

    # 1. Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # Add Kafka connector and Kafka client JARs to the environment
    env.add_jars("file:///Users/khoitm/Projects/docker/lib-jar/flink-connector-kafka-1.17.1.jar")
    env.add_jars("file:///Users/khoitm/Projects/docker/lib-jar/kafka-clients-3.9.0.jar") 

    # 2. Kafka connection properties
    kafka_props = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "flink-py-consumer"
    }

    # 3. Create Kafka Consumer using PyFlink connector
    kafka_consumer = FlinkKafkaConsumer(
        topics='flink-topic',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    # 4. Add Kafka source
    data_stream = env.add_source(kafka_consumer).returns(Types.STRING())

    # 5. Print consumed messages
    data_stream.print()

    # 6. Execute the job
    env.execute("Kafka Consumer with PyFlink")

if __name__ == "__main__":
    main()

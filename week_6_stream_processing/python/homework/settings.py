INPUT_DATA_PATH = '../resources/fhv_tripdata_2019-03.csv'

RIDE_KEY_SCHEMA_PATH = '../resources/schemas/fhv_ride_key.avsc'
RIDE_VALUE_SCHEMA_PATH = '../resources/schemas/fhv_ride_value.avsc'

SCHEMA_REGISTRY_URL = 'http://schema-registry:8081'
BOOTSTRAP_SERVERS = 'broker:29092'
KAFKA_TOPIC = 'fhv_rides_avro'
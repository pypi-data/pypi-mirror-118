import os

DEBUG = bool(int(os.environ.get("DEBUG", False)))
SPAN_SAMPLE_RATE = float(os.environ.get("SPAN_SAMPLE_RATE", "0.1"))
SHUTDOWN_GRACE_PERIOD = int(os.environ.get("SHUTDOWN_GRACE_PERIOD", "30"))

MQ_HOST = os.environ.get('MQ_HOST', "localhost")
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME', "admin")
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', "pswd")
MQ_PORT = os.environ.get('MQ_PORT', 5672)
MQ_RETRY = int(os.environ.get('MQ_RETRY', 2))

REDIS_HOST = os.environ.get('REDIS_HOST', "localhost")
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

MAIN_EXCHANGE_NAME: str = os.environ.get('MAIN_EXCHANGE_NAME', "quru_main")
RPC_EXCHANGE_NAME = os.environ.get('RPC_EXCHANGE_NAME', "quru_rpc")
BROADCAST_EXCHANGE_NAME = os.environ.get('BROADCAST_EXCHANGE_NAME', "quru_bd")

TRACING_HOST = os.environ.get("TRACING_HOST", "localhost")
TRACING_SPAN_PORT = os.environ.get("TRACING_SPAN_PORT", 9411)

ZIPKIN_ADDR = "http://{}:{}/api/v2/spans".format(
    TRACING_HOST, TRACING_SPAN_PORT)

# RPC config
PPL_RPC_TIMEOUT = 100000 if not DEBUG else -1  # ms
DIR_RPC_TIMEOUT = int(os.environ.get("DIR_RPC_TIMEOUT", 500))

# Raft config
HEARTBEAT_INTERVAL = 15 * DIR_RPC_TIMEOUT  # ms

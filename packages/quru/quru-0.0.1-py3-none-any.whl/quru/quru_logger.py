import logging.config

import structlog
from aiozipkin.span import SpanAbc

from .env import DEBUG
import chardet


_UNUSED_LOG_ENTRY = set([
    "span",
    "event",
    "level",
    "timestamp"
])


timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
pre_chain = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    timestamper,
]


def proc_span(logger, method_name, event_dict):
    """
    Add the log level to the event dict.
    """
    if "span" in event_dict[0][0]:
        span = event_dict[0][0]['span']
        if isinstance(span, SpanAbc):
            span_annotation = event_dict[0][0]['event']
            for k, v in event_dict[0][0].items():
                if k not in _UNUSED_LOG_ENTRY:
                    span_annotation += " {}={}".format(k, v)
            span.annotate(span_annotation)
        event_dict[0][0].pop("span")
    return event_dict


logging.getLogger("pika").setLevel(logging.WARNING)
logging.getLogger("aio_pika").setLevel(logging.WARNING)
LOGGER_LEVEL = "DEBUG" if DEBUG else "INFO"

logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=False),
                "foreign_pre_chain": pre_chain,
            },
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=False),
                "foreign_pre_chain": pre_chain,
            },
        },
        "handlers": {
            "default": {
                "level": LOGGER_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "colored",
            },
            # "file": {
            #     "level": "DEBUG",
            #     "class": "logging.handlers.WatchedFileHandler",
            #     "filename": "test.log",
            #     "formatter": "plain",
            # },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": True,
            },
        }
})

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        proc_span
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logging.getLogger("chardet").setLevel(logging.INFO)
logging.getLogger("py4j").setLevel(logging.INFO)

logger = structlog.getLogger()

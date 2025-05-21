from flask import request, Response
import traceback
import logging
import os
from functools import wraps
from datetime import datetime
from opencensus.ext.azure.log_exporter import AzureLogHandler


class UnifiedLogger:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        connection_string = os.getenv('APPINSIGHTS_CONNECTION_STRING')
        if connection_string:
            azure_handler = AzureLogHandler(connection_string=connection_string)
            self.logger.addHandler(azure_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
        )
        self.logger.addHandler(stream_handler)

    def log_message(self, event_type: str, message: str, severity: str, custom_dimensions=None):
        custom_dimensions = custom_dimensions or {}
        custom_dimensions.update({
            'service_name': self.service_name,
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat()
        })

        log_method = getattr(self.logger, severity.lower(), self.logger.info)
        log_method(message, extra={'custom_dimensions': custom_dimensions})

    def log_request(self, event_name: str, status_code: int = None):
        self.log_message(
            event_type=event_name,
            message=f"{event_name} - {request.method} {request.path} [{status_code or 'unknown'}]",
            severity="INFO" if status_code and 200 <= status_code < 400 else "ERROR",
            custom_dimensions={
                "method": request.method,
                "url": request.url,
                "endpoint": request.path,
                "remote_addr": request.remote_addr,
                "headers": dict(request.headers),
                "cookies": request.cookies,
                "args": request.args.to_dict(),
                "json": request.get_json(silent=True),
                "status_code": status_code,
            }
        )

    def log_exception(self, error: Exception, event_name="UnhandledException"):
        self.logger.exception(f"{event_name}: {error}", extra={
            'custom_dimensions': {
                'service_name': self.service_name,
                'timestamp': datetime.now().isoformat(),
                'traceback': traceback.format_exc()
            }
        })


def log_event(service_name: str, event_base: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = UnifiedLogger(service_name)
            logger.log_request(f"{event_base}Attempt")

            try:
                response = func(*args, **kwargs)

                # Try to extract status code
                if isinstance(response, tuple):
                    # Flask pattern: return data, status_code
                    status_code = response[1]
                elif isinstance(response, Response):
                    status_code = response.status_code
                else:
                    status_code = 200  # fallback

                event_type = f"{event_base}Success" if 200 <= status_code < 400 else f"{event_base}Failure"
                logger.log_request(event_type, status_code)
                return response

            except Exception as e:
                logger.log_exception(e, f"{event_base}Failure")
                raise

        return wrapper
    return decorator

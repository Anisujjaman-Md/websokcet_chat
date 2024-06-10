import logging
import time
from django.utils import timezone
import sys


log_file_path = 'app.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create a stream handler for console output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.ERROR)  # Only show ERROR or higher messages in the console
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Record the start time of the request processing
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        # Record the end time of the request processing
        end_time = time.time()

        # Calculate the total time taken for the request
        elapsed_time = end_time - start_time

        # Customize log message based on severity level
        if response.status_code >= 500:
            log_level = logging.ERROR
            log_message = "Server Error"
        elif response.status_code >= 400:
            log_level = logging.WARNING
            log_message = "Client Error"
        else:
            log_level = logging.INFO
            log_message = "Success"

        # Log request details
        logger.log(
            log_level,
            f"Method: {request.method}, "
            f"Path: {request.path}, "
            f"Status Code: {response.status_code}, "
            f"Time Taken: {elapsed_time:.2f}s, "
            f"Message: {log_message}, "
            f"Timestamp: {timezone.now()}"
        )

        return response
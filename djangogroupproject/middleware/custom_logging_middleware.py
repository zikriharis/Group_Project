from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class CustomLoggingMiddleware(MiddlewareMixin):
    """
    Example middleware to log each incoming request's method, path, and user.
    """

    def process_request(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"Request: {request.method} {request.path} | User: {user}")
        # Example: add custom request attribute
        request.custom_logged = True

    def process_response(self, request, response):
        # Add a custom header for demonstration
        response['X-Custom-Logged'] = '1'
        return response
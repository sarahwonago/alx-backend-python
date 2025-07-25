from datetime import datetime, time
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("requests.log", "a") as logfile:
            logfile.write(log_entry)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start = time(18, 0)  # 6:00 PM
        end = time(21, 0)  # 9:00 PM

        # Only restrict /api or /chats endpoints (optional)
        if request.path.startswith("/api") or request.path.startswith("/chats"):
            if not (start <= now <= end):
                return HttpResponseForbidden(
                    "Access to chats is only allowed between 6PM and 9PM."
                )

        return self.get_response(request)

from datetime import datetime, time
from django.http import HttpResponseForbidden
from collections import defaultdict
from datetime import datetime


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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = defaultdict(list)  # {ip: [timestamp1, timestamp2, ...]}
        self.limit = 5  # max requests
        self.time_window = 60  # seconds

    def __call__(self, request):
        # Only monitor POST requests to message endpoints
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_ip(request)
            now = time.time()

            # Remove timestamps older than 60 seconds
            self.request_log[ip] = [
                timestamp
                for timestamp in self.request_log[ip]
                if now - timestamp < self.time_window
            ]

            if len(self.request_log[ip]) >= self.limit:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")

            self.request_log[ip].append(now)

        return self.get_response(request)

    def get_ip(self, request):
        # Use X-Forwarded-For if behind a proxy
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to protected paths (e.g., chats/messages)
        protected_paths = ["/messages", "/conversations"]

        if any(path in request.path for path in protected_paths):
            user = request.user
            if user.is_authenticated:
                user_role = getattr(user, "role", None)
                if user_role not in ["admin", "moderator"]:
                    return HttpResponseForbidden(
                        "You do not have permission to perform this action."
                    )
            else:
                return HttpResponseForbidden("Authentication required.")

        return self.get_response(request)

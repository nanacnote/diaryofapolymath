import os


class GoatcounterAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if "text/html" in response.get("Content-Type", ""):
            goatcounter_url = os.environ.get("GOATCOUNTER_DOMAIN_NAME")
            script = (
                "<script "
                f'data-goatcounter="http://{goatcounter_url}/count" '
                f'async src="//{goatcounter_url}/count.js"></script>'
            )
            closing_body_index = response.content.find(b"</body>")
            if closing_body_index != -1:
                response.content = (
                    response.content[:closing_body_index]
                    + script.encode()  # noqa: W503
                    + response.content[closing_body_index:]  # noqa: W503
                )
        return response


class SessionThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        theme = request.GET.get("theme")
        if theme in ["light", "dark"]:
            request.session["theme"] = theme
        return self.get_response(request)

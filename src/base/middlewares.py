import os


# TODO: test coverage
class GoatcounterAnalyticsMiddleware:  # pragma: no cover
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
        color_scheme = request.headers.get("Sec-CH-Prefers-Color-Scheme")
        if color_scheme in ["light", "dark"]:
            request.color_scheme = color_scheme

        theme = request.GET.get("theme")
        if theme in ["light", "dark"]:
            request.session["theme"] = theme

        response = self.get_response(request)

        response["Accept-CH"] = "Sec-CH-Prefers-Color-Scheme"
        response["Critical-CH"] = "Sec-CH-Prefers-Color-Scheme"
        response["Vary"] = "Sec-CH-Prefers-Color-Scheme"
        response["Permissions-Policy"] = "ch-prefers-color-scheme=(self)"

        return response

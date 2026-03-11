def session_theme_processor(request):
    session_theme = request.session.get("theme", "light")
    return {"session_theme": session_theme}


def copy_processor(request):
    return {
        "copy": {
            "site_name": "Diary of a Polymath",
            "site_description": "",
        }
    }

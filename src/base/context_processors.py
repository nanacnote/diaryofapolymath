def session_theme_processor(request):
    session_theme = request.session.get("theme", "light")
    return {"session_theme": session_theme}


def copy_processor(request):
    return {
        "copy": {
            "meta_site_name": "Diary of a Polymath",
            "meta_site_description": "",
            "nav_about": "About",
            "nav_blog": "Blog",
            "nav_exclusive": "Exclusive",
            "footer_powered_by": "Powered by",
        }
    }

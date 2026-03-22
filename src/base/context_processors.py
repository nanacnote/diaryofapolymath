def session_theme_processor(request):
    color_scheme = getattr(request, "color_scheme", "light")
    session_theme = request.session.get("theme", color_scheme)
    return {"session_theme": session_theme}


def copy_processor(request):
    return {
        "copy": {
            "meta_site_name": "Diary of a Polymath",
            "meta_site_description": "A personal knowledge journal and publishing space.",
            "nav_about": "About",
            "nav_blog": "Blog",
            "nav_exclusive": "Exclusive",
            "common_powered_by": "Powered by",
            "common_tagged": "Tagged",
            "common_archived": "Archived",
            "common_shared_by": "Shared by",
            "common_like": "Like",
            "common_comment": "Comment",
            "common_copy_link": "Copy link",
        }
    }

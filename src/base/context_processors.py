def session_theme_processor(request):
    session_theme = request.session.get("theme", "light")
    return {"session_theme": session_theme}

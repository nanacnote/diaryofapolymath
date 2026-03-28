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
            "common_tags": "Tags",
            "common_tagged": "Tagged",
            "common_archive": "Archive",
            "common_archived": "Archived",
            "common_pinned": "Pinned",
            "common_shared_by": "Shared by",
            "common_like": "Like",
            "common_copy_link": "Copy link",
            "common_image_of_sponsor": "Image of sponsor",
            "common_reply": "Reply",
            "common_submit": "Submit",
            "common_cancel": "Cancel",
            "common_upvote": "Upvote",
            "common_submit_comment": "Submit Comment",
            "common_comment": "Comment",
            "common_comments": "Comments",
            "common_leave_a_comment": "Leave a comment",
            "common_no_comments_yet": "No comments yet",
            "common_be_the_first_to_comment": "Be the first to comment!",
            "common_comment_submitted_message": "Thank you — your comment has been submitted and is pending review."
        }
    }

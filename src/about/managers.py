from django.contrib.auth.models import UserManager


class ProfileManager(UserManager):
    def get_profile_links_timelines_for_superuser(self):
        profile = self.prefetch_related("link_set", "timeline_set").get(
            is_superuser=True
        )
        links = profile.link_set.all()
        timelines = profile.timeline_set.all()
        return (profile, links, timelines)

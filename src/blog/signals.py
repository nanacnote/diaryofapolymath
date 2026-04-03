from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from base.integrations.matrix.notifier import notify_new_comment

from .models import Comment


@receiver(post_save, sender=Comment)
def on_comment_saved(sender, instance, created, raw, **kwargs):
    if raw or not created:
        return

    # Fire only once the DB transaction commits successfully.
    transaction.on_commit(lambda: notify_new_comment.delay(instance.pk))

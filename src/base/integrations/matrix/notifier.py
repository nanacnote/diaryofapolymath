import logging
import os
from configparser import ConfigParser

from asgiref.sync import async_to_sync
from celery import shared_task
from mautrix.client import Client
from mautrix.types import RoomID

logger = logging.getLogger(__name__)


class MatrixNotifier:  # pragma: no cover
    def __init__(self):
        self._enabled = bool(
            ConfigParser.BOOLEAN_STATES[
                os.environ.get("MATRIX_NOTIFIER_ENABLED", "true").strip().lower()
            ]
        )
        self._base_url = (os.environ.get("MATRIX_BASE_URL") or "").strip()
        self._access_token = (os.environ.get("MATRIX_ACCESS_TOKEN") or "").strip()
        self._room_id = (os.environ.get("MATRIX_ROOM_ID") or "").strip()

        if self._enabled and not all([self._base_url, self._access_token, self._room_id]):
            raise RuntimeError(
                "Matrix notifier is enabled but one or more required environment variables are "
                "missing: MATRIX_BASE_URL, MATRIX_ACCESS_TOKEN, MATRIX_ROOM_ID"
            )

    def send(self, message):
        if not self._enabled:
            logger.debug("Matrix notifier is disabled; skipping message send")
            return False
        return async_to_sync(self.send_async)(message)

    async def send_async(self, message):
        if not self._enabled:
            return False

        client = Client(base_url=self._base_url, token=self._access_token)
        try:
            await client.send_text(RoomID(self._room_id), message)
        finally:
            await client.api.session.close()
        return True


@shared_task(autoretry_for=(Exception,), max_retries=2, retry_backoff=True)
def notify_new_comment(comment_id):  # pragma: no cover
    """Send a Matrix notification for a newly created comment."""
    from blog.models import Comment

    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        logger.warning(f"notify_new_comment: comment {comment_id} not found")
        return

    commenter = (comment.name or comment.email or "Unknown").strip()
    content = (comment.content or "").strip()
    MatrixNotifier().send(f"New comment received\nAuthor: {commenter}\nMessage: {content}")

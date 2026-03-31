import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore

from mautrix.client import Client
from mautrix.types import RoomID

logger = logging.getLogger(__name__)

# Module-level thread pool shared across all MatrixNotifier instances
_EXECUTOR = ThreadPoolExecutor(max_workers=3)
_PENDING_SLOTS = BoundedSemaphore(100)


# TODO: test coverage
class MatrixNotifier:  # pragma: no cover
    def __init__(self):
        self.base_url = os.environ.get("MATRIX_BASE_URL")
        self.access_token = os.environ.get("MATRIX_ACCESS_TOKEN")
        self.room_id = os.environ.get("MATRIX_ROOM_ID")

        if not all([self.base_url, self.access_token, self.room_id]):
            raise RuntimeError("MatrixNotifier missing required environment variables!")

    def send(self, message):
        if not _PENDING_SLOTS.acquire(blocking=False):
            logger.warning("Dropping Matrix notification: pending queue is full")
            return

        async def _send_async():
            client = Client(base_url=self.base_url, token=self.access_token)
            await client.send_text(RoomID(str(self.room_id)), message)

        def _runner():
            asyncio.run(_send_async())

        try:
            future = _EXECUTOR.submit(_runner)
        except Exception:
            _PENDING_SLOTS.release()
            raise

        def _on_done(done_future):
            _PENDING_SLOTS.release()
            exc = done_future.exception()
            if exc is not None:
                logger.exception(f"Failed to send Matrix notification: {exc}")

        future.add_done_callback(_on_done)


def notify_new_comment(comment):  # pragma: no cover
    """Send a Matrix notification for a new comment"""
    if os.environ.get("APP_ENV") == "production":
        try:
            MatrixNotifier().send(
                f"New comment by \n"
                f"{comment.name or comment.email}: \n"
                f"{comment.content[:255]}"
            )
        except Exception:
            logger.exception("Failed to send Matrix comment notification")

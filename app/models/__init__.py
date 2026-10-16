from app.models.user import User
from app.models.announcement import Announcement

# Export the models so they can be imported as app.models.User and app.models.Announcement.
__all__ = ["User", "Announcement"]

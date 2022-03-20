from django.conf import settings
static = settings.STATIC_URL
from .Global import data as global_data

data = {
    **global_data,
}
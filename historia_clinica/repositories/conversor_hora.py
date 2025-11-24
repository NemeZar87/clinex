from django.conf import settings
from django.utils import timezone



# --- helper para convertir a aware si es necesario ---
def make_aware_if_needed(dt):
    if settings.USE_TZ:
        if timezone.is_naive(dt):
            return timezone.make_aware(dt, timezone.get_default_timezone())
    return dt
from django.conf import settings


def admin_portal_url(request):
    return {"ADMIN_PORTAL_URL": settings.ADMIN_PORTAL_URL}

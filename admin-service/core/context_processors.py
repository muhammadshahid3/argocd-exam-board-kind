from django.conf import settings


def student_portal_url(request):
    return {"STUDENT_PORTAL_URL": settings.STUDENT_PORTAL_URL}

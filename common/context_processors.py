from django.conf import settings

from apps.core.models import EduProcess, SiteContent


def getting_info(request):
    style_core_version = settings.STYLE_CORE_VERSION
    style_responsive_version = settings.STYLE_RESPONSIVE_VERSION
    edu_processes = EduProcess.active.all()
    CONTACTS = settings.CONTACTS
    site_content = {c.key: c.value for c in SiteContent.objects.all()}
    return locals()

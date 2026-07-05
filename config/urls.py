from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from communication.views import AnnouncementViewSet
from core.views import OrganizationViewSet
from events.views import AttendanceViewSet, EventViewSet
from finance.views import ContributionViewSet
from members.views import FamilyViewSet, MemberViewSet


def home_view(request):
    return HttpResponse("PIGOE is running", content_type="text/plain")


# API First (ADR-0002) — un ViewSet DRF par modèle métier, exposé sous /api/v1/
router = DefaultRouter()
router.register("organizations", OrganizationViewSet)
router.register("families", FamilyViewSet)
router.register("members", MemberViewSet)
router.register("contributions", ContributionViewSet)
router.register("events", EventViewSet)
router.register("attendances", AttendanceViewSet)
router.register("announcements", AnnouncementViewSet)


urlpatterns = [
    path("", home_view, name="home"),
    path("health/", lambda request: HttpResponse("ok", content_type="text/plain"), name="health"),
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    # Allauth — authentification sociale OAuth2 (ADR-0004)
    # Expose : /accounts/login/, /accounts/logout/,
    #           /accounts/google/login/, /accounts/google/login/callback/
    path("accounts/", include("allauth.urls")),
]

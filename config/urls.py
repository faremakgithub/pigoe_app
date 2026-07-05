from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def home_view(request):
    return HttpResponse("PIGOE is running", content_type="text/plain")


urlpatterns = [
    path("", home_view, name="home"),
    path("health/", lambda request: HttpResponse("ok", content_type="text/plain"), name="health"),
    path("admin/", admin.site.urls),
    # Allauth — authentification sociale OAuth2 (ADR-0004)
    # Expose : /accounts/login/, /accounts/logout/,
    #           /accounts/google/login/, /accounts/google/login/callback/
    path("accounts/", include("allauth.urls")),
]

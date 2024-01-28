# Django
from django.urls import include, path

# DRF
from rest_framework.routers import DefaultRouter

# Api Views
from .api.v1.views import NewsletterViewSet
# It's creating a router object that will be used to register the viewsets.
router = DefaultRouter()

router.register("newsletter", NewsletterViewSet, basename="newsletter")


urlpatterns = [
    path("", include(router.urls)),
]

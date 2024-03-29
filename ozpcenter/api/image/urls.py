"""
Urls
"""
from django.conf.urls import url, include
from rest_framework import routers

import ozpcenter.api.image.views as views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'image', views.ImageViewSet, base_name='image')
router.register(r'imagetype', views.ImageTypeViewSet, base_name='imagetype')

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^', include(router.urls)),
]
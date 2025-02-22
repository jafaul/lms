"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config.settings import base

api_urls = [
    path('courses/', include("apps.management.api_urls")),
    path('courses/<int:pk>/tasks/<int:pktask>/', include("apps.assessment.api_urls")),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls', namespace='home')),
    path('courses/', include('apps.management.urls', namespace='management')),
    path('accounts/', include('apps.authentication.urls', namespace='authentication')),
    path('tinymce/', include('tinymce.urls')),
    path('courses/<int:pk>/tasks/<int:pktask>/', include('apps.assessment.urls', namespace='assessment')),
    path('', include('social_django.urls', namespace='social')),

    path('api/', include(api_urls)),

] + static(base.MEDIA_URL, document_root=base.MEDIA_ROOT) \
    + static(base.STATIC_URL, document_root=base.STATIC_ROOT)


if base.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()




# todo https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Sessions
# todo try to do data migrations (DML) while dividing app for a few new apps
# todo https://www.geeksforgeeks.org/software-engineering-coupling-and-cohesion/ ; two scoops of django
# todo check pbkdf2 storage password standard; c
# todo книжка искусство джанго
# todo check oauth2, jwt
# todo dive deeper into celery, celery beat, celery beat for task with course data, celery results, caching with redis
# todo check AJAX, GraphQL, jQuery
# todo high scalability .com site to research microservices examples

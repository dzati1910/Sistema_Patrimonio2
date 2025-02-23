from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    # ... other URLs ...
    path("api/", include("config.urls")),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('contacts/',include('contacts.urls')),
    path("assets/", include("assets.urls")),
    path('maintenance/',include('maintenance.urls')),
    path('movements/', include('movements.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

]
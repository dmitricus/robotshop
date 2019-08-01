from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
import mainapp.views as mainapp
from django.conf.urls.static import static
from django.conf.urls import include


from django.conf import settings


urlpatterns = [
    url(r'^$', mainapp.main, name='main'),
    url(r'^catalog/',  include('mainapp.urls', namespace='catalog')),
    url(r'^contacts/$', mainapp.contacts, name='contacts'),
    url(r'^auth/', include('authapp.urls', namespace='auth')),
    url(r'^basket/', include('basketapp.urls', namespace='basket')),
    url(r'^admin/', include('adminapp.urls', namespace='admin')),
    #url(r'^admin/', admin.site.urls),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico'), name='favicon'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
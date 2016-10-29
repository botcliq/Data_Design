from django.conf.urls import patterns, include, url, RedirectView

from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/', inclulde('catalog.urls')),
    url(r'^$', RedirectView.as_view(url='/catalog/', permaanent=True)),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
)

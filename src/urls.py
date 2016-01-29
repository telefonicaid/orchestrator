from django.conf.urls import url, include, patterns

urlpatterns = patterns('',
    url(r'^v1.0/', include('orchestrator.api.urls')),
)

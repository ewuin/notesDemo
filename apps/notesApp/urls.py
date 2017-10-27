from django.conf.urls import url
from . import views           # This line is new!


urlpatterns = [
    url(r'^$',views.table),
    url(r'^select_page$',views.select_page),
    url(r'^add2$',views.add2),
    url(r'^refresh_pagination$',views.refresh_pagination),
    url(r'^update_note$',views.update_note),
    url(r'^delete2$',views.delete2),
    url(r'^from_date$',views.from_date),
    url(r'^to_date$',views.to_date),
    ]

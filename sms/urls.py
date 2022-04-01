from django.urls import path
from sms.views.list_views import *

app_name = 'sms'

urlpatterns = [
    # views
    path('list/', \
        SmsListView.as_view(), \
        name='sms-list'),
]
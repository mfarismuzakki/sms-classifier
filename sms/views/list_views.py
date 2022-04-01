from django.shortcuts import render
from django.views.generic import View


class SmsListView(View):
    @classmethod
    def get(cls, request):
        context = {

        }

        return render(request, 'sms/messages/list.html', context)

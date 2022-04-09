from django.shortcuts import render
from django.views.generic import View
from sms.apis.sms_apis import SmsApi

class SmsListView(View):
    @classmethod
    def get(cls, request):
        user_id = request.GET['user_id']
        target_id = request.GET.get('target_id')

        phone_number_list, sms_list, target_number = SmsApi.get_group_list(user_id, target_id)
        
        context = {
            'phone_number_list' : phone_number_list,
            'sms_list' : sms_list,
            'target_number' : target_number,
        }

        return render(request, 'sms/messages/list.html', context)
    
    @classmethod
    def post(cls, request):

        recipient_number = request.POST['recipient']
        sender_id = request.GET['user_id']
        message = request.POST['message']

        target_id = SmsApi.store_message(sender_id, recipient_number, message)
        
        user_id = request.GET['user_id']
        phone_number_list, sms_list, target_number = SmsApi.get_group_list(user_id, target_id)
        
        context = {
            'phone_number_list' : phone_number_list,
            'sms_list' : sms_list,
            'target_number' : target_number,
        }

        return render(request, 'sms/messages/list.html', context)

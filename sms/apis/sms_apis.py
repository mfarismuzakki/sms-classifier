from django.views.generic import View
from django.db.models import Q
from django.utils import timezone

from user.models import *
from sms.models import *

class SmsApi(View):
    @classmethod
    def get_group_list(cls, user_id, target_id):
        """
        mendapatkan list grup sms
        """
        user_id = int(user_id)

        # filter
        filter = Q(sender_id=user_id) | Q(recipient_id=user_id) 

        sms_list = \
            Sms.objects \
                .filter(filter) \
                .order_by('-create_dt') \
                .values('sender_id', 'recipient_id',
                        'sender__phone_number', 
                        'recipient__phone_number', 
                        'type__type', 'message', 'create_dt')
        
        phone_number_list = cls.get_phone_number_list(sms_list, user_id)

        chat_list, target_number = cls.get_chat_list(sms_list, user_id, target_id)

        return phone_number_list, chat_list, target_number
        
    @classmethod
    def get_chat_list(cls, sms_list, user_id, target_id):
        result = []
        target_number = ''

        if target_id == None:
            return [], ''
        
        target_id = int(target_id)

        for sms in reversed(sms_list):
            if sms['sender_id'] == user_id and sms['recipient_id'] == target_id:
                result.append({
                    "message" : sms['message'],
                    "create_dt" : sms['create_dt'],
                    "sender" : 0
                })
                if target_number == '':
                    target_number = sms['recipient__phone_number']
            
            if sms['sender_id'] == target_id:
                result.append({
                    "message" : sms['message'],
                    "create_dt" : sms['create_dt'],
                    "sender" : 1
                })
                if target_number == '':
                    target_number = sms['sender__phone_number']
        
        return result, target_number

    @classmethod
    def get_phone_number_list(cls, sms_list, user_id):
        """
        mendapatkan list nomor telepon sms
        """
        phone_number_list = []
        result = []

        for sms in sms_list: 
            if sms['sender__phone_number'] not in phone_number_list and \
               sms['sender_id'] != user_id:

                phone_number_list.append(sms['sender__phone_number'])
            
            if sms['recipient__phone_number'] not in phone_number_list and \
               sms['recipient_id'] != user_id:

                phone_number_list.append(sms['recipient__phone_number'])
 
        result = []       
        for sms in sms_list:
            if len(phone_number_list) == 0:
                break

            if sms['recipient__phone_number'] in phone_number_list:
                result.append({
                    "phone_number" : sms['recipient__phone_number'],
                    "user_id" : sms['recipient_id'],
                    "message" : sms['message'],
                    "create_dt" : sms['create_dt'],
                    "type" : sms['type__type'],
                })
                index = phone_number_list.index(sms['recipient__phone_number'])
                phone_number_list.pop(index)

            if sms['sender__phone_number'] in phone_number_list:
                result.append({
                    "phone_number" : sms['sender__phone_number'],
                    "user_id" : sms['sender_id'],
                    "message" : sms['message'],
                    "create_dt" : sms['create_dt'],
                    "type" : sms['type__type'],
                })
                index = phone_number_list.index(sms['sender__phone_number'])
                phone_number_list.pop(index)

        return result

    @classmethod
    def store_message(cls, sender_id, recipient_number, message):
        """
        menyimpan pesan
        """

        recipient = User.objects \
            .filter(phone_number = recipient_number) \
            .first()

        new_message_data = Sms(
            message = message,
            recipient = recipient,
            sender_id = sender_id,
            type_id = 1,
            create_dt = timezone.now()
        )

        new_message_data.save()

        return recipient.id
    

    @classmethod
    def predict_message(cls):
        pass

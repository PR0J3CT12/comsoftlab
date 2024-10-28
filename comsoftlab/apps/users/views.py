from django.http import HttpResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
import json
from django.core.exceptions import ObjectDoesNotExist
from comsoftlab.apps.users.models import User, Message
from comsoftlab.apps.users.docs import *


@swagger_auto_schema(method='GET', operation_summary="Получить сообщения пользователя.",
                     responses=get_messages_responses)
@api_view(["GET"])
def get_messages(request, uid):
    try:
        user = User.objects.get(id=uid)
        messages = Message.objects.filter(user=user).order_by('sent_date').values('id', 'subject', 'sent_date', 'received_date', 'message_subject', 'message_text', 'attachments')
        messages_list = []
        for message in messages:
            messages_list.append({
                'id': message['id'],
                'subject': message['subject'],
                'sent_date': message['sent_date'].strftime("%d.%m.%Y %H:%M"),
                'received_date': message['received_date'].strftime("%d.%m.%Y %H:%M"),
                'message_subject': message['message_subject'],
                'message_text': message['message_text'],
                'attachments': message['attachments'],
            })
        return HttpResponse(json.dumps(
            messages_list, ensure_ascii=False), status=200)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps(
            {'state': 'error', 'message': 'Пользователь не существует.', 'details': {},
             'instance': request.path},
            ensure_ascii=False), status=404)
    except Exception as e:
        return HttpResponse(json.dumps(
            {'state': 'error', 'message': f'Произошла странная ошибка.', 'details': {'error': str(e)},
             'instance': request.path},
            ensure_ascii=False), status=404)
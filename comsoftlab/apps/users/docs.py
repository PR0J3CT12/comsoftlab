from drf_yasg import openapi

get_messages_response_200 = openapi.Schema(type=openapi.TYPE_OBJECT,
                                           properties={
                                               'id': openapi.Schema(type=openapi.TYPE_STRING,
                                                                    example="CAOP6p6da6nKiyPUWQsPL214ErFwNXfkKt-S-3WpONmQq4Jtk1Q"),
                                               'subject': openapi.Schema(type=openapi.TYPE_STRING,
                                                                         example="mail@mail.ru"),
                                               'sent_date': openapi.Schema(type=openapi.TYPE_STRING,
                                                                           example="01.01.2024 14:14"),
                                               'received_date': openapi.Schema(type=openapi.TYPE_STRING,
                                                                               example="01.01.2024 14:14"),
                                               'message_subject': openapi.Schema(type=openapi.TYPE_STRING,
                                                                                 example="Тема сообщения"),
                                               'message_text': openapi.Schema(type=openapi.TYPE_STRING,
                                                                              example="Текст сообщения"),
                                               'attachments': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                                             items=openapi.Schema(
                                                                                 type=openapi.TYPE_OBJECT,
                                                                                 properties={
                                                                                     'filename': openapi.Schema(
                                                                                         type=openapi.TYPE_STRING,
                                                                                         example="filename.jpg"),
                                                                                 })),
                                           })
get_messages_responses = {200: get_messages_response_200}

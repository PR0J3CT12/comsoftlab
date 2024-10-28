from django.db import models


class User(models.Model):
    id = models.AutoField('id пользователя', primary_key=True, editable=False)
    email = models.EmailField('Почта пользователя', max_length=100, unique=True)
    password = models.CharField('Пароль пользователя', max_length=200)  # конечно хранить нужно хеш пароля
    created = models.DateTimeField('Дата создания пользователя', auto_now_add=True)

    def __str__(self):
        return f'{str(self.email)}'

    class Meta:
        db_table = 'users'


class Message(models.Model):
    id = models.CharField('id сообщения', primary_key=True, editable=False, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField('Отправитель/получатель', max_length=255)
    sent_date = models.DateTimeField('Дата отправки сообщения')
    received_date = models.DateTimeField('Дата получения сообщения', auto_now_add=True)
    message_subject = models.TextField('Тема сообщения')
    message_text = models.TextField('Текст сообщения')
    attachments = models.JSONField('Список файлов', blank=True)

    class Meta:
        db_table = 'messages'

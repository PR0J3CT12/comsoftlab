import imaplib
from email import message_from_bytes
import base64
from datetime import datetime


EMAIL_PROVIDERS = {
    'gmail.com': {
        'scope': 'https://mail.google.com',
        'imap_server': 'imap.gmail.com',
    },
    'yandex.ru': {
        'scope': 'https://mail.yandex.ru',
        'imap_server': 'imap.yandex.ru',
    },
    'mail.ru': {
        'scope': 'https://e.mail.ru',
        'imap_server': 'imap.mail.ru',
    },
}


class EmailClient:
    def __init__(self, email, password, provider):
        self.email = email
        self.password = password
        self.provider = provider
        self.config = EMAIL_PROVIDERS.get(provider)

        if not self.config:
            raise ValueError(f"Неизвестный почтовый провайдер: {provider}")

        self.imap_server = self.config['imap_server']
        self.connection = None

    def connect(self):
        self.connection = self._connect_with_password()

    def _connect_with_password(self):
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.email, self.password)
        return mail

    def fetch_messages(self, folder='inbox'):
        if not self.connection:
            raise ConnectionError("Необходимо сначала подключиться к почтовому серверу.")

        self.connection.select(folder)
        status, message_numbers = self.connection.search(None, 'ALL')

        if status != 'OK':
            raise Exception("Ошибка поиска сообщений")

        messages = []
        for num in message_numbers[0].split():
            status, data = self.connection.fetch(num, '(RFC822)')
            if status != 'OK':
                continue

            msg = message_from_bytes(data[0][1])
            messages.append(self._parse_message(msg))

        messages.reverse()
        return messages

    def _decode_base64(self, msg):
        base64_encoded = msg.split('?B?')[1].split('?=')[0]
        decoded_text = base64.b64decode(base64_encoded).decode('utf-8')
        return decoded_text

    def _parse_date(self, date_string):
        date_object = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
        return date_object

    def _parse_email(self, email_string):
        email = email_string.split('<')[-1][:-1]
        return email

    def _parse_message(self, msg):
        return {
            'id': msg.get('Message-ID')[1:-1].split('@')[0],
            'subject': self._decode_base64(msg.get('Subject')),  # тема сообщения
            'from': self._parse_email(msg.get('From')),
            'to': msg.get('To'),
            'date': self._parse_date(msg.get('Date')),
            'body': self._get_message_body(msg),
            'attachments': self._get_attachments(msg)
        }

    def _get_message_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()

    def _get_attachments(self, msg):
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append({
                            'filename': filename,
                            #'data': part.get_payload(decode=True)
                        })
        return attachments

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection.logout()

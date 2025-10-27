from django.conf import settings
import requests



class Telegram:
    def __init__(self, token=settings.TELEGRAM_TOKEN):
        self.token = token
        self.chat_id_channel = settings.CHAT_ID_CHANNEL
        self.url = f'https://api.telegram.org/bot{self.token}/'
    



    def send_message(self, chat_id, text):
        params = {
            'chat_id': chat_id,
            'text': text,
        }
        response = requests.post(self.url + 'sendMessage', data=params)
        return response.json()
    def send_photo(self, chat_id, photo, caption=None):
        params = {
            'chat_id': chat_id,
            'photo': photo,
        }
        if caption is not None:
            params['caption'] = caption
        response = requests.post(self.url + 'sendPhoto', data=params)
        return response.json()

    def send_product_to_channel(self, text, image=None):
        if image:
            self.send_photo(self.chat_id_channel, image, text)
        else:
            self.send_message(self.chat_id_channel, text)
    
    def edit_message_text(self, chat_id, message_id, text):
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
        }
        response = requests.post(self.url + 'editMessageText', data=params)
        return response.json()

    def edit_message_caption(self, chat_id, message_id, caption):
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'caption': caption,
        }
        response = requests.post(self.url + 'editMessageCaption', data=params)
        return response.json()

    def edit_message_media(self, chat_id, message_id, photo, caption=None):
        media = {
            'type': 'photo',
            'media': photo,
        }
        if caption is not None:
            media['caption'] = caption
        payload = {
            'chat_id': chat_id,
            'message_id': message_id,
            'media': media,
        }
        response = requests.post(self.url + 'editMessageMedia', json=payload)
        return response.json()
    
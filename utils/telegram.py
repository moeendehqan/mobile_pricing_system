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
        response = requests.post(self.url + 'sendMessage', params=params)
        return response.json()
    def send_photo(self, chat_id, photo, caption=None):
        params = {
            'chat_id': chat_id,
            'photo': photo,
        }
        if caption:
            params['caption'] = caption
        response = requests.post(self.url + 'sendPhoto', params=params)
        return response.json()
    def send_video(self, chat_id, video):
        params = {
            'chat_id': chat_id,
            'video': video,
        }
        response = requests.post(self.url + 'sendVideo', params=params)
        return response.json()
    def send_document(self, chat_id, document):
        params = {
            'chat_id': chat_id,
            'document': document,
        }
        response = requests.post(self.url + 'sendDocument', params=params)
        return response.json()
    def send_audio(self, chat_id, audio):
        params = {
            'chat_id': chat_id,
            'audio': audio,
        }
        response = requests.post(self.url + 'sendAudio', params=params)
        return response.json()
    def send_voice(self, chat_id, voice):
        params = {
            'chat_id': chat_id,
            'voice': voice,
        }
        response = requests.post(self.url + 'sendVoice', params=params)
        return response.json()
    def send_location(self, chat_id, location):
        params = {
            'chat_id': chat_id,
            'location': location,
        }
        response = requests.post(self.url + 'sendLocation', params=params)
        return response.json()
    def send_contact(self, chat_id, contact):
        params = {
            'chat_id': chat_id,
            'contact': contact,
        }
        response = requests.post(self.url + 'sendContact', params=params)
        return response.json()
    

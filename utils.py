import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage


channel_access_token = "91xFl2RPQAVenKkLweKDwVPlGN0MAQ4/RD2zuqWunfBz7KFSLjGlj6mMpcZqHEmpT+4L89diO5nGokJVzkW7aMO2nrreYfVnhIeUcFgecqpkyl7i01Upe512uLtX5epSUHNJGvZfxlnD9iHjfcwDuQdB04t89/1O/w1cDnyilFU="


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""

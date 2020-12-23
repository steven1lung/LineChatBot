import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage ,  ButtonsTemplate,ImageSendMessage, TemplateSendMessage, MessageTemplateAction


channel_access_token = "91xFl2RPQAVenKkLweKDwVPlGN0MAQ4/RD2zuqWunfBz7KFSLjGlj6mMpcZqHEmpT+4L89diO5nGokJVzkW7aMO2nrreYfVnhIeUcFgecqpkyl7i01Upe512uLtX5epSUHNJGvZfxlnD9iHjfcwDuQdB04t89/1O/w1cDnyilFU="


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"
    
def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"


def send_button_message(reply_token, title, text, btn, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"



"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""

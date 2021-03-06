# encoding: utf-8
import os
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from googleTranslater import *
from moodDeterminer import *

app = Flask(__name__)
line_bot_api = LineBotApi('quz2dQQwCibQaIaWOJ7Y2uz6Uh486G+WHjLAFvuhYN0EHur2EtKMstVo+Y0niIjNhV9adAg/LDK7pY1T2ZRuBeH+Rga1DljktGG+2/fNmdw9FX0kyN6HWiV0zUyj3Vkhk7EcWdGgSjCmTcc/c9e3EwdB04t89/1O/w1cDnyilFU=') # Your Channel Access Token
handler = WebhookHandler('456d1cdec1fb86bc17c82d3c0c3941c6') # Your Channel Secret

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="hello"))
    translater = GoogleTranslater()
    determiner = MoodDeterminer()
    translater.sendText(event.message.text)
    receive1 = translater.getText()
    determiner.sendText(receive1)
    text = "開心程度: %s" % determiner.getText()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text)) # reply the same message from user
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

# encoding: utf-8
import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

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
    url = "https://tw.beanfun.com/maplestory/Bullentin_alpha/_BullentinDefault.aspx"
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    hoarding = soup.select(".maple01")
    # text = event.message.text # message from user
    text = ""
    for i in hoarding[1:]:
	    h = i.find("a").get("href")
	    if not "https" in h:
		    text += "* https://tw.beanfun.com/%s\n\n" % h
	    else:
		    text += "* %s\n\n" % h
    text = text.split('*')
    for i in text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=i))
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text)) # reply the same message from user

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

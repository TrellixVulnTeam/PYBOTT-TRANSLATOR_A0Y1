from flask import Flask, request, abort , send_from_directory , render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from yandex.Translater import Translater
from fuzzywuzzy import process ## import fuzz

app = Flask(__name__)

line_bot_api = LineBotApi('n47jlxbCxgSRHezdf7LmnkR8yOHsF2QxvcxcQmphMqidQEBXoieLSqzREtf/wKOM+b3676KR4wisbOblnHXmNVkMuqaCxV26/E/TCYH4D/EJQyrzv9EOiI9fHbPCOPsXbZaGonctXaeLgGn5vfhZxgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ecf5d0fcdaa5b716853f6f133af60874')
user_session = {} #database for correct user
tr = Translater()
tr.set_key('trnsl.1.1.20191108T161057Z.789702196707e5b2.41eba9a721c3e06bd2ae57a2a1189764eb9e1b8d') # Api key found on https://translate.yandex.com/developers/keys

List_test = []


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

from yandex.Translater import Translater



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text_from_user = event.message.text #get text from user
    replytoken = event.reply_token #get reply token
    userid = event.source.user_id # get userid
    print(user_session)
    print(userid)
    print(type(userid))
    user_current_session = user_session[userid]['session'] #get current user session
    
    ## Acess Translation function
    if user_current_session == None and text_from_user == 'แปลข้อความ':
        action1 = MessageAction(label="English",text="English")
        qbtn1 = QuickReplyButton(action=action1)
        action2 = MessageAction(label="France",text="France")
        qbtn2 = QuickReplyButton(action=action2)
        action3 = MessageAction(label="German",text="German")
        qbtn3 = QuickReplyButton(action=action3)
        action4 = MessageAction(label="Japan",text="Japan")
        qbtn4 = QuickReplyButton(action=action4)

        qreply = QuickReply(items=[qbtn1,qbtn2,qbtn3,qbtn4])

        text = TextSendMessage(text="ต้องการแปลเป็นภาษาอะไรดีคะ? กรุณาระบุ",quick_reply=qreply)
        line_bot_api.reply_message(replytoken,text)
        user_session[userid]['session'] = "Selectlang"

    elif user_current_session == "Selectlang":
        from translator import check_lang
        True_lang = check_lang(Input=text_from_user)
        if True_lang is None:
            text = TextSendMessage(text="ดิฉันไม่รู้จักภาษานั้น กรุณาเลือกภาษาใหม่อีกครั้ง")
            line_bot_api.reply_message(replytoken,text)
        else:
            text = TextSendMessage(text="ท่านต้องการให้ดิฉันแปลจากไทยเป็น {} ใช่ไหมค่ะ".format(True_lang))
            text2 = TextSendMessage(text="กรุณาพิมพ์ข้อความที่ท่านต้องการแปลคะ")
            line_bot_api.reply_message(replytoken,messages=[text,text2])
            user_session[userid]['session'] = "textinput"
            user_session[userid]['lang'] = True_lang

    
    elif user_current_session == "textinput":
        from translator import tran
        output = tran(text_from_user=text_from_user,
                                to_lang=user_session[userid]['lang'],tr=tr)
        from Flex import Flex_output
        flex_to_reply = Flex_output(text=output)
        flex_object = Base.get_or_new_from_json_dict(flex_to_reply,FlexSendMessage)
        line_bot_api.reply_message(replytoken,messages=flex_object)
        user_session[userid]['session'] = "continue"
        List_test.append([text_from_user,output])
    
    elif user_current_session == "continue":
        if text_from_user == 'แปลข้อความใหม่':
            text2 = TextSendMessage(text="กรุณาพิมพ์ข้อความที่ท่านต้องการแปลคะ")
            line_bot_api.reply_message(replytoken,messages=text2)
            user_session[userid]['session'] = "textinput"
        elif text_from_user == 'ออกจากการแปล':
            text2 = TextSendMessage(text="ขอบคุณที่ใช้บริการล่ามแปลภาษาคะ ไว้มาใช้บริการใหม่นะคะ")
            line_bot_api.reply_message(replytoken,messages=text2)
            user_session[userid]['session'] = None


@handler.add(FollowEvent)
def Greeting(event):
    userid = event.source.user_id # get userid
    user = {}
    user['session'] = None
    user['lang'] = None
    user_session[userid] = user

    line_bot_api.link_rich_menu_to_user(user_id=userid,
    rich_menu_id="richmenu-b72e00c9a83af2083a82e3f117a409d2")

    text = TextSendMessage(text="สวัสดีคะ ยินดีต้อนรับสู่บริการแปลข้อความ")
    reply_tok = event.reply_token
    line_bot_api.reply_message(reply_tok,messages=text) ##ตอบกลับ

import os
@app.route('/<picname>')
def getimage(picname):
    current_path = os.path.dirname(os.path.realpath(__file__)) 
    dir_path = os.path.join(current_path,'pic','pic1')
    return send_from_directory(dir_path,picname)

@app.route('/<picname>/1040')
def getimagemap(picname):
    current_path = os.path.dirname(os.path.realpath(__file__)) 
    dir_path = os.path.join(current_path,'pic','pic1')
    return send_from_directory(dir_path,picname)

@app.route('/')
def index():
    return render_template('index.html',data = List_test)


if __name__ == "__main__":
    app.run(port=8000)
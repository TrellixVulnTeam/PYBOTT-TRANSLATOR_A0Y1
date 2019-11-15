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

from Config import DEVELOPEMENTCONFIG
from datetime import datetime
from Flex import Flex_output , Flex_database

line_bot_api = LineBotApi(DEVELOPEMENTCONFIG.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(DEVELOPEMENTCONFIG.CHANNEL_SECRET)
user_session = {} #database for correct user
tr = Translater()
tr.set_key(DEVELOPEMENTCONFIG.YANDEX_KEY) # Api key found on https://translate.yandex.com/developers/keys

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
from MessageTemplate.Imgmap import ImgmapCourses,ImgmapDetail


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text_from_user = event.message.text #get text from user
    replytoken = event.reply_token #get reply token
    userid = event.source.user_id # get userid 
    try :
        user_current_session = user_session[userid]['session'] #get current user session
    except:
        user = {}
        user['session'] = None
        user['lang'] = None
        user_session[userid] = user
        user_current_session = user_session[userid]['session']
    
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
        
        if output is not None:
            flex_to_reply = Flex_output(text=output['text_output'],to_lang=output['to_lang'])
            flex_object = Base.get_or_new_from_json_dict(flex_to_reply,FlexSendMessage)
            line_bot_api.reply_message(replytoken,messages=flex_object)
        else :
            flex_to_reply = Flex_output(to_lang=output['to_lang'])
            flex_object = Base.get_or_new_from_json_dict(flex_to_reply,FlexSendMessage)
            line_bot_api.reply_message(replytoken,messages=flex_object)
        user_session[userid]['session'] = "continue"
        
        ### get data to database
        profile = line_bot_api.get_profile(userid)
        display_name = profile.display_name
        pic = profile.picture_url
        date = datetime.date(datetime.now())
        List_test.append([text_from_user,output,display_name,pic,date])
    
    elif user_current_session == "continue":
        if text_from_user == 'แปลข้อความใหม่':
            text2 = TextSendMessage(text="กรุณาพิมพ์ข้อความที่ท่านต้องการแปลคะ")
            line_bot_api.reply_message(replytoken,messages=text2)
            user_session[userid]['session'] = "textinput"
        elif text_from_user == 'ออกจากการแปล':
            action1 = MessageAction(label="เริ่มแปลข้อความ",text="แปลข้อความ")
            qbtn1 = QuickReplyButton(action=action1)
            action2 = MessageAction(label="สนใจเรียนเขียนแชทบอท",text="สนใจคอสเรียนไพทอน-LineChatBot")
            qbtn2 = QuickReplyButton(action=action2)
            qreply = QuickReply(items=[qbtn1,qbtn2])
            
            imagemap = Base.get_or_new_from_json_dict(data=ImgmapCourses(),cls=ImagemapSendMessage)
            
            text2 = TextSendMessage(text="ขอบคุณที่ใช้บริการล่ามแปลภาษาคะ ไว้มาใช้บริการใหม่นะคะ",quick_reply=qreply)
            
            line_bot_api.reply_message(replytoken,messages=[imagemap,text2])
            user_session[userid]['session'] = None
    
    elif user_current_session == None and text_from_user == 'สนใจคอสเรียนไพทอน-LineChatBot':
        action1 = MessageAction(label="เริ่มแปลข้อความ",text="แปลข้อความ")
        qbtn1 = QuickReplyButton(action=action1)


        qreply = QuickReply(items=[qbtn1])
        imagemap2 = Base.get_or_new_from_json_dict(data=ImgmapDetail(),cls=ImagemapSendMessage)
        text2 = TextSendMessage(text="ยังไม่เปิดรับสมัคร ณ ขณะนี้ ท่านสามารถ Inbox ทางเพจ Pybott เพื่อจองที่นั่งก่อนได้ ฝากกดไลค์กดแชร์เพื่อติดตาม เนื้อหา / คอสเรียนฟรี ผ่านเพจ Pybott ด้วยนะคะ",quick_reply=qreply)

        line_bot_api.reply_message(replytoken,[imagemap2,text2])
        
    elif user_current_session == None and text_from_user == 'ฐานข้อมูลผู้ใช้งาน':
        action1 = MessageAction(label="เริ่มแปลข้อความ",text="แปลข้อความ")
        qbtn1 = QuickReplyButton(action=action1)


        qreply = QuickReply(items=[qbtn1])
        flex_db = Base.get_or_new_from_json_dict(data=Flex_database(),cls=FlexSendMessage)
        text2 = TextSendMessage(text="เช็คว่าทุกคนแปลข้อความอะไรไปบ้าง",quick_reply=qreply)
        
        line_bot_api.reply_message(replytoken,[flex_db,text2])
        
    
    else:
        action1 = MessageAction(label="เริ่มแปลข้อความ",text="แปลข้อความ")
        qbtn1 = QuickReplyButton(action=action1)
        action2 = MessageAction(label="สนใจเรียนเขียนแชทบอท",text="สนใจคอสเรียนไพทอน-LineChatBot")
        qbtn2 = QuickReplyButton(action=action2)
        qreply = QuickReply(items=[qbtn1,qbtn2])
        imagemap = Base.get_or_new_from_json_dict(data=ImgmapCourses(),cls=ImagemapSendMessage)
        text1 = TextSendMessage(text="อยากมีบอท เลขาอัจริยะส่วนตัว เป็นของตัวเองไหมคะ เราขอนำเสนอ คอสเรียน Line Chatbot With Python >> Zero to Hero<< ไม่ต้องมีพื้นฐาน เรียนออนไลน์ดูได้จนกว่าจะเป็น พร้อมตัวอย่าง SourceCode การพัฒนาบอทในทางต่างๆ",quick_reply=qreply)
        text2 = TextSendMessage(text="ท่านสามารถใช้งานได้โดยการกดปุ่ม แปลข้อความ เพื่อเริ่มบริการแปล",quick_reply=qreply)
        
        line_bot_api.reply_message(replytoken,[imagemap,text1,text2])
        
        
        

@handler.add(FollowEvent)
def Greeting(event):
    userid = event.source.user_id # get userid
    user = {}
    user['session'] = None
    user['lang'] = None
    user_session[userid] = user

    line_bot_api.link_rich_menu_to_user(user_id=userid,
    rich_menu_id="richmenu-6832c0f205b6d0c787d70c7c3364d0c9")
    
    action1 = MessageAction(label="เริ่มแปลข้อความ",text="แปลข้อความ")
    qbtn1 = QuickReplyButton(action=action1)
    
    qreply = QuickReply(items=[qbtn1])

    text = TextSendMessage(text="สวัสดีคะ ยินดีต้อนรับสู่บริการแปลข้อความ",quick_reply=qreply)
    
    imagemap = Base.get_or_new_from_json_dict(data=ImgmapCourses(),cls=ImagemapSendMessage)
    
    
    reply_tok = event.reply_token
    line_bot_api.reply_message(reply_tok,messages=[imagemap,text]) ##ตอบกลับ

import os
@app.route('/<picname>')
def getimage(picname):
    current_path = os.path.dirname(os.path.realpath(__file__)) 
    dir_path = os.path.join(current_path,'pic')
    return send_from_directory(dir_path,picname)

@app.route('/<picname>/1040')
def getimagemap(picname):
    current_path = os.path.dirname(os.path.realpath(__file__)) 
    dir_path = os.path.join(current_path,'pic')
    return send_from_directory(dir_path,picname)

@app.route('/')
def index():
    return render_template('index.html',data = List_test)


if __name__ == "__main__":
    app.run(port=200)
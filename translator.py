from yandex.Translater import Translater
from fuzzywuzzy import process ## import fuzz
#ctrl+[ ดึงไปทางซ้าย
# Api key found on https://translate.yandex.com/developers/keys

## สำหรับแปลภาษา ใส่ คำที่ต้องการแปล + ภาษาที่ต้องการแปล
def tran(text_from_user,to_lang,tr):
    data = {}
    if to_lang == 'fr':
        data['to_lang'] = 'ฝรั่งเศษ'
    elif to_lang == 'de':
        data['to_lang'] = 'เยอรมัน'
    elif to_lang == 'en':
        data['to_lang'] = 'อังกฤษ'
    elif to_lang == 'ja':
        data['to_lang'] = 'ญี่ปุ่น'
        
    if to_lang is None:
        return None
    else :
        tr.set_from_lang('th')
        tr.set_to_lang(to_lang)
        tr.set_text(text_from_user)
        text_output = tr.translate()
        data['text_output'] = text_output
        return data

## ดูว่ายูสเซอต้องการแปลภาษาอะไร
def check_lang(Input):
    corpus = {
        'fr' : ['france','ฝรั่งเศส'], #90
        'de' : ['german','deutsch','เยอรมันนี'], #36
        'en' : ['english','อังกฤษ','อิ้ง'], #67
        'ja' : ['Japanese','ญป','ญี่ปุ่น','ยุ่น','เจแปน'] 
    }
    best_match = ''
    highest_score = 0
    for key,value in corpus.items():
        out = process.extractOne(Input, value)
        if out[1] > highest_score:
            highest_score = out[1]
            best_match = key
        else :
            continue
    if highest_score <= 70:
        best_match = None
    return best_match

# print("ยินดีต้อนรับสู่บริการแปลภาษา") #<---- greeting 
# while True:
#     True_Lang = None
#     while True:
#         In1 = input("ต้องการแปลไทยเป็นภาษาอะไรดีคะ?") #<-- selectlang
#         lang = check_lang(In1)
#         if lang is None:
#             continue
#         else :
#             True_Lang = lang
#             break
#     print(True_Lang)
#     In2 = input("กรุณา พิมพ์ประโยคที่ต้องการให้แปลคะ") #<-- textinput
#     result = tran(text_from_user=In2,to_lang=True_Lang)
#     print(result) #<-- result output
#     In3 = input("ต้องการแปลอีกไหมคะ?(Y/N))") #<-- result output
#     if In3.upper() == 'Y':
#         continue
#     else : 
#         break

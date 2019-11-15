richdata = {
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": True,
  "name": "แถบช่วยเหลือ",
  "chatBarText": "แถบช่วยเหลือ",
  "areas": [
    {
      "bounds": {
        "x": 0,
        "y": 8,
        "width": 2496,
        "height": 886
      },
      "action": {
        "type": "message",
        "text": "สนใจเรียนแชทบอท"
      }
    },
    {
      "bounds": {
        "x": 8,
        "y": 919,
        "width": 1013,
        "height": 755
      },
      "action": {
        "type": "message",
        "text": "ฐานข้อมูลผู้ใช้งาน"
      }
    },
    {
      "bounds": {
        "x": 1038,
        "y": 919,
        "width": 1454,
        "height": 750
      },
      "action": {
        "type": "message",
        "text": "แปลข้อความ"
      }
    }
  ]
}

channel_access_token = "n47jlxbCxgSRHezdf7LmnkR8yOHsF2QxvcxcQmphMqidQEBXoieLSqzREtf/wKOM+b3676KR4wisbOblnHXmNVkMuqaCxV26/E/TCYH4D/EJQyrzv9EOiI9fHbPCOPsXbZaGonctXaeLgGn5vfhZxgdB04t89/1O/w1cDnyilFU="

import json

import requests



def RegisRich(Rich_json,channel_access_token):

    url = 'https://api.line.me/v2/bot/richmenu'

    Rich_json = json.dumps(Rich_json)

    Authorization = 'Bearer {}'.format(channel_access_token)


    headers = {'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': Authorization}

    response = requests.post(url,headers = headers , data = Rich_json)

    print(str(response.json()['richMenuId']))

    return str(response.json()['richMenuId'])

def CreateRichMenu(ImageFilePath,Rich_json,channel_access_token):


    richId = RegisRich(Rich_json = Rich_json,channel_access_token = channel_access_token)

    url = ' https://api.line.me/v2/bot/richmenu/{}/content'.format(richId)

    Authorization = 'Bearer {}'.format(channel_access_token)

    headers = {'Content-Type': 'image/jpeg',
    'Authorization': Authorization}

    img = open(ImageFilePath,'rb').read()

    response = requests.post(url,headers = headers , data = img)

    print(response.json())



CreateRichMenu(ImageFilePath='tran.jpg',Rich_json=richdata,channel_access_token=channel_access_token)



def Flex_output(text="ขออภัยคะดิฉันไม่สามารถแปลความหมายของคำนี้เลยคะ",to_lang=" - "):
    flex = {
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "bubble",
    "direction": "ltr",
    "hero": {
      "type": "image",
      "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDYswiR8z_eWmSf2Y3e7N7knq6BuxG56r78NnhZJzupyANAHMq",
      "align": "center",
      "gravity": "center",
      "size": "full",
      "aspectRatio": "1.51:1",
      "aspectMode": "cover"
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "RESULT",
          "size": "xxl",
          "align": "start",
          "weight": "bold",
          "color": "#0927A5"
        },
        {
          "type": "text",
          "text": "ข้อความดังกล่าวแปลเป็นภาษา",
          "margin": "none",
          "size": "md",
          "align": "start",
          "color": "#8EA0EC"
        },
        {
          "type": "text",
          "text": "{} ได้ดังนี้.....".format(to_lang),
          "size": "md",
          "align": "start",
          "color": "#8EA0EC"
        },
        {
          "type": "separator",
          "margin": "lg",
          "color": "#BFBFBF"
        },
        {
          "type": "box",
          "layout": "vertical",
          "margin": "md",
          "contents": [
            {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": text,
                  "align": "start",
                  "wrap": True
                }
              ]
            }
          ]
        },
        {
          "type": "separator",
          "margin": "lg",
          "color": "#BFBFBF"
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "แปลข้อความใหม่",
                "text": "แปลข้อความใหม่"
              },
              "color": "#0D2678",
              "height": "sm",
              "style": "primary"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "ออกจากการแปล",
                "text": "ออกจากการแปล"
              },
              "margin": "md",
              "height": "sm",
              "style": "secondary"
            }
          ]
        }
      ]
    }
  }
}
    return flex
  


from flask import request
def Flex_database():
  flex = {
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "bubble",
    "direction": "ltr",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "ฐานข้อมูลการใช้งานของ USER",
          "align": "center"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "https://pngriver.com/wp-content/uploads/2018/04/Download-Database-PNG.png",
      "size": "full",
      "aspectRatio": "1.51:1",
      "aspectMode": "fit"
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "separator"
        },
        {
          "type": "text",
          "text": "รวมข้อมูลการใช้งานของ USER",
          "margin": "lg",
          "size": "md",
          "align": "center",
          "weight": "bold",
          "color": "#05013D"
        },
        {
          "type": "separator",
          "margin": "lg",
          "color": "#B8B8B8"
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "กดเพื่อเปิดฐานข้อมูล",
            "uri": "https://"+request.host
          },
          "color": "#0A2389",
          "style": "primary"
        }
      ]
    }
  }
}
  return flex
  

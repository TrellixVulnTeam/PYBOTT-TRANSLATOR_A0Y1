from flask import request


def ImgmapCourses():
  url = 'https://'+request.host+'/ImageMapCourses.png'
  imagemap = {
  "type": "imagemap",
  "baseUrl": url,
  "altText": "This is an imagemap",
  "baseSize": {
    "width": 1040,
    "height": 1040
  },
  "actions": [
    {
      "type": "message",
      "area": {
        "x": 2,
        "y": 0,
        "width": 1034,
        "height": 1038
      },
      "text": "สนใจคอสเรียนไพทอน-LineChatBot"
    }
  ]
}
  
  return imagemap

def ImgmapDetail():
  url = 'https://'+request.host+'/ImageMapDetail.png'
  imagemap = {
  "type": "imagemap",
  "baseUrl": url,
  "altText": "This is an imagemap",
  "baseSize": {
    "width": 1040,
    "height": 1040
  },
  "actions": [
    {
      "type": "uri",
      "area": {
        "x": 4,
        "y": 5,
        "width": 1032,
        "height": 1031
      },
      "linkUri": "https://www.facebook.com/Pybott"
    }
  ]
}      
  return imagemap

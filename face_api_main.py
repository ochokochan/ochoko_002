import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

st.title('顔認識アプリ')

subscription_key = 'c71719dca22746b3ac36f180fee7bb23'
assert subscription_key
face_api_url = 'https://faceapitest20210810b.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader('Choose an image...', type = 'jpg')

if uploaded_file is not None:

    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
          img.save(output, format = 'JPEG')
          binary_img = output.getvalue() #バイナリ取得

    headers = {
          'Content-Type':'application/octet-stream',
          'Ocp-Apim-Subscription-Key': subscription_key
    }
    params = {
          'returnFaceId': 'true',
          'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
    results = res.json()

    for result in results:
          rect = result['faceRectangle']
          text = result['faceAttributes']['gender']+'/'+str(result['faceAttributes']['age'])

          draw = ImageDraw.Draw(img)
          draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'],
                          rect['top']+rect['height'])], fill = None, outline = 'green', width =5)

          draw_x = rect['left']
          draw_y = rect['top']-30

          text_top_left = (rect['left'] , rect['top'] - 30)
          align = 'Left'
          fill  = 'Red'
          draw.text((draw_x, draw_y), text, fill='red')

    st.image(img, caption='upload images',use_column_width=True)

import base64
import requests
import json
import re
import boto3
# from io 
url = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDrfUf8BMPMRcHQzAi1h4MZ56pGPeIeNMs'

# AIzaSyDrfUf8BMPMRcHQzAi1h4MZ56pGPeIeNMs


def detect_license_plate(encodedImage, imagePath):
    # img_base64 = base64.b64encode(imagePath)
    
    # headers = {'content-type': 'application/json'}

    # data = """{
    #   "requests": [
    #     {
    #       "image": {
    #                "content": '""" + encodedImage[:-1] + """'

    #                 },

    #       "features": [
    #         {
    #           "type": "TEXT_DETECTION"
    #         }
    #       ]
    #     }
    #   ]
    # }"""
    # r = requests.post(url, headers=headers, data=data)
    # result = json.loads(r.text)
    # print(result)
    # try:
    #     result = result['responses'][0]['textAnnotations'][0]['description']
    # except Exception as e:
    #     return r
    # result = result.replace('\n', '').replace(' ', '')
    # result =re.sub('\W+','', result)
    mystates = ['AP','AR','AS','BR','CG','GA','GJ','HR' ,'HP' ,'JK','JH','KA','KL','MP','MH','MN','ML','MZ','NL' ,'OD','PB' ,'RJ','SK','TN','TS','TR','UA','UK','UP','WB','AN','CH','DN','DD','DL' ,'LD','PY']
    
    
    # return result
    client = boto3.client("textract")
    image_binary = open(imagePath, "rb").read()
    response = client.detect_document_text(Document={"Bytes": image_binary})
    # print(response)
    blocks = response['Blocks']
    result = ""
    # print(blocks)
    for block in blocks:
      # print(block)
      if block['BlockType'] == "LINE":
        result = block['Text']

    # print(block)
    # print(block[])
    # print(result)
    if(len(result) > 0):
      res=re.findall("\s*[AP,AR,AS,BR,CG,GA,GJ,HR,HP,JK,JH,KA,KL,MP,MH,MN,ML,MZ,NL,OD,PB,RJ,SK,TN,TS,TR,UA,UK,UP,WB,AN,CH,DN,DD,DL,LD,PY]{2}\s*[0-9]{1,2}\s*[A-Z]{1,2}\s*[0-9]{1,4}\s*]?",result)    
      print(res)
      for word in mystates:
          if(word in result):
              res = re.findall(word + "[0-9]{1,2}\s*[A-Z]{1,2}\s*[0-9]{1,4}\s*]?", result)
              if(len(res) >0):
                  # print(res[0])
                  return "".join(re.findall("[A-Za-z0-9]*", res[0]))
    # if len(result) and result[0:3] == "IND": result = result[3:]

    return "".join(re.findall("[A-Za-z0-9]*", result))
    

import requests
import boto3

from os import path, curdir

inputFileName = "inputImage.jpg"
imagePath = path.join(curdir, "images/" + inputFileName)
image_display = True
pred_stagesArgVal = 2
croppedImagepath = path.join(curdir, "images/croppedImage.jpg")
print(imagePath, croppedImagepath)

def decodeImageIntoBase64(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    print(fileName)
    f = open(fileName, "wb")
    f.write(imgdata)
    f.save()
    f.close()
    print("Image saved")


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())


def main(event, context):
    filename = event["filename"]
    bucket = event["bucket"]
    objectName = event["object_name"]
    s3 = boto3.client("s3")
    with open(filename, "wb") as f:
        s3.download_fileobj(bucket, objectName, f)
        # saving the file
        f.save(imagePath)
    
    try:
        clApp = ClientApp()
        labelledImage = clApp.numberPlateObj.predictImages(imagePath, pred_stagesArgVal,
                                                           croppedImagepath, clApp.numberPlateObj)
        if labelledImage is not None:
            encodedCroppedImageStr = encodeImageIntoBase64(croppedImagepath)
            ig = str(encodedCroppedImageStr)
            ik = ig.replace('b\'', '')
            numberPlateVal = detect_license_plate(ik, croppedImagepath)
            if numberPlateVal is not None or numberPlateVal != "":
                # returnedVal = clApp.regPartDetailsObj.getNumberDetails(numberPlateVal)
                # responseDict = {"base64Image": ik, "partDetails" : returnedVal, "numberPlateVal": numberPlateVal}
                responseDict = {"registrationNumber": numberPlateVal}
                # responseList.append(responseDict)
                # print(responseDict)
                # convert to json data
                jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
                # print(jsonStr.decode())
                # return Response(jsonStr.decode())
                return responseDict
            else:
                # responseDict = {"base64Image": "Unknown", "partDetails" : "Unknown", "numberPlateVal": "Unknown"}
                responseDict = {"registrationNumber": "Unknown"}
                # responseList.append(responseDict)
                # print(responseDict)
                # convert to json data
                jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
                # print(jsonStr.decode())
                # return Response(jsonStr.decode())
                return responseDict
        else:
            # responseDict = {"base64Image": "Unknown", "partDetails" : "Unknown", "numberPlateVal": "Unknown"}
            responseDict = {"registrationNumber": "Unknown"}
            # responseList.append(responseDict)
            # print(responseDict)
            # convert to json data
            jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
            # print(jsonStr.decode())
            return responseDict
    except Exception as e:
        print(e)
    # responseDict = {"base64Image": "Unknown", "partDetails": "Unknown", "numberPlateVal": "Unknown"}
    responseDict = {"registrationNumber": "Unknown"}
    # responseList.append(responseDict)
    # print(responseDict)
    # convert to json data
    jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
    # print(jsonStr.decode())
    return responseDict
    # return Response("Invalid Input")


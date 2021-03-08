from wsgiref import simple_server
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
from getNumberPlateVals import detect_license_plate
import base64
import os
# from predict_iages import DetectVehicleNumberPlate
from predict_images import DetectVehicleNumberPlate
from os import curdir, path

application = Flask(__name__)

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
CORS(application)

inputFileName = "inputImage.jpg"
imagePath = path.join(curdir, "images/" + inputFileName)
image_display = True
pred_stagesArgVal = 2
croppedImagepath = path.join(curdir, "images/croppedImage.jpg")
print(imagePath, croppedImagepath)

class ClientApp:
    def __init__(self):
        # modelArg = "datasets/experiment_faster_rcnn/2018_08_02/exported_model/frozen_inference_graph.pb"
        self.modelArg = path.join(curdir, "datasets/experiment_ssd/2018_07_25_14-00/exported_model/frozen_inference_graph.pb")
        self.labelsArg = path.join(curdir, "datasets/records/classes.pbtxt")
        self.num_classesArg = 37
        self.min_confidenceArg = 0.5
        filepath = "autoPartsMapping/partNumbers.xlsx"
        # self.regPartDetailsObj = ReadPartDetails(filepath)
        self.numberPlateObj = DetectVehicleNumberPlate()


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

    # return base64.b64encode(croppedImagePath)

@application.route("/predict", methods=["POST"])
def getPrediction():
    print("Started prediction")
    # inpImage = request.json['image']
    # decodeImageIntoBase64(inpImage, imagePath)
    if 'file' not in request.files:
            return "No attribute with the name file"
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "No filename"
    # if file and allowed_file(file.filename):
    # filename = secure_filename(file.filename)
    file.save(path.join(imagePath))
    # responseList = []
    # it's a temporary variable just for testing
    # imageLoc = "images/truck.jpg"
    print("Saved image and headed to try block!")
    try:
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
                return jsonify(responseDict)
            else:
                # responseDict = {"base64Image": "Unknown", "partDetails" : "Unknown", "numberPlateVal": "Unknown"}
                responseDict = {"registrationNumber": "Unknown"}
                # responseList.append(responseDict)
                # print(responseDict)
                # convert to json data
                jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
                # print(jsonStr.decode())
                # return Response(jsonStr.decode())
                return jsonify(responseDict)
        else:
            # responseDict = {"base64Image": "Unknown", "partDetails" : "Unknown", "numberPlateVal": "Unknown"}
            responseDict = {"registrationNumber": "Unknown"}
            # responseList.append(responseDict)
            # print(responseDict)
            # convert to json data
            jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
            # print(jsonStr.decode())
            return Response(jsonStr.decode())
    except Exception as e:
        print(e)
    # responseDict = {"base64Image": "Unknown", "partDetails": "Unknown", "numberPlateVal": "Unknown"}
    responseDict = {"registrationNumber": "Unknown"}
    # responseList.append(responseDict)
    # print(responseDict)
    # convert to json data
    jsonStr = json.dumps(responseDict, ensure_ascii=False).encode('utf8')
    # print(jsonStr.decode())
    return Response(jsonStr.decode())
    # return Response("Invalid Input")


# port = int(os.getenv("PORT"))
if __name__ == '__main__':
    clApp = ClientApp()
    # host = "127.0.0.1"
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, application)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
    # application.run(host='0.0.0.0', port=port)

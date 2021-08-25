# fed4iot-cbpf-pana

## Require packages
```bash
$pip3 install pillow
$pip3 install azure-cognitiveservices-vision-face
$pip3 install paho-mqtt
$pip3 install Werkzeug
$pip3 install flask
```

## Create directory
```bash
$cd ~/fed4iot-cbpf-pana/src/FaceDetectionAndRecognition/
$mkdir image/find_image
$mkdir image/temp_image
$mkdir cache
```

## Usage  
```bash
$cd ~/fed4iot-cbpf-pana/src/FaceDetectionAndRecognition  
$python3 restapi_main.py
```
## Test script (for TV side)
```bash
$cd ~/fed4iot-cbpf-pana/test_tool/
$python3 test_cbpf.py start
(start camera system)
$python3 test_cbpf.py upload 
(upload request image file to find a person)
$python3 test_cbpf.py get_result
(obtain result)
$python3 test_cbpf.py close
(end camera system)

$python3 test_cbpf.py <cmd>
 <cmd>: start, close, upload, get_result
```

## Data model
```bash
{
  "id": "urn:ngsi-ld:CBPF",
  "type": "CBPF event",
  "Camera": {
    "id": {
      "type": "@id",
      "value": "urn:ngsi-ld:CBPF:camera"
    },
    "type": {
      "type": "@id",
      "value": "camera"
    },
    "location": {
      "type": "GeoProperty",
      "value": [
        <latitude>,
        <longitude>
      ]
    },
    "createdAt": {
      "type": "Property",
      "value": <datetime>
    },
    "dataProvider": {
      "type": "Property",
      "value": <value>
    },
    "entityVesrion": {
      "type": "Property",
      "value": "1.0"
    },
    "deviceModel": {
      "type": "Relationship",
      "value": <device model>
    },
    "description": {
      "type": "Property",
      "value": "panasonic network camera"
    },
    "FileName": {
      "type": "Property",
      "value": <file name>
    }
  },
  "HumanDetector": {
    "id": {
      "type": "@id",
      "value": "urn:gnsi-ld:CBPF:HumanDetector"
    },
    "type": {
      "type": "@id",
      "value": "human detector"
    },
    "location": {
      "type": "GeoProperty",
      "value": [
        <latitude>,
        <longitude>
      ]
    },
    "createdAt": {
      "type": "Property",
      "value": <datetime>
    },
    "dataProvider": {
      "type": "Property",
      "value": <value>
    },
    "entityVesrion": {
      "type": "Property",
      "value": "1.0"
    },
    "description": {
      "type": "Property",
      "value": "virtual person finder"
    },
    "softwareVersion": {
      "type": "Property",
      "value": "1.0"
    },
    "DetectHuman": {
      "type": "Property",
      "value": <boolean>
    }
  }
}
```

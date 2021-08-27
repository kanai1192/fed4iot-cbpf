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
  "@context": {
      "type": "StructuredValue",
      "value": [
              "http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
              "https://fed4iot.nz.comm.waseda.ac.jp/cbpfOntology/v1/cbpf-context.jsonld"
               ],
      "metadata": {}
  },
  "@id": "uri:ngsi-ld:CBPF:murcia:1",
  "type": "CBPF",
  "Camera": {
    "id": {
      "type": "@id",
      "value": "urn:ngsi-ld:CBPF:murcia:camera:1"
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
  }
}
```

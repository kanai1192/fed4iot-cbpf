import json
import base64
import socket
import sys
import uuid
from logging import getLogger

from common import common

logger = getLogger(__name__)

HOST = "0.0.0.0"
PORT = 33101
REVSIZE = 1024

def callYOLO(content, interest):

    logger.debug("[callService] start calling service function")

    #if service['input'] == "only content":
    #if content != b'':
    #    contentName = common.getContentName(interest)
    #    temp = json.loads(content)
    #    temp = temp[contentName]['content']['value']
    #    inputData = base64.b64decode(temp.encode('utf-8'))
    #else:
        #if content != b'':
            #inputData = content.encode()
    
    #port = int(service['port'])

    host = HOST
    port = int(PORT)
    revSize = int(REVSIZE)
    inputData = content

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((host, port))

        #sending input data
        if content != b'':
            s.sendall(inputData)
            s.shutdown(1)
        ########

        #receiving data from service function
        revData = b''
        data = s.recv(revSize)
        revData += data

        if sys.getsizeof(data) > revSize:

            while True:
                data = s.recv(revSize)
                #revData += data
                #print(sys.getsizeof(data))
                #if sys.getsizeof(data) < revSize:
                #    revData += data
                #    break
                if not data:
                    break 
                revData += data

        result = revData.decode()

        YOLO = []
        if (result != "null"):

            temp = result.split("_")
            numDetect = len(temp)

            for i in range(numDetect-1):

                temp2 = temp[i].split(",")

                if temp2[2].isdecimal() == True:
                    left = int(temp2[2])
                else:
                    left = 0
                if temp2[3].isdecimal() == True:
                    right = int(temp2[3])
                else:
                    right = 0
                if temp2[4].isdecimal() == True:
                    top = int(temp2[4])
                else:
                    top = 0
                if temp2[5].isdecimal() == True:
                    bottom = int(temp2[5])
                else:
                    top = 0
                width = right - left
                height = bottom - top

                tagName = temp2[0]
                body = {'content': 
                         {'tagID': str(uuid.uuid4()),
                          'probability': float(temp2[1])/100.0,
                          'boundingBox': {'left': left,
                                          'top': top,
                                          'width': width,
                                          'height': height
                                         }
                          }
                        }
                yolo_body = {'tagName': tagName, 'content': body}
                YOLO.append(yolo_body)

        print (YOLO)

        person_list=[]
        car_list=[]
        animal_list=[]
        for i in range(len(YOLO)):
            if YOLO[i]['tagName'] == 'person':
                person_list.append(YOLO[i]['content'])
            if YOLO[i]['tagName'] == 'car':
                car_list.append(YOLO[i]['content'])
            if YOLO[i]['tagName'] == 'truck':
                car_list.append(YOLO[i]['content'])
            if YOLO[i]['tagName'] == 'bus':
                car_list.append(YOLO[i]['content'])
            if YOLO[i]['tagName'] == 'cat':
                animal_list.append(YOLO[i]['content'])
            if YOLO[i]['tagName'] == 'dog':
                animal_list.append(YOLO[i]['content'])
            if YOLO[i]['tagName'] == 'horse':
                animal_list.append(YOLO[i]['content'])

        result = {'person': person_list, 'car': car_list, 'animal': animal_list}
        #########

        logger.debug("[callYOLO] complete")

        return result

def concatData(rawData, procData, funcName):

    logger.debug("[concatData] data serialization")

    BODY = []

    if type(procData) is str:
        procData = json.loads(procData)

    if type(rawData) is str:
        rawData = json.loads(rawData)

    BODY = rawData
    payload = {'type': 'service function',
               'name': funcName,
               'content': {'type': 'Property', 'value': procData}}
    BODY.update({funcName: payload})
    #BODY.update(procData)

    #logger.info("[concatData] data {}".format(BODY))

    logger.debug("[concatData] complete!")

    return BODY

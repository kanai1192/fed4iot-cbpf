#! /usr/bin/python3 
import requests
import json
import base64
import sys

headers = {
        'accept': "application/json",
        'x-m2m-ri': "12345",
        'x-m2m-origin': 'S',
        'content-type': "application/vnd.onem2m-res+json;ty=4",
        'cache-control': "no-cache",
}

payload = {
        'm2m:cin': {
        'con': {
            'cmd-value': 'null',
	    'cmd-qos':'2',
            'cmd-params': 'null'
	    }
        }
}

def main():

    cmd = sys.argv

    if (len(cmd) != 6):
        print("please input propert arguments")
        print("[Usage] $python3 **.py <vsilo ip> <vsilo port> <vthing name> <command> <request image name>")
        print("[example] $python3 **.py vm1 31315 cbpf-murcia/cbpf/01 start test.jpg")
        print("Available commands: <start> and <close>")
        sys.exit(-1)
    else:
        pass

    vsilo_ip = cmd[1]
    vsilo_port = cmd[2]
    v_thing_name = cmd[3].replace('/', ':')
    command = cmd[4]
    request_img = cmd[5]

    end_point = "http://"+vsilo_ip+":"+vsilo_port+"/Mobius/"+v_thing_name+"/"+v_thing_name

    if command == "close":
        act_cmd = end_point + "/" + command
        payload['con']['cmd-value'] = command 

    elif command == "start":
        act_cmd = end_point + "/" + command

        with open(testImgDir+testImgName, 'rb') as f:
            srcImg = f.read()

        binImg = base64.b64encode(srcImg).decode('utf-8')
        params = {"content": {"value": binImg},
                "file name": {"value": testImgName}}

        payload['con']['cmd-value'] = command
        payload['con']['cmd-params'] = params

    else:
        print ("input command is not available") 
        sys.exit(-1)
    
    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

    print(response.text.encode('utf8'))

if __name__ == '__main__':

    main()

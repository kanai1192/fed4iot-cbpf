import subprocess
import time
import json
import sys

###################
file_path = './config.json'
with open(file_path) as f:
    dict_config = json.load(f)

TV_NUM = dict_config['tv num']
SILO_NUM = dict_config['silo num']
TV_ZONE = dict_config['tv zone']
FLAV_ZONE = dict_config['flav zone']
mapping = dict_config['mapping']
FLAV = dict_config['flavour']
tenant = dict_config['tenant']
Master_Controller = dict_config['master controller']

#TV_NUM = 10
#SILO_NUM = 10

#TV_ZONE = 'default'
#TV_ZONE = 'japan'

#FLAV_ZONE = 'default'
#FLAV_ZONE = 'japan'

#mapping = 'OneToOne'
#mapping = 'OneToMany'
#mapping = 'ManyToOne'
#mapping = 'ManyToMany'

### vSilo setting ###

if FLAV == 'mqtt':
    FLAV_NAME = "Raw-base-actuator-wo-http-f"
    base_vSilo_name = 'Silo-mqtt'

if FLAV == 'mobius':
    FLAV_NAME = "Mobius-base-actuator-wo-http-f"
    base_vSilo_name = 'Silo-mobius'

if FLAV == 'mobius2':
    FLAV_NAME = "Mobius2-base-actuator-wo-http-f"
    base_vSilo_name = 'Silo-mobiusv'

if FLAV == 'orion':
    FLAV_NAME = "orion-wo-http-f"
    base_vSilo_name = 'Silo-orion'

if FLAV == 'ngsi-ld':
    FLAV_NAME = 'ngsild-orionld-wo-http-f'
    base_vSilo_name = 'Silo-ngsild'

if FLAV == 'orion-ld':
    FLAV_NAME = 'ngsild-orionld-wo-http-f'
    base_vSilo_name = 'Silo-orionld'

if FLAV == 'scorpio':
    FLAV_NAME = 'ngsild-scorpio-wo-http-f'
    base_vSilo_name = 'Silo-scorpio'

#################

### ThingVisor setting ###

YAML = "../yaml/thingVisor-relay-http-webserver.yaml"
DESC = "replica relay thingvisors"
PARAM = "{'vThingName':'timestamp','vThingType':'timestamp'}"
TV_NAME = "fed4iot/relay-tv"
base_tv_name = 'relay-tv'
label =  'timestamp'
num_vt = 1

END_POINT = 'http://127.0.0.1:8081'

#######

SLEEP = 1

def run():

    #if len(sys.argv) != 3:
    #    print ("Usage: python3 [program] [option] [option2]")
    #    print ("[option]")
    #    print ("add: create TVs & vSilos and add vThings to vSilos")
    #    print ("del: delete vThings, vSilos, and TVs")
    #else:
        #option = sys.argv[1]
        #option2 = sys.argv[2]

        #if option == "add":
        #createAndAdd()
        #elif option == "del":
    deleteAll()
        #else:
        #    print ("Usage: python3 [program] [option]")
        #    print ("[option]")
        #    print ("add: create TVs & vSilos and add vThings to vSilos")
        #    print ("del: delete vThings, vSilos, and TVs")


def createAndAdd():

    createTVs()
    createvSilos()

    #last_tv_name = base_tv_name+str(TV_NUM-1)
    #checkVT(last_tv_name)
    #addEndPointVT()

    #if mapping == 'OneToOne':
    #    oneToOneMap()
    #if mapping == 'OneToMany':
    #    oneToManyMap()
    #if mapping == 'ManyToOne':
    #    manyToOneMap()
    #if mapping == 'ManyToMany':
    #    manyToManyMap()
    
def deleteAll():

    deletevThings()
    destroyvSilos()
    deleteTVs()

def createTVs():

    for i in range(TV_NUM):

        tv_name = base_tv_name + str(i)
        
        #ARG = ['python3', 'f4i.py', 'add-thingvisor', '-i', TV_NAME, '-n', tv_name, '-d', DESC, '-p', PARAM]

        ARG = ['python3', 'f4i.py', 'add-thingvisor', '-c', Master_Controller, '-y', YAML, '-i', TV_NAME, '-n', tv_name, '-d', DESC, '-p', PARAM, '-z', TV_ZONE]


        print (ARG)

        result = subprocess.call(ARG)
        #print (result)

def createvSilos():

    for i in range(SILO_NUM):

        vSilo_name = base_vSilo_name + str(i)

        #ARG = ['python3', 'f4i.py', 'create-vsilo', '-f', FLAV_NAME, '-t', tenant, '-s', vSilo_name]
        ARG = ['python3', 'f4i.py', 'create-vsilo', '-c', Master-Controller, '-f', FLAV_NAME, '-t', tenant, '-s', vSilo_name, '-z', FLAV_ZONE]

        print (ARG)

        result = subprocess.call(ARG)
        #print (result)

def checkVT(tv_name):

    ARG = ['python3', 'f4i.py', 'list-thingvisors', '-c', Master_Controller]

    print (ARG)

    flag = 0

    while True:

        result = subprocess.check_output(ARG)
        result = result.decode()
        dict_tv_info = json.loads(result)

        for i in range(len(dict_tv_info)):
            tv_id = dict_tv_info[i]['thingVisorID']
            if tv_id == tv_name:
                print ("find ThingVisor")
                print ("check vThing...")
                num = len(dict_tv_info[i]['vThings'])
                print (dict_tv_info[i]['vThings'])
                print (num)
                if num != 0:
                    print ("vThing is found")
                    flag = 1
                    break
        if (flag == 1):
            break
        else:
            time.sleep(SLEEP)

def addEndPointVT():

    for i in range(TV_NUM):

        vt_name = base_tv_name + str(i) + '/' + label
        ARG = ['f4i.py', 'set-vthing-endpoint', '-c', Master_Controller, '-v', vt_name, '-e', END_POINT]

        print (ARG)
        result = subprocess.call(ARG)

# no sharing vThings among vSilos
# one to one mapping between vThing and vSilo
def oneToOneMap():

    if TV_NUM <= SILO_NUM:
        NUM = TV_NUM
    else:
        NUM = SILO_NUM

    for i in range(NUM):

        vt_name = base_tv_name + str(i) + '/' + label
        vSilo_name = base_vSilo_name + str(i)

        ARG = ['python3', 'f4i.py', 'add-vthing', '-c', Master_Controller, '-t', tenant, '-s', vSilo_name, '-v', vt_name]
        
        print (ARG)

        result = subprocess.call(ARG)
        #print(result)

def oneToManyMap():

    print ("dummy")


def manyToOneMap():

    for i in range(TV_NUM):

        vt_name = base_tv_name + str(i) + '/' + label
        vSilo_name = base_vSilo_name + str(0)

        ARG = ['python3', 'f4i.py', 'add-vthing', '-c', Master_Controller, '-t', tenant, '-s', vSilo_name, '-v', vt_name]

        print (ARG)

        result = subprocess.call(ARG)
        #print(result)

def manyToManyMap():

    print ("dummy")

def deletevThings():

    if mapping == 'OneToOne':

        if TV_NUM <= SILO_NUM:
            NUM = TV_NUM
        else:
            NUM = SILO_NUM

        for i in range(NUM):

            vt_name = base_tv_name + str(i) + '/' + label
            vSilo_name = base_vSilo_name + str(i)

            ARG = ['python3', 'f4i.py', 'del-vthing', '-c', Master_Controller, '-t', tenant, '-s', vSilo_name, '-v', vt_name]
        
            print (ARG)

            result = subprocess.call(ARG)
            #print(result)


    if mapping == 'manyToOne':

        for i in range(TV_NUM):

            vt_name = base_tv_name + str(i) + '/' + label
            vSilo_name = base_vSilo_name + str(0)

            ARG = ['python3', 'f4i.py', 'del-vthing', '-c', Master_Controller, '-t', tenant, '-s', vSilo_name, '-v', vt_name]
        
            print (ARG)

            result = subprocess.call(ARG)
            #print(result)


def destroyvSilos():

    for i in range(SILO_NUM):

        vSilo_name = base_vSilo_name + str(i)

        ARG = ['python3', 'f4i.py', 'destroy-vsilo', '-c', Master_Controller, '-t', tenant, '-s', vSilo_name]

        print (ARG)

        result = subprocess.call(ARG)
        #print (result)

def deleteTVs():

    for i in range(TV_NUM):

        tv_name = base_tv_name + str(i)
        
        ARG = ['python3', 'f4i.py', 'del-thingvisor', '-c', Master_Controller, '-n', tv_name]

        print (ARG)

        result = subprocess.call(ARG)
        #print (result)

def jsonReader(file_path):

    with open(file_path) as f:
        dict_data = json.load(f)

    return dict_data


if __name__ == '__main__':

    run()

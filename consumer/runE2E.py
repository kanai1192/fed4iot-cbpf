import subprocess
import json
import time
import os
import signal
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
deploy_method = dict_config['deploy']
FLAV = dict_config['flavour']
EXP_TIME = dict_config['exp time']
tenant = dict_config['tenant']
mobius_silo = dict_config['mobius silo']
con_ip = dict_config['con ip']
producer_rate = dict_config['producer rate']
Master_Controller = dict_config['master controller']

if deploy_method == 'k8s':
    pro_ip = '192.168.11.25'
    vsilo_ip = '192.168.11.25'
    #con_ip = 'vm5'
else:
    pro_ip = '59.106.217.215'
    vsilo_ip = '59.106.217.215'
    #con_ip = '59.106.217.215'

### Exp time must be multiples of 10
SLEEP = 10
####

base_tv_name = 'relay-tv'
label = 'timestamp'
tv_port_key = '8089/tcp'
num_vt = 0

producer = 'producerv2.py'
api = 'notify'
rate = 1

if FLAV == 'mqtt':
    base_vsilo_name = 'Silo-mqtt'
    vsilo_port_key = '1883/tcp'
    consumer = 'consumerMQTTv2.py'

if FLAV == 'mobius':
    base_vsilo_name = 'Silo-mobius'
    consumer = 'consumerOneM2Mv2.py'
    if mobius_silo == 'mqtt':
        vsilo_port_key = '1883/tcp'
        mobius_silo_protocol = 'MQTT'
    elif mobius_silo == 'http':
        vsilo_port_key = '7579/tcp'
        mobius_silo_protocol = 'HTTP'
    else:
        print ("please specify mobius silo protocol correctly")
        sys.exit(1)

if FLAV == 'mobius2':
    base_vsilo_name = 'Silo-mobiusv'
    consumer = 'consumerMobius2.py'
    if mobius_silo == 'mqtt':
        vsilo_port_key = '1883/tcp'
        mobius_silo_protocol = 'MQTT'
    elif mobius_silo == 'http':
        vsilo_port_key = '7579/tcp'
        mobius_silo_protocol = 'HTTP'
    else:
        print ("please specify mobius silo protocol correctly")
        sys.exit(1)

if FLAV == 'orion':
    base_vsilo_name = 'Silo-orion'
    vsilo_port_key = '1026/tcp'
    consumer = 'consumerNGSIv2.py'
    type_name = 'timestamp'

if FLAV == 'orion-ld':
    base_vsilo_name = 'Silo-orionld'
    vsilo_port_key = '1026/tcp'
    consumer = 'consumerORIONLDv2.py'
    type_name = 'timestamp'

if FLAV == 'scorpio':
    base_vsilo_name = 'Silo-scorpio'
    vsilo_port_key = '9090/tcp'
    consumer = 'consumerSCORPIOv2.py'
    type_name = 'timestamp'

NOTIFY_PORT = 33101

def run():

    print ("run producer")
    pro_pid_list = runProducer()

    time.sleep(2)

    print ("run consumer")

    if FLAV == 'mqtt':
        con_pid_list = runConsumerMQTT()

    if FLAV == 'mobius' or FLAV == 'mobius2':
        con_pid_list = runConsumerOneM2M()

    if FLAV == 'orion':
        con_pid_list = runConsumerNGSI()

    if FLAV == 'orion-ld' or FLAV == 'scorpio':
        con_pid_list = runConsumerNGSILD()

    time.sleep(5)

    print ("running...")
    print ("please wait until the experiment is finished...")
    print ("Experiment time: {} sec".format(EXP_TIME))

    for i in range(0, EXP_TIME, SLEEP):
        print ("{} sec...".format(i))
        time.sleep(int(SLEEP))

    print ("The experiment is finished")
    print ("Killing the process")

    for i in range(len(pro_pid_list)):
        pid = pro_pid_list[i]
        print ("kill producer PID: {}".format(pid))
        os.kill(pid, signal.SIGTERM)

    for i in range(len(con_pid_list)):
        pid = con_pid_list[i]
        print ("kill consumer PID: {}".format(pid))
        os.kill(pid, signal.SIGTERM)

    print ("end")

def runProducer():

    ARG = ['python3', 'f4i.py', 'list-thingvisors', '-c', Master_Controller]

    print (ARG)

    result = subprocess.check_output(ARG)
    result = result.decode()
    dict_tv_info = json.loads(result)

    pid_list = []

    for j in range(TV_NUM):

        tv_name = base_tv_name + str(j)

        for i in range(len(dict_tv_info)):
            tv_id = dict_tv_info[i]['thingVisorID']

            if tv_id == tv_name :

                vt_name = dict_tv_info[i]['vThings'][num_vt]['id']
                tv_port = dict_tv_info[i]['port'][tv_port_key]

                print ('{} {}'.format(vt_name, tv_port))

                producer_end = 'http://'+pro_ip+':'+tv_port+'/'+api
                ARG = ['python3', producer, '-t', producer_end, '-r', str(producer_rate)]
                print (ARG)

                result = subprocess.Popen(ARG)
                pid_list.append(result.pid)
                #print (result)

    return pid_list

def runConsumerMQTT():

    ARG = ['python3', 'f4i.py', 'inspect-tenant', '-c', Master_Controller, '-t', tenant]

    print (ARG)

    result = subprocess.check_output(ARG)
    result = result.decode()
    dict_tenant_info = json.loads(result)
    dict_vsilo_info = dict_tenant_info['vSilos']
    dict_vthing_info = dict_tenant_info['vThings']

    pid_list = []

    if mapping == 'OneToOne':

        for j in range(SILO_NUM):

            tar_vsilo_name = base_vsilo_name + str(j)

            for i in range(len(dict_vsilo_info)):

                vsilo_name = dict_vsilo_info[i]['vSiloName']

                if vsilo_name == tar_vsilo_name:
                    vsilo_port = dict_vsilo_info[i]['port'][vsilo_port_key]
                    vsilo_id = dict_vsilo_info[i]['vSiloID']

                    for j in range(len(dict_vthing_info)):
                        if vsilo_id == dict_vthing_info[j]['vSiloID']:
                            vt_name = dict_vthing_info[j]['vThingID']

                    print ('{} {} {}'.format(vsilo_name, vsilo_port, vt_name))

            ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-v', vt_name, '-t', tenant] 
            print (ARG)

            result = subprocess.Popen(ARG)
            #print (result)

            pid_list.append(result.pid)

    if mapping == 'ManyToOne':

        tar_vsilo_name = base_vsilo_name + str(0)

        for i in range(len(dict_vsilo_info)):

            vsilo_name = dict_vsilo_info[i]['vSiloName']

            if vsilo_name == tar_vsilo_name:
                vsilo_port = dict_vsilo_info[i]['port'][vsilo_port_key]
                vsilo_id = dict_vsilo_info[i]['vSiloID']

        for j in range(len(dict_vthing_info)):
            if vsilo_id == dict_vthing_info[j]['vSiloID']:
                vt_name = dict_vthing_info[j]['vThingID']

                print ('{} {} {}'.format(vsilo_name, vsilo_port, vt_name))

                ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-v', vt_name, '-t', tenant] 
                print (ARG)

                result = subprocess.Popen(ARG)
                #print (result)

                pid_list.append(result.pid)

    return pid_list

def runConsumerOneM2M():

    ARG = ['python3', 'f4i.py', 'inspect-tenant', '-c', Master_Controller, '-t', tenant]

    print (ARG)

    result = subprocess.check_output(ARG)
    result = result.decode()
    dict_tenant_info = json.loads(result)
    dict_vsilo_info = dict_tenant_info['vSilos']
    dict_vthing_info = dict_tenant_info['vThings']

    pid_list = []

    if mapping == 'OneToOne':

        notify_port = NOTIFY_PORT

        for j in range(SILO_NUM):

            tar_vsilo_name = base_vsilo_name + str(j)

            for i in range(len(dict_vsilo_info)):

                vsilo_name = dict_vsilo_info[i]['vSiloName']

                if vsilo_name == tar_vsilo_name:
                    vsilo_port = dict_vsilo_info[i]['port'][vsilo_port_key]
                    vsilo_id = dict_vsilo_info[i]['vSiloID']

                    for j in range(len(dict_vthing_info)):
                        if vsilo_id == dict_vthing_info[j]['vSiloID']:
                            vt_name = dict_vthing_info[j]['vThingID']

                    print ('{} {} {}'.format(vsilo_name, vsilo_port, vt_name))

            if (mobius_silo_protocol == 'HTTP'):
                ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-pm', '1883', '-m', mobius_silo_protocol, '-nuri', 'http://'+con_ip+':'+str(notify_port)+'/notify',  '-v', vt_name] 

            elif (mobius_silo_protocol == 'MQTT'):
                ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-pm', '1883', '-m', mobius_silo_protocol, '-v', vt_name] 
   
            print (ARG)

            result = subprocess.Popen(ARG)
            print (result)

            pid_list.append(result.pid)
            notify_port = notify_port + 1


    if mapping == 'ManyToOne':

        notify_port = NOTIFY_PORT
        tar_vsilo_name = base_vsilo_name + str(0)

        for i in range(len(dict_vsilo_info)):

            vsilo_name = dict_vsilo_info[i]['vSiloName']

            if vsilo_name == tar_vsilo_name:
                vsilo_port = dict_vsilo_info[i]['port'][vsilo_port_key]
                vsilo_id = dict_vsilo_info[i]['vSiloID']

        for j in range(len(dict_vthing_info)):
            if vsilo_id == dict_vthing_info[j]['vSiloID']:
                vt_name = dict_vthing_info[j]['vThingID']

                print ('{} {} {}'.format(vsilo_name, vsilo_port, vt_name))

                if (mobius_silo_protocol == 'HTTP'):
                    ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-pm', '1883', '-m', mobius_silo_protocol, '-nuri', 'http://'+con_ip+':'+str(notify_port)+'/notify',  '-v', vt_name]

                elif (mobius_silo_protocol == 'MQTT'):
                    ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-pm', '1883', '-m', mobius_silo_protocol, '-v', vt_name]

                print (ARG)

                result = subprocess.Popen(ARG)
                #print (result)

                pid_list.append(result.pid)
                notify_port = notify_port + 1

    return pid_list

def runConsumerNGSI():

    ARG = ['python3', 'f4i.py', 'inspect-tenant', '-c', Master_Controller, '-t', tenant]

    print (ARG)

    result = subprocess.check_output(ARG)
    result = result.decode()
    dict_tenant_info = json.loads(result)
    dict_vsilo_info = dict_tenant_info['vSilos']
    dict_vthing_info = dict_tenant_info['vThings']

    pid_list = []

    if mapping == 'OneToOne':

        notify_port = NOTIFY_PORT

        for j in range(SILO_NUM):

            tar_vsilo_name = base_vsilo_name + str(j)

            for i in range(len(dict_vsilo_info)):

                vsilo_name = dict_vsilo_info[i]['vSiloName']

                if vsilo_name == tar_vsilo_name:
                    vsilo_port = dict_vsilo_info[i]['port'][vsilo_port_key]
                    vsilo_id = dict_vsilo_info[i]['vSiloID']

                    for j in range(len(dict_vthing_info)):
                        if vsilo_id == dict_vthing_info[j]['vSiloID']:
                            vt_name = dict_vthing_info[j]['vThingID']

                    print ('{} {} {}'.format(vsilo_name, vsilo_port, vt_name))

            ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-nuri', 'http://'+con_ip+':'+str(notify_port)+'/notify',  '-v', vt_name, '-t', type_name] 
            print (ARG)

            result = subprocess.Popen(ARG)
            print (result)

            pid_list.append(result.pid)
            notify_port = notify_port + 1

    if mapping == 'ManyToOne':

        tar_vsilo_name = base_vsilo_name + str(0)
        notify_port = NOTIFY_PORT

        for i in range(len(dict_vsilo_info)):

            vsilo_name = dict_vsilo_info[i]['vSiloName']

            if vsilo_name == tar_vsilo_name:
                vsilo_port = dict_vsilo_info[i]['port'][vsilo_port_key]
                vsilo_id = dict_vsilo_info[i]['vSiloID']

        for j in range(len(dict_vthing_info)):
            if vsilo_id == dict_vthing_info[j]['vSiloID']:
                vt_name = dict_vthing_info[j]['vThingID']

                print ('{} {} {}'.format(vsilo_name, vsilo_port, vt_name))

                ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-nuri', 'http://'+con_ip+':'+str(notify_port)+'/notify',  '-v', vt_name, '-t', type_name] 
                print (ARG)

                result = subprocess.Popen(ARG)
                #print (result)

                pid_list.append(result.pid)
                notify_port = notify_port + 1

    return pid_list

def runConsumerNGSILD():

    ARG = ['python3', 'f4i.py', 'inspect-tenant', '-c', Master_Controller, '-t', tenant]

    print (ARG)

    result = subprocess.check_output(ARG)
    result = result.decode()
    dict_tenant_info = json.loads(result)
    dict_vsilo_info = dict_tenant_info['vSilos']
    dict_vthing_info = dict_tenant_info['vThings']

    pid_list = []

    if mapping == 'OneToOne':

        notify_port = NOTIFY_PORT

        for j in range(SILO_NUM):

            tar_vsilo_name = base_vsilo_name + str(j)

            for i in range(len(dict_vsilo_info)):

                vsilo_name = dict_vsilo_info[i]['vSiloName']

                if vsilo_name == tar_vsilo_name:
                    vsilo_port = dict_vsilo_info[i]['port'][vsilo_port_key]
                    vsilo_id = dict_vsilo_info[i]['vSiloID']

                    for j in range(len(dict_vthing_info)):
                        if vsilo_id == dict_vthing_info[j]['vSiloID']:
                            vt_name = dict_vthing_info[j]['vThingID']

                    print ('{} {} {}'.format(vsilo_name, vsilo_port, vt_name))

            ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-nuri', 'http://'+con_ip+':'+str(notify_port)+'/notify',  '-v', vt_name, '-t', type_name] 
            print (ARG)

            result = subprocess.Popen(ARG)
            print (result)

            pid_list.append(result.pid)
            notify_port = notify_port + 1

    if mapping == 'ManyToOne':

        tar_vsilo_name = base_vsilo_name + str(0)
        notify_port = NOTIFY_PORT

        for i in range(len(dict_vsilo_info)):

            vsilo_name = dict_vsilo_info[i]['vSiloName']

            if vsilo_name == tar_vsilo_name:
                vsilo_port = dict_vsilo_info[i]['port'][vsilo_port_key]
                vsilo_id = dict_vsilo_info[i]['vSiloID']

        for j in range(len(dict_vthing_info)):
            if vsilo_id == dict_vthing_info[j]['vSiloID']:
                vt_name = dict_vthing_info[j]['vThingID']

                print ('{} {} {}'.format(vsilo_name, vsilo_port, vt_name))

                ARG = ['python3', consumer, '-s', vsilo_ip, '-p', vsilo_port, '-nuri', 'http://'+con_ip+':'+str(notify_port)+'/notify',  '-v', vt_name, '-t', type_name] 
                print (ARG)

                result = subprocess.Popen(ARG)
                #print (result)

                pid_list.append(result.pid)
                notify_port = notify_port + 1

    return pid_list


if __name__ == '__main__':

    run()

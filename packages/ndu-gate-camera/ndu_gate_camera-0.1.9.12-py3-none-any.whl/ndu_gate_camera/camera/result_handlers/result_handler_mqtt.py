import os
import socket
import time

# import paho.mqtt.client as mqtt
import json

import paho.mqtt.client as mqttClient
from ndu_gate_camera.utility import constants


class ResultHandlerMqtt:
    '''
        Cihaz verilerinin NDU platformuna MQTT APİ üzerinden gönderilmesi
    '''

    def __init__(self, access_token, mqtt_obj):
        host = mqtt_obj.get("host")
        self.host = host
        self.port = mqtt_obj.get("port")
        self.connected_devices = {}
        self.connected = False
        self.client = mqttClient.Client()
        self.client.username_pw_set(access_token)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.disconnected_data = []
        # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
        try:
            self.client.connect(host, mqtt_obj.get("port"), 5)
            self.client.loop_start()
            self.connected = True
        except socket.error:
            print("can not connect mqtt broker!")
            port = mqtt_obj.get("port")
            self.try_to_connect(host, port)
            # TODO - bağlanamasa belli aralıklara bağlanmayı tekrar denesin, bağlanamadığı sırada veri gelirse o veriyi hafızada belirli bir süre/miktar tutmalı.
            #  bağlantı oluşur oluşmaz bu biriken veriler de gönderilmelidir.

    def try_to_connect(self, host, port):
        try:
            self.client.connect(host, port, 60)
            self.client.loop_start()
        except socket.error:
            import time
            print("can not connect mqtt broker, trying again in 15 seconds")
            time.sleep(15)
            self.try_to_connect(self.host, self.port)

    def on_connect(self, client, userdata, flags, rc):
        print('connected')
        self.connected = True
        self.disconnected_data = self.load_data(constants.LOCAL_RESULTS_PATH)

        if len(self.disconnected_data) > 0:
            self.publish_historic_data(self.disconnected_data)
            self.disconnected_data = []
            self.clear_file(constants.LOCAL_RESULTS_PATH)

    def clear_file(self, filename):
        open(filename, 'w').close()

    def publish_historic_data(self, results):
        for result in results:
            self.client.publish('v1/gateway/telemetry', json.dumps(result), 1)

    def on_disconnect(self, client, userdata, rc=0):
        print('disconnected')
        self.connected = False

    def send_connect_request(self, device_name):
        mqtt_data = {"device": device_name}
        self.client.publish('v1/gateway/connect', json.dumps(mqtt_data), 1)
        self.connected_devices[device_name] = True

    def send_disconnect_request(self, device_name):
        mqtt_data = {"device": device_name}
        self.client.publish('v1/gateway/disconnect', json.dumps(mqtt_data), 1)
        self.connected_devices.pop(device_name)

    def save_result(self, results, device=None, runner_name=None, data_type='telemetry'):
        if self.connected is True:
            if self.connected_devices.get(device) is None:
                self.send_connect_request(device)

            if data_type == 'telemetry':
                self.send_telemetry(device, results)
            elif data_type == 'attribute':
                self.send_attribute(device, results)
        else:
            self.store_local(results, constants.LOCAL_RESULTS_PATH, device)

    def store_local(self, results, filename, device):
        file = open(filename, 'a')
        mqtt_data = {
            device: []
        }
        for result in results:
            if result is None:
                continue
            data = result.get(constants.RESULT_KEY_DATA, None)

            if data is None:
                continue

            single_data = {}
            single_data['ts'] = round(time.time()) * 1000
            single_data['values'] = {}
            for key in data:
                if data[key] is not None:
                    single_data['values'][key] = data[key]
            # mqtt_data[device].append(time.time())
            mqtt_data[device].append(single_data)
            file.write(json.dumps(mqtt_data))
            file.write("\n")
        file.close()

    def load_data(self, filename):
        result_list = []
        try:
            with open(filename) as f:
                for line in f:
                    # get json object
                    json_object = json.loads(line)
                    # add json object to list
                    result_list.append(json_object)
        except:
            f = open(filename, 'w+')
        return result_list

    def send_telemetry(self, device, results):
        try:
            mqtt_data = {
                device: []
            }
            # if mqtt_data.get(device) is None:
            #     mqtt_data['device'] = 'device'

            for result in results:
                if result is None:
                    continue
                data = result.get(constants.RESULT_KEY_DATA, None)

                if data is None:
                    continue

                single_data = {}
                for key in data:
                    if data[key] is not None:
                        single_data[key] = data[key]

                mqtt_data[device].append(single_data)
            if not len(mqtt_data[device]) == 0:
                self.client.publish('v1/gateway/telemetry', json.dumps(mqtt_data), 1)

        except socket.error:
            print('Cannot send data due to connection lost')

        except KeyError:
            print('Exception while saving result, key error')

    def send_attribute(self, device, results):
        try:
            mqtt_data = {
                device: {}
            }

            for result in results:
                if result is None:
                    continue
                data = result.get(constants.RESULT_KEY_DATA, None)

                if data is None:
                    continue

                for key in data:
                    if data[key] is not None:
                        mqtt_data[device][key] = data[key]

            if not len(mqtt_data[device]) == 0:
                self.client.publish('v1/gateway/attributes', json.dumps(mqtt_data), 1)
        except KeyError:
            print('Exception while saving result, key error')

    def dispose(self):
        # TODO - disconnect devices
        pass

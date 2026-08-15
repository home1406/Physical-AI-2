import paho.mqtt.client as mqtt
import time
 
received_count = {0: 0, 1: 0, 2: 0}
 
def on_message(client, userdata, msg):
    qos = int(msg.topic.split("/")[-1])
    received_count[qos] += 1
 
sub = mqtt.Client()
sub.on_message = on_message
sub.connect("localhost", 1883)
for qos in (0, 1, 2):
    sub.subscribe(f"test/qos/{qos}", qos=qos)
sub.loop_start()
 
pub = mqtt.Client()
pub.connect("localhost", 1883)
for qos in (0, 1, 2):
    for i in range(100):
        pub.publish(f"test/qos/{qos}", payload=f"msg-{i}", qos=qos)
    time.sleep(2)  # 네트워크를 이 사이에 일부러 끊었다 연결해본다
 
time.sleep(3)
for qos, count in received_count.items():
    print(f"QoS {qos}: {count}/100 수신")
 
sub.loop_stop()

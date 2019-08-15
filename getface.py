# coding:utf-8
import dlib
import cv2
import numpy
from socket import socket, AF_INET, SOCK_DGRAM
from socket_server import  upper_socket_server
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read('/home/lixuan/camera.conf')
choose = int(cf.get('db','db_getface'))
class socket_sender(object):
    def __init__(self, addr, port):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.addr = addr
        self.port = port

    def send_data(self, data):
        self.sock.sendto(data, (self.addr, self.port))

sender_to_voice = socket_sender('localhost',20000)

def preprocess_image(src):
    # scale the image
    NETWORK_WIDTH = 160
    NETWORK_HEIGHT = 160
    preprocessed_image = cv2.resize(src, (NETWORK_WIDTH, NETWORK_HEIGHT))

    #convert to RGB

    # return the preprocessed image
    return preprocessed_image

sender_to_data = sender_to_voice.send_data("cmd:getname")
print("请输入您的名字:")
#name = raw_input("请输入您的名字:\n")
##############udp server block  ##########
address = ('127.0.0.1', 20001)  
s = socket(AF_INET, SOCK_DGRAM)  
s.bind(address) 
data, addr = s.recvfrom(2048)

print data
s.close()
name = data
##############udp server block  ########## 
cap = cv2.VideoCapture(choose)
detector = dlib.get_frontal_face_detector()
while True:
    ret,frame = cap.read()
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if len(detector(gray_img,1))==1:
        if ret ==True:
            #frame =preprocess_image(frame)
            cv2.imwrite('./'+name+'.jpg',frame)
            sender_to_voice.send_data("录制完成")
            break
cap.release()
'''
待改进加一个人脸矫正,人脸抠图
'''

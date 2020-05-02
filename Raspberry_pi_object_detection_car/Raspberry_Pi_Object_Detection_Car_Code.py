import cv2
import numpy as np
import cv2.cv as cv
import time
import serial
import RPi.GPIO as gpio
import RPi.GPIO as GPIO
gpio.setmode(gpio.BCM)
gpio.setup(27,gpio.OUT)
gpio.setup(24,gpio.OUT)
gpio.setup(17,gpio.OUT)
gpio.setup(23,gpio.OUT)
cap=cv2.VideoCapture(0)
width,height=cap.get(3),cap.get(4)
print 'frame wid and hei:',width,height
while(1):
	ret,frame = cap.read()
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	lower_orange = np.array([10,116,210])
	upper_orange = np.array([79,255,255])
	mask = cv2.inRange(hsv,lower_orange,upper_orange)
	res = cv2.bitwise_and(frame,frame,mask=mask)
	kernel=np.ones((5,5),np.uint8)
	erosion = cv2.erode(mask,kernel,iterations = 1)
	dilation = cv2.dilate(mask,kernel,iterations = 1)
	opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	closing = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)	
	circles = cv2.HoughCircles(closing,cv.CV_HOUGH_GRADIENT,2,120,
	param1=70,param2=50,minRadius=0,maxRadius=0)
	if circles is not None:
                for i in circles[0,:]:
                        cv2.circle(frame,(int(round(i[1])),int(round(i[1]))),5,(0,255,0),5)
                        cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(255,0,0),1)
						cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),5,(0,0,255),5)
                        x=int(round(i[0]))
                        y=int(round(i[1]))
                        z=int(round(i[2]))
                        print('x=',x,'y=',y,'z=',z)
                        a=int(round(i[1]))
                        if z>=80:
                                print('stop!!!!,the ball is in my hand')
                                GPIO.setmode(GPIO.BCM)
                                GPIO.setup(2,GPIO.OUT)
                                pwm=GPIO.PWM(2,50)
                                GPIO.setup(3,GPIO.OUT)
                                pwm1=GPIO.PWM(3,50)
                                pwm.start(5)
                                pwm1.start(5)
                                pwm.ChangeDutyCycle(4)
                                pwm1.ChangeDutyCycle(4)
                                time.sleep(2)
                                pwm.ChangeDutyCycle(8)
                                pwm1.ChangeDutyCycle(8)
                                time.sleep(2)
                                pwm.stop()
                                pwm1.stop()
                                gpio.output(24,False)
                                gpio.output(27,False)
                                time.sleep(1)
                                break
                        elif z<20:
                                print('go front for two seconds')
                                gpio.output(24,False)
                                gpio.output(27,True)
                                time.sleep(0.1)
                                gpio.output(24,True)
                                gpio.output(27,True)
                                time.sleep(0.5)
                                gpio.output(27,False)
                                gpio.output(24,False)
                                time.sleep(2)
                                break
                                
                        else :
                                print('go front for two seconds')
                                gpio.output(24,False)
                                gpio.output(27,True)
                                time.sleep(0.2)
                                gpio.output(24,True)
                                gpio.output(27,True)
                                time.sleep(0.1)
                                gpio.output(27,False)
                                gpio.output(24,False)
                                time.sleep(2)
                                break
                                
        else:
                print('move left or right')
                gpio.output(24,True)
                gpio.output(27,False)
                gpio.output(17,True)
                gpio.output(23,False)
                time.sleep(0.015)
                gpio.output(24,False)
                gpio.output(27,False)
                gpio.output(17,False)
                gpio.output(23,False)
                time.sleep(0.1)
	cv2.imshow('tracking',frame)
	cv2.imshow('result',res)
	k = cv2.waitKey(5) & 0xFF
	if k==27:
		break
cv2.destroyAllWindows()
cap.release()


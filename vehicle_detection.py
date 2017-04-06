# -*- coding: utf-8 -*-

import cv2
import time
import imutils
#print(cv2.__version__)


def withinRange(X1,X2,Y1,Y2):
    MAX_X_DIFF = 65
    MAX_Y_DIFF = 25
    if((abs(X1-X2) < MAX_X_DIFF) and (abs(Y1-Y2) < MAX_Y_DIFF)):
        return True
    else:
        return False

def CarListLength():
    return CarList.__len__()

class Car(object):

    def __init__(self, num, x, y, w, h, direction, frame, found, active):
        self.num = num
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.direction = direction
        self.frame = frame
        self.found = found
        self.active = active
        self.xc = x + (w/2)
        self.yc = y + (h/2)
        
    def Update(self, x, y, w, h, direction, frame, found, active):
        #self.num = num
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.direction = direction
        self.frame = frame
        self.found = found
        self.active = active
        self.xc = x + (w/2)
        self.yc = y + (h/2)

    def getNum(self):
        return self.num
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getW(self):
        return self.w
    def getH(self):
        return self.h
    def getDirection(self):
        return self.direction
    def getFrame(self):
        return self.frame
    def getFound(self):
        return self.found
    def getActive(self):
        return self.active
    def getXc(self):
        return self.xc
    def getYc(self):
        return self.yc

    def setActive(self, active):
        self.active = active
    def setFound(self, found):
        self.found = found
    def setFrame(self, frame):
        self.frame = frame


STARTX_LEFT = 80
STARTX_RIGHT = 720
ENDX_LEFT = 120
ENDX_RIGHT = 680
missingFrame = 0
CarList = []
Frame = 0
Errors = 0
NumCar = 1
timeTotal = 0
FrameNum = 0

cascade_src = 'cascade13.xml' #Path to Haar Cascade Model
video_src = 'dataset/vid1_clip.mp4' #Path to video file

cap = cv2.VideoCapture(video_src) #Load video file
car_cascade = cv2.CascadeClassifier(cascade_src) #Load Haar Cascade Model


while True:
    ret, img = cap.read()
    Frame += 1
            
    #Handle empty frame or end of video feed    
    if (type(img) == type(None)):
        missingFrame += 1
        if(missingFrame<100):
            print "MISSING FRAME"
        elif(missingFrame > 500):
            timePerFrame = timeTotal/FrameNum
            print "Seconds per Frame:" + str(timePerFrame)
            cv2.destroyAllWindows()
            break

    #Downsample video and begin processing frame by frame
    elif(((Frame%6) == 0) and (Frame>11)):
        missingFrame = 0
        FrameNum += 1
        resize = imutils.resize(img, width = 800) #resize image
        gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY) #convert to grayscale

        time1 = time.time()
        cars = car_cascade.detectMultiScale(gray) #Use model to detect location of cars
        
        cars = list(cars) #convert from array to list format

        for carObject in CarList:
            carObject.setFound(False)

        for (x,y,w,h) in cars:
            xc = x + (w/2)
            yc = y + (h/2)

            #Remove car detected twice (two bounding boxes for one car)
            carDuplicate = 0
            for (x2,y2,w2,h2) in cars:
                if((x2>x) and (x2<(x+w)) and (y2>y) and (y2<(y+h))):
                    #cv2.waitKey()
                    del cars[carDuplicate]
                    break
                if((x>x2) and (x<(x2+w2)) and (y>y2) and (y<(y2+h2))):
                    #cv2.waitKey()
                    del cars[carDuplicate]
                    break
                carDuplicate+=1

            cv2.rectangle(resize,(x,y),(x+w,y+h),(0,0,255),2) #Display bounding box on image at car's location


            if(Frame == 12):
                detectedCar = Car(NumCar, x, y, w, h,'INDEFINITE', Frame, True, True)
                CarList.append(detectedCar)
                NumCar += 1
            else:
                foundCar = False
                for prevCar in CarList:
                    if(withinRange(prevCar.getXc(), xc, prevCar.getYc(), yc)):
                        if(prevCar.getActive() == True):
                            print "FOUND BETWEEN FRAMES!!!"
                            print "X: "+ str(prevCar.getXc()) + " -> " + str(xc)
                            print "Y: " + str(prevCar.getYc()) + " -> " + str(yc)
                            if(prevCar.getXc() < xc):
                                prevCar.Update(x,y,w,h,'RIGHT',Frame, True, True)
                            elif(prevCar.getXc() > xc):
                                prevCar.Update(x,y,w,h,'LEFT',Frame, True, True)
                            elif(prevCar.getXc() == xc):
                                prevCar.Update(x,y,w,h,'INDEFINITE',Frame, True, True)
                            foundCar = True
                            break
                if(foundCar != True):
                    if((xc < STARTX_LEFT) or (xc > STARTX_RIGHT)):
                        newCar = Car(NumCar, x, y, w, h, 'INDEFINITE', Frame, True, True)
                        CarList.append(newCar)
                        NumCar += 1
                        print "New Car not found in Frame"
                        print "New Car X: " + str(newCar.getXc())
                        print "New Car Y: " + str(newCar.getYc())
                        #cv2.waitKey()
                    else:
                        print "New car appeared in middle of screen"
                        #cv2.waitKey()
        
        for carObject in CarList:
            if((carObject.getFound() == False) and (carObject.getActive() == True)):
                if((carObject.getDirection() == 'RIGHT') and (carObject.getXc() > ENDX_RIGHT)):
                    print "Car Left Screen on Right Side"
                    #cv2.waitKey()
                    carObject.setActive(False)
                elif((carObject.getDirection() == 'LEFT') and (carObject.getXc() < ENDX_LEFT)):
                    print "Car Left Screen on Left Side"
                    #cv2.waitKey()
                    carObject.setActive(False)
                else:
                    carObject.setActive(False)
                    print "Car Undetected in Middle"
                    #cv2.waitKey()

        for carObject in CarList:
            if((carObject.getFound() == True) and (carObject.getActive() == True)):
                carX = carObject.getX()
                carW = carObject.getW()
                carY = carObject.getY()
                cv2.putText(resize, str(carObject.getNum()), (carX + carW, carY - 10), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 255), 1) 
                    
        

        print "Num of Cars: " + str(CarListLength())
        cv2.imshow('video', resize)

        time2 = time.time()
        timeTotal = timeTotal + (time2 - time1)

        cv2.waitKey(25)
        if cv2.waitKey(33) == 27:
            break

cv2.destroyAllWindows()

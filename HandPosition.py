from Triangle import *
import time
import Keys
import cv2

class Rectangle:

    def __init__(self, p1 : Point , p2 : Point , p3 : Point , p4 : Point)  :
        #coordinates
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3 
        self.p4 = p4
        # Position var is to know if the Rectangle has a landmark on it 
        self.Position = 0
        #time var is to know where the landmark has be pointing to that direction 
        self.Time = 0
    
    def Reset(self):
        """Reset the time and position variables , we usually call it after making a detection"""
        self.Position = 0 
        self.Time = 0

    def setTime(self):
        """ set current position time """
        self.Time = time.time()

    def getTime(self) -> int :
        """ get the current object time"""
        return self.Time

    def getPosition(self) :
        """ get the current hand position on the screen (handland mark)"""    
        return self.Position

    def setPosition(self, current_position):
        """ set the coordinate of position on the screen """
        self.Position = current_position

    def In(self , p : Point):
        """ if a p point is in a given shape 'Rectangle'"""
        if (p.x >= self.p1.x and p.y >= self.p1.y ): # if p1 is before p1
            if (self.p2.x >= p.x and self.p2.y <= p.y): # if  p2 is after p
                if(p.x >= self.p3.x and  p.y<= self.p3.y): #if p3 if after p
                    if(self.p4.x >= p.x and self.p4.y >= p.y): #if p4 is after p
                        #Traitement 
                        return True
        return False

class HandPosition :

    # SCREEN DIMENSIONS
    WIDTH = 0
    HEIGHT = 0
    # SCREEN ZONE
    UP = Rectangle
    DOWN = None
    LEFT = None
    RIGHT = None
    #ERROR (EACH ZONE OCCUPIED SCALE*100 of the screen) : to adjust
    SCALE = 0.25
    #delay time every movement out of the range is not considered : delay between moving from (up->down) 
    TIMEDELAY = 0.5

    @staticmethod
    def SetDimensions(Width,Height):
        """Set the image dimensions """
        HandPosition.WIDTH = Width 
        HandPosition.HEIGHT = Height
        print("WEBCAME = [{},{}]".format(HandPosition.WIDTH,HandPosition.HEIGHT))

    def setScale(self,new_scale):
        """Change the scale by default it would take 10% of the screen dimensions"""
        self.SCALE = new_scale

    @staticmethod
    def getScreenSize():
        """ return the screen dimensions"""
        return HandPosition.WIDTH , HandPosition.HEIGHT

    def setPositions(self):
        """ set 4 positions : (up , down , right , left) : Rectangle"""

        p1 = Point(0,0)  
        p2 = Point(int(HandPosition.WIDTH),0) 
        p3 = Point(0,int(HandPosition.SCALE*HandPosition.HEIGHT))
        p4 = Point(int(HandPosition.WIDTH),int(HandPosition.SCALE*HandPosition.HEIGHT))

        self.UP = Rectangle(p1,p2,p3,p4)

    
        ##################################################################################################

        p5 = Point(0,int((1-HandPosition.SCALE)*HandPosition.HEIGHT))
        p6 = Point(int(HandPosition.WIDTH),int((1-HandPosition.SCALE)*HandPosition.HEIGHT))
        p7 = Point(0,int(HandPosition.HEIGHT))
        p8 = Point(int(HandPosition.WIDTH),int(HandPosition.HEIGHT))

        self.DOWN = Rectangle(p5,p6,p7,p8)

        ##################################################################################################

        p9 = p1
        p10 = Point(int(HandPosition.WIDTH*HandPosition.SCALE),0)
        p11 = p7
        p12 = Point(int(HandPosition.WIDTH*HandPosition.SCALE),int(HandPosition.HEIGHT))

        self.LEFT = Rectangle(p9,p10,p11,p12)

        ##################################################################################################

        p13 = Point(int((1-HandPosition.SCALE)*HandPosition.WIDTH),0)
        p14 = p2
        p15 = Point(int((1-HandPosition.SCALE)*HandPosition.WIDTH),int(HandPosition.HEIGHT))
        p16 = p8

        self.RIGHT = Rectangle(p13,p14,p15,p16)

        ##################################################################################################

    @staticmethod
    def Delay(A : Rectangle , B : Rectangle):
        """ Return True if the time between 2 triangle object is <= DELAYTIME"""
        if (A.getTime() != 0 and B.getTime() != 0): #none empty default case is having time = 0
            if (0 <= (B.getTime() - A.getTime()) <= (HandPosition.TIMEDELAY)):
                #print((B.getTime(),A.getTime()))
                # if the time between moving from a given position in a rectangle is <= than the delay so the swipe motion is produced
                return True
            return False

    def UPDOWN(self):
        """ detect whatever the swipe (up->down) is produced takes: hand detection object"""
        if self.UP.getPosition() and self.DOWN.getPosition() and HandPosition.Delay(self.UP,self.DOWN):
            self.UP.Reset()
            self.DOWN.Reset()
            print("SWIPE DOWN ! ")
            Keys.VolumeDown()
            return True
        return False
    
    def DOWNUP(self):
        """ detect whatever the swipe (down->up) is produced takes: hand detection object"""
        if self.UP.getPosition() and self.DOWN.getPosition() and HandPosition.Delay(self.DOWN,self.UP):
            self.UP.Reset()
            self.DOWN.Reset()
            print("SWIPE UP ! ")
            Keys.VolumeUp()
            return True 

    def LEFTRIGHT(self):
        """ detect whatever the swipe (left->right) is produced takes: hand detection object"""
        if self.LEFT.getPosition() and self.RIGHT.getPosition() and HandPosition.Delay(self.LEFT,self.RIGHT):
            self.LEFT.Reset()
            self.RIGHT.Reset()
            print("SWIPE RIGHT ! ")
            Keys.NextVideo()
            return True
        return False
    
    def RIGHTLEFT(self):
        """ detect whatever the swipe (right->left) is produced takes: hand detection object"""
        if self.RIGHT.getPosition() and self.LEFT.getPosition() and HandPosition.Delay(self.RIGHT,self.LEFT):
            self.LEFT.Reset()
            self.RIGHT.Reset()
            print("SWIPE LEFT ! ")
            Keys.PreviousVideo()
            return True
        return False

    @staticmethod
    def Draw_Rectangle(image,rectangle : Rectangle,color):
        """ Draw Rectangle on image"""
        if rectangle != None :
            start_point =( rectangle.p1.x , rectangle.p1.y)
            end_point = (rectangle.p4.x , rectangle.p4.y)
            cv2.rectangle(image, (0,0), (100,100), (255,0,0), 2)

    def Detect(self,hand_land_mark_position):
        """detect where the hand land mark """
        tmp = hand_land_mark_position
        position = Point(tmp[0],tmp[1]) #affet it to a variable 

        # DETECT POSITIONS

        if(self.UP.In(position)):
            self.UP.setPosition(1)
            self.UP.setTime()
            #print("hand mouved top!")
        if(self.DOWN.In(position)):
            self.DOWN.setPosition(1)
            self.DOWN.setTime()
            #print("hand mouved down!")
        if(self.LEFT.In(position)):
            self.LEFT.setPosition(1)
            self.LEFT.setTime()
            #print("hand mouved left!")
        if(self.RIGHT.In(position)):
            self.RIGHT.setPosition(1)
            self.RIGHT.setTime()
            #print("hand mouved right!")

        # DETECT GESTURES AND SWIPING

        
        HandPosition.DOWNUP(self)
        HandPosition.UPDOWN(self)
        HandPosition.LEFTRIGHT(self)
        HandPosition.RIGHTLEFT(self)

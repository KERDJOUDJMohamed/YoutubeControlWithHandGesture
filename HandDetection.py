from HandPosition import Rectangle
import cv2
import mediapipe as mp
import time 
import mouse
import threading
from win32api import GetSystemMetrics
from Triangle import *

class HandDetection :
        def __init__(self,land_mark=9):
            """
            Initialise the hand detection module
            """
            ######################################
            ################CONST#################
            self.FIRST_TIME = True
            self.CURRET_TIME = 0
            self.PREV_TIME = 0
            self.FPS = 0
            ######################################
            ################LIST##################
            self.Hand_Land_Marks_Position  = [[],[]]
            ######################################
            self.IMG_HEIGHT = 0
            self.IMG_LENGTH = 0
            self.SUCCESS = 0
            self.Capture_Video = None 
            self.Image = None
            self.mpHands = mp.solutions.hands 
            self.Hands =    self.mpHands.Hands(static_image_mode=False,
                                                max_num_hands=2,
                                                min_detection_confidence=0.7,
                                                min_tracking_confidence=0.6)
            self.mpDraw = mp.solutions.drawing_utils#draw detected points 
            self.HandPosition = None
            self.Results = None 
            self.Hand_Land_Marks = False 
            ######################################
            self.Font = cv2.FONT_HERSHEY_COMPLEX
            self.QUIT = True 
            self.Land_Mark = land_mark
            #######################################
            ################MOUSE##################
            self.Hold = False
            #######################################
            ################COLOR##################
            self.BLACK_COLOR = (0,0,0)
            self.RED_COLOR   = (255,0,0)
            self.PURPLE_COLOR = (128, 0, 128)
            self.BLUE_COLOR = (0,0,255)

        def Drag_detection(self,hand=0,error=20):
            """Detect whatever the user want to hond on pressed the mouse """
            if not self.Empty_land_mark_list(hand):

                #GET x,y position from hand mark listt
                p4_x , p4_y =  self.Position(hand,4)

                p8_x , p8_y =  self.Position(hand,8)
                
                #Creat a point obj
                p4 = Point(p4_x,p4_y)
                p8 = Point(p8_x,p8_y)

                # if user wants to hold on the click
                hold = Line.near(p4,p8) 
                if hold : 
                    print("Mouse Draging!")
                    if self.Hold :
                        pass 
                    else:
                        #the first detection -> press 
                        self.Hold = True
                        mouse.press()
                else:
                    self.Hold = False
                    #print("Mouse Relesed!")
                    mouse.release()
                    
        def Position(self,hand=0,landmark=0):
            """ Return the x , y position of a specified landmark on a specified hand """
            if not self.Empty_land_mark_list():
                return self.Hand_Land_Marks_Position[hand][landmark]['x'],self.Hand_Land_Marks_Position[hand][landmark]['y']
            return (0,0)

        def Empty_land_mark_list(self,hand=0):
            """ Check if the HAnd Land Mark list is empty or not """
            if len(self.Hand_Land_Marks_Position[hand]) != 0 :
                return False 
            return True

        def click_detection(self,hand=0):
            """Detect whatever use wants to click mouse"""
            if not self.Empty_land_mark_list(hand):
                
                #get x , y position from the list 
                p4_x , p4_y   =  self.Position(hand,4)
                p5_x , p5_y   =  self.Position(hand,5)
                p17_x , p17_y =  self.Position(hand,17)
                p0_x , p0_y   =  self.Position(hand,0)

                #creat point obj

                p4 = Point(p4_x,p4_y)
                p5 = Point(p5_x,p5_y)
                p17 = Point(p17_x,p17_y)
                p0 = Point(p0_x,p0_y)

                #creat triangle obj 
                
                t = Triangle(p5,p17,p0)

                # look if the point is in the triangle 

                is_pressed = t.In(p4)

                if (is_pressed):
                    print("Mouse Clicked!")
                    #mouse.click()

        def Capture_Image(self):
            """ Read Image From a Video Shout"""
            self.SUCCESS , self.Image = self.Capture_Video.read()
            self.IMG_HEIGHT = self.Image.shape[1]
            self.IMG_LENGTH = self.Image.shape[0]
        
        def Show(self,Name="Image"):
            """Show the Final image"""
            cv2.imshow(Name,self.Image)#show the image
            
        def Draw_Rectangle(self,alpha,rec : Rectangle ,color):
            """Draw Rectangle in the screen """
                
            x1 = rec.p1.x
            y1 = rec.p1.y

            x2 = rec.p4.x
            y2 = rec.p4.y

            new_Image = self.Image.copy() #clone image 
            cv2.rectangle(new_Image,(x1,y1),(x2,y2),color,cv2.FILLED) #create rectangle 
            self.Image = cv2.addWeighted(new_Image, alpha, self.Image, 1 - alpha, 0) # 
            
        def Quit(self):
            """ Set QUIT var to False if user pressed a quit key """
            Key = cv2.waitKey(1)#waiting for key pressed

            if Key%256 == 27:
                # Quit if ESC pressed
                print("Escape hit, closing...")
                self.QUIT = False
    
        def Text_On_Image(self,text,origin,Color):#Origin = (0,70)
            """print a text on an image"""
            cv2.putText(self.Image,str(text),origin,self.Font,3,Color,3)#print the text on the image

        def Set_Webcame(self,nb=0):
            """
            Set the webcome and start recording 
            """
            cap = cv2.VideoCapture(0)
            self.IMG_LENGTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.IMG_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.Capture_Video = cap
            

        def Hand_vibration(self,precision = 5):
            """
            Eliminate the hand vibration for every land mark , Check if the land mark moved around for +- precision 
            """
            pass

        def Mouse_move(self,hand_point=9,hand =0 ,acceleration = 2,duration=0.1):
            acceleration_x = acceleration
            acceleration_y = acceleration
            """
            move the mouse according to the hand mouvement the trick is that the hand covering the entire image should cover the eniter screen
            absolute : move the mouse to an absolate position
            duration : create and animated motion of the mouse 
            """
            #print(self.Hand_Land_Marks_Position[0])
            if not self.Empty_land_mark_list():
                pos = self.Hand_Land_Marks_Position[hand].pop()
                pos_x = pos['x']
                pos_y = pos['y']
                mouse.move(pos_x*acceleration_x , pos_y*acceleration_y , absolute=True , duration=duration)
                self.Clear_Hand_Tracking(hand)

        def Clear_Hand_Tracking(self,Hand):
            """
            Clear a hand tracking list 
            """
            
            self.Hand_Land_Marks_Position[Hand].clear()
            
        def Fps(self):
            """
            calculate the fps takes the previous and the current tike like arguments 
            returns the current time and the frame per second
            """
            self.PREV_TIME = self.CURRET_TIME
            self.CURRET_TIME = time.time()
            self.FPS = int(1/(self.CURRET_TIME - self.PREV_TIME))
            
        def ratio_to_pixel(self,landmark):
            """
            convert ratio generated by the module to an pixel 
            """
            x_ratio = landmark.x
            y_ratio = landmark.y
            
            return int(x_ratio*self.IMG_HEIGHT),int(y_ratio*self.IMG_LENGTH)  
        
        def Process(self,RGB_Image):
            """Processes an RGB image and returns the hand landmarks and handedness of each detected hand.

            Args:
            image: An RGB image represented as a numpy ndarray.

            Returns: -> Results
            A NamedTuple object with two fields: a "multi_hand_landmarks" field that
            contains the hand landmarks on each detected hand and a "multi_handedness"
            field that contains the handedness (left v.s. right hand) of the detected
            hand.
            """
            self.Results = self.Hands.process(RGB_Image)

            self.Hand_Land_Marks = self.Results.multi_hand_landmarks
            
        def Flip_Horiz(self):
            """
            rotate the image Horiz
            """
            self.Image = cv2.flip(self.Image, 1)

        def Flip_Vert(self):
            """
            rotate the image Vert
            """
            self.Image = cv2.flip(self.Image, 0)
        
        def Get_RGB(self):
            """
            convert the image to RGB 
            """
            return cv2.cvtColor(self.Image,cv2.COLOR_BGR2RGB)

        def Draw_Hand(self,handLM,DRAW_CONNECTIONS = True):
            """
            Draw handlandmarks and connections 
            """
            if DRAW_CONNECTIONS:
                self.mpDraw.draw_landmarks(self.Image,handLM,self.mpHands.HAND_CONNECTIONS)#draw on the image captured the detected points and the connections btw
            else :
                self.mpDraw.draw_landmarks(self.Image,handLM)
        
        def Save_Hand_Land_Marks(self,hand,id , x , y):
            """
            Save hand land marks position into a list 
            """ 
            self.Hand_Land_Marks_Position[hand].append({"id":id , "x":x , "y":y })
            
        def Mouse_Threading(self,hand_point=9,hand =0 ,acceleration=3,duration=0.1):
            """Start a thread mouse function"""
            return threading.Thread(target=self.Mouse_move,args=(hand_point,hand,acceleration,duration,))

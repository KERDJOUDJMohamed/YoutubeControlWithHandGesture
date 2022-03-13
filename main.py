from HandDetection import * 
from HandPosition import *


""" HAND DETECTION """
hd = HandDetection() #create new instance 
hd.Set_Webcame() #set the output device(webcame) default = 0

""" HAND POSITION """
hp = HandPosition() #create new instance 
HandPosition.SetDimensions(hd.IMG_LENGTH,hd.IMG_HEIGHT) #set the hand position parameters according to the camera resolution
hp.setPositions() # set the default parameters

while hd.QUIT :

    hd.Fps()
    hd.Capture_Image() #get an image and store it in Image , success = 1 if successufully get the image 0 otherise 
    hd.Flip_Horiz() # rotate the image horiz 
    RGB_Image = hd.Get_RGB() #convert the taken image from BGR to RGB
    Hand_land_marks = hd.Process(RGB_Image) # process the RGB image 

    if hd.Hand_Land_Marks: #if hand has been detected 
        ### TRAITEMENT ###
        for HandLM in hd.Hand_Land_Marks: #for each hand 
            hd.Draw_Hand(HandLM,DRAW_CONNECTIONS=True)#we draw the correspondante hand (draw connection : optional )
            for id , landmark in enumerate(HandLM.landmark): #for every item in each hand we have(21 mark in the hand ) we are getting there position in the picture(ratio)
                # given the h , w of the picture , and the ratio 
                #id is th number of the landmark we have 21 land mark(see the picture)
                x , y = hd.ratio_to_pixel(landmark) # x , y are the position of each handmark
                ##### id = the hand land mark (0,20) , x , y = position of the hand land mark in pixel #####
                #hd.Save_Hand_Land_Marks(hd.Hand_Land_Marks.index(HandLM),id,x,y)
                if id == 9:
                    #Draw Up Rectangle Zone
                    
                    hp.Detect((x,y))
    
    #hd.Text_On_Image(hd.FPS,(0,70),hd.BLACK_COLOR)
    
    """ DRAW RECT"""
    hd.Draw_Rectangle(0.2,hp.UP,(255,0,0)) # draw up rectangle in blue color 
    hd.Draw_Rectangle(0.2,hp.DOWN,(255,0,0)) # draw DOWN rectangle in blue color

    hd.Draw_Rectangle(0.2,hp.RIGHT,(0,0,255)) # draw up rectangle in green color
    hd.Draw_Rectangle(0.2,hp.LEFT,(0,0,255)) # draw up rectangle in green color

    hd.Show() #show the image
    #hd.click_detection() 
    #get the position of a specified and land mark
    
    #hd.Drag_detection()
    #hd.Mouse_Threading().start() #start a thread
    hd.Quit() # press esc to close 
import asyncio
import setup_path
import airsim
import WP_Parser
import os
import sys
sys.path.append('./')
import cv2 as cv
import numpy as np
import concurrent.futures
import threading
import math
import tkinter
import tkinter.ttk
import PIL.Image, PIL.ImageTk
import time
from detect_model.detect import DetectModel
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

#declare global client
#client1 : for move
#client2 : for vizualization

client1 = airsim.MultirotorClient()
client2 = airsim.MultirotorClient()


control_center = []
#
class ViewApp(threading.Thread):
    def __init__(self, model, window, window_title):
        threading.Thread.__init__(self)

        self.detect_model = model
        self.window = window 
        self.window.title(window_title)
        self.delay=15

        #View Video
        self.original_width = 256
        self.original_height = 144
        self.canvas = tkinter.Canvas(window, width = self.original_width * 3, height = self.original_height * 3)
        self.canvas.pack()

        self.update()
        self.window.mainloop()
    def update(self):
        try:
            box_candidate = []
            responses = client2.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
            response = responses[0]

            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 
            img = img1d.reshape(response.height, response.width, 3)

            #* Detect Box *#
            det = self.detect_model.detect(img)
            img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            
            if len(det) > 0:
                for box in det:
                    img_rgb = cv.rectangle(img_rgb, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)
                    box_center_x = int(int(int(box[0]) + int(box[2])) / 2)
                    box_center_y = int(int(int(box[1]) + int(box[3])) / 2)
                    img_rgb = cv.circle(img_rgb, (box_center_x, box_center_y), 2, (0, 0, 255), -1)
                    
                    #* cal box for control
                    box_area = (box[2] - box[0]) * (box[3] - box[1]) 
                    box_list = [box_area.cpu().numpy(), (box_center_x, box_center_y)]
                    box_candidate.append(box_list)

            #* box sorting (find maximum area box)
            box_candidate.sort(key = lambda x : x[0])

            global control_center
            control_center = box_candidate

            img_rgb = cv.resize(img_rgb, dsize=(self.original_width * 3, self.original_height * 3), interpolation=cv.INTER_LINEAR)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img_rgb, mode="RGB"))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        except:
            pass

        self.window.after(self.delay, self.update)


def move_function(client, WPP):  
    con = 1
    global control_center
    image_center = [128, 72] #(W (x), H (y)) image resolution : [256, 144]
    print("hello")
    while(True):
        control_x = 1
        control_y = 0
        control_z = 0
        print("in move : ", control_center)
        print("cal : ", control_center)
        # print("con : ", con)    
            # Get WayPoint Data index = con
        # Proceed If Next WayPoint Exist
        if len(control_center) > 0:
            if control_center[0][0] > 600:
                if image_center[0] > control_center[0][1][0]: #if iamge center coord x is larger than control center
                    control_y = -0.5 #go left side
                    print
                elif image_center[0] < control_center[0][1][0]: #if image center coord x is smaller than control center
                    control_y = 0.5 #go right side
                else: #!need to think point
                    control_y = 0

                if image_center[1] > control_center[0][1][1]: #if iamge center coord y is larger than control center
                    control_z = -0.5 #go downward side
                elif image_center[1] < control_center[0][1][1]: #if image center coord y is smaller than control center
                    control_z = 0.5 #go upward side
                else: #!need to think point
                    control_z = 0

        client1.moveByVelocityBodyFrameAsync(control_x, control_y, control_z, 0.5).join()
        # client.rotateToYawAsync(int(new.ZR)).join()
        # client.moveToPositionAsync(int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1, 2).join()
        

if __name__ == '__main__':
    desired_speed  = 5
    # WayPoints Data Path
    docs = os.path.join(sys.path[0], "multirotor_example/WayPoints.txt")
    
    # connect to the AirSim simulator
    
    client1.confirmConnection()
    client1.enableApiControl(True)
    client1.armDisarm(True)

    # TakeOff
    print("Taking Off")
    client1.takeoffAsync().join()
    print("Initializing")
    way_points = []
    filename = 'C:/Users/ssjun511/Documents/AirSim/testimg/test_img'
    # Create WayPoint Parser
    WPP = WP_Parser.WP_Data(docs, None)
    detect_model = DetectModel()

    if WPP.IsFileOpen:
        print("GOGO")

        move_thread = threading.Thread(target=move_function, args=(client1, WPP))
        move_thread.daemon = True
        move_thread.start()

        image_thread = ViewApp(detect_model, tkinter.Tk(), "GUI")
        image_thread.daemon = True
        image_thread.start()
    
    # client.hoverAsync().join()
    # client.landAsync().join()

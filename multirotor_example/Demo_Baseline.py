import asyncio
import setup_path
import airsim
import WP_Parser
import os
import sys
import cv2 as cv
import numpy as np
import concurrent.futures
import threading
import math
import tkinter
import tkinter.ttk
import PIL.Image, PIL.ImageTk
#declare global client
#client1 : for move
#client2 : for vizualization

client1 = airsim.MultirotorClient()
client2 = airsim.MultirotorClient()
#
class ViewApp(threading.Thread):
    def __init__(self, window, window_title):
        threading.Thread.__init__(self)
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
            responses = client2.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
            response = responses[0]
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 
            img_rgb = img1d.reshape(response.height, response.width, 3)
            img_rgb = cv.cvtColor(img_rgb, cv.COLOR_BGR2RGB)
            img_rgb = cv.resize(img_rgb, dsize=(self.original_width * 3, self.original_height * 3), interpolation=cv.INTER_LINEAR)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img_rgb, mode="RGB"))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        except:
            pass

        self.window.after(self.delay, self.update)


def move_function(client, WPP):  
    con = 1
    while(True):
        print("con : ", con)
        if con == 17: con+=1

            # Get WayPoint Data index = con
        new = WPP.ReadData(con, "WP")
        # Proceed If Next WayPoint Exist

        if new:
            con += 1
            print(new.X)
            print(new.Y)
            print(new.Z)
            print(new.Xoff)
            print(new.Zoff)
            print(new.Yoff, "\n")

            way_points.append([int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1])
            client.rotateToYawAsync(int(new.ZR)).join()
            client.moveToPositionAsync(int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1, 5).join()
        
        else:
            break

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
    if WPP.IsFileOpen:
        print("GOGO")

        move_thread = threading.Thread(target=move_function, args=(client1, WPP))
        move_thread.daemon = True
        move_thread.start()

        image_thread = ViewApp(tkinter.Tk(), "GUI")
        image_thread.daemon = True
        image_thread.start()
    
    # client.hoverAsync().join()
    # client.landAsync().join()

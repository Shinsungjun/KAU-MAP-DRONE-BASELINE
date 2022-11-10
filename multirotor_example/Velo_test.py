
import setup_path
import airsim
import WP_Parser
import os
import sys

# Desired Speed in m/s
desired_speed  = 5

# WayPoints Data Path
docs = os.path.join(sys.path[0], "multirotor_example/WayPoints.txt")

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# TakeOff
print("Taking Off")
client.takeoffAsync().join()
print("Initializing")
way_points = []


# Create WayPoint Parser
WPP = WP_Parser.WP_Data(docs, None)

# If Found WayPoint Data
if WPP.IsFileOpen:
    print("GOGO")

    # LOOP
    con = 1
    while(1):

        # Ignore WaPoint #17

        # Get WayPoint Data index = con

        # Proceed If Next WayPoint Exist
        client.moveByVelocityBodyFrameAsync(1, 0, 0, 0.1).join()
        # * moveByVelocityBodyFrameAsync - local frame, x : + -> forward y : + -> right z : + -> down (NED Coord)
            # client.rotateToYawAsync(int(new.ZR)).join()


    # Return To First WayPoint
    new = WPP.ReadData(1, "WP")
    way_points.append([int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1])
    client.moveToPositionAsync(int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1, 5).join()
   
else:
    print("Failed To open WayPoint File")
   
client.hoverAsync().join()
client.landAsync().join()
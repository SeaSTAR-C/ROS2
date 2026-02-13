from controller import SwitchController
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import os #to create files (like my txt and csv files)
from datetime import datetime #creates files w/ date and time

#this remembers that if the buttons were pressed on the last loop so it only reacts once per press
#if these arent here it'll print button x was pressed like 15 times per press.
#I know i can put 3 quotes at the top and three at the bottom if my comments are multiple lines
#but if i do that then my comment becomes bright green and it looks like code, I like it to be grey.
b0_was_down = False #debounce for button 0
b1_was_down = False #debounce for button 1 
b2_was_down = False #debounce for button 2 
b3_was_down = False #debounce for button 3 
b4_was_down = False #debounce for button 4 
b5_was_down = False #debounce for button 5 
b6_was_down = False #debounce for button 6 
b7_was_down = False #debounce for button 7 
b8_was_down = False #debounce for button 8 
b9_was_down = False #debounce for button 9 
b10_was_down = False #debounce for button 10 
b11_was_down = False #debounce for button 11 
b12_was_down = False #debounce for button 12 
b13_was_down = False #debounce for button 13 
b14_was_down = False #debounce for button 14 

recording = False #trigger debounce, same thing as buttons, (we're currently not recording data, this becomes true when we do)
combo_was_down = False #this remembers if both triggers (ZL + ZR) were down last loop
log_file = None #we start at none
log_path = None

def trigger_pressed(v, thresh=0.5):
    #this is my helper function, so it tells me when the triggers are pressed, for example, on the
    #controller when the trigger is pressed v = 1.00, when it isn't pressed v = -1.00, therefore I
    #am setting the threshold to 0.5 because that means that for the most part it is mostly pressed.
    return v > thresh #therefore, if v > 0.5 the trigger is being pressed, if v < 0.5 the trigger is not being pressed.

def ensure_logs_dir(): #this makes a folder called "logs" exist and if it already does, it does nothing.
    os.makedirs("logs", exist_ok=True)

def start_log(): #this starts recording data, and creates a new CSV file.
    global log_file, log_path
    ensure_logs_dir() #calling my function to make sure logs exist
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") #function from datetime and it should get the date and time for the file being created.
    log_path = os.path.join("logs", f"run_{ts}.csv") #full file path (name)
    log_file = open(log_path, "w", buffering=1) #opens the file in write mode, so it can write the data in the file.
    log_file.write("time,lx,ly,rx,ry,zl,zr,buttons\n") #formats the data in the file.
    print(f" RECORDING STARTED -> {log_path}") #just prints so I know it's recording
    node.ui_pub.publish(String(data="RECORDING STARTED")) #prints this to the UI


def stop_log(): #this function stops recording the data, and closes the CSV file.
    global log_file, log_path #global variable b/c we are using it in more than one function
    if log_file: #this checks if there is an open file
        log_file.close() #this closes the CSV file.
        log_file = None #this sets log_file to back none, to show that there is no file open.
    print("🔴 RECORDING STOPPED") #prints it stopped recording so I know
    log_path = None #no active log anymore

# fixed loop rate
DT = 0.1  #this is how fast the loop runs (0.1 seconds)
next_t = time.time() #this is the time the next loop should run

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')
        self.ui_pub = self.create_publisher(String, '/ui/controller_events', 10)

if __name__ == "__main__":
    rclpy.init() #initialize ROS2
    node = ControllerNode()
    c = SwitchController() #creates a "joystick object" this helps read the joystick position. "C" for controller

    #while True:
    while rclpy.ok():

        rclpy.spin_once(node, timeout_sec=0.0)

        c.update() #update the controller + the pygame events
    
        #These read the joystick axes, and buttons being pressed.
        lx, ly = c.get_left_stick() #left joystick
        rx, ry = c.get_right_stick() #right joystick
        zl, zr = c.get_triggers() #ZL & ZR triggers
        buttons = c.get_pressed_buttons() #all the buttons

        #joystick axis, and button, and recording status being printed
        print(
            f"Left: ({lx:.2f}, {ly:.2f}) | "
            f"Right: ({rx:.2f}, {ry:.2f}) | "
            f"Triggers: ZL={zl:.2f} ZR={zr:.2f} | "
            f"Buttons: {buttons} | "
            f"REC={'ON' if recording else 'OFF'}"
        )

        #buttons
        b0_down = c.js.get_button(0)
        b1_down = c.js.get_button(1)
        b2_down = c.js.get_button(2)
        b3_down = c.js.get_button(3)
        b4_down = c.js.get_button(4)
        b5_down = c.js.get_button(5)
        b6_down = c.js.get_button(6)
        b7_down = c.js.get_button(7)
        b8_down = c.js.get_button(8)
        b9_down = c.js.get_button(9)
        b10_down = c.js.get_button(10)
        b11_down = c.js.get_button(11)
        b12_down = c.js.get_button(12)
        b13_down = c.js.get_button(13)
        b14_down = c.js.get_button(14)

        #button 1 (B)
        if b1_down and not b1_was_down:
            button_1_message = "button 1 has been pressed"
            print(button_1_message)
            node.ui_pub.publish(String(data=button_1_message)) #should print to UI
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_1_message + "\n")
        #button 2 (X)
        if b2_down and not b2_was_down:
            button_2_message = "button 2 has been pressed"
            print(button_2_message)
            node.ui_pub.publish(String(data=button_2_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_2_message + "\n")
        #button 3 (Y)
        if b3_down and not b3_was_down:
            button_3_message = "button 3 has been pressed"
            print(button_3_message)
            node.ui_pub.publish(String(data=button_3_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_3_message + "\n")
        #button 0 (A)
        if b0_down and not b0_was_down:
            button_0_message = "button 0 has been pressed"
            print(button_0_message)
            node.ui_pub.publish(String(data=button_0_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_0_message + "\n")
        #button 4 (-)
        if b4_down and not b4_was_down:
            button_4_message = "button 4 has been pressed"
            print(button_4_message)
            node.ui_pub.publish(String(data=button_4_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_4_message + "\n")
        #button 5 (home button)
        if b5_down and not b5_was_down:
            button_5_message = "button 5 has been pressed"
            print(button_5_message)
            node.ui_pub.publish(String(data=button_5_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_5_message + "\n")
        #button 6 (+)
        if b6_down and not b6_was_down:
            button_6_message = "button 6 has been pressed"
            print(button_6_message)
            node.ui_pub.publish(String(data=button_6_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_6_message + "\n")
        #button 7 (left joystick pressed)
        if b7_down and not b7_was_down:
            button_7_message = "button 7 has been pressed"
            print(button_7_message)
            node.ui_pub.publish(String(data=button_7_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_7_message + "\n")
        #button 8 (right joystick pressed)
        if b8_down and not b8_was_down:
            button_8_message = "button 8 has been pressed"
            print(button_8_message)
            node.ui_pub.publish(String(data=button_8_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_8_message + "\n")
        #button 9 (Left Trigger)
        if b9_down and not b9_was_down:
            button_9_message = "button 9 has been pressed"
            print(button_9_message)
            node.ui_pub.publish(String(data=button_9_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_9_message + "\n")
        #button 10 (Right Trigger)
        if b10_down and not b10_was_down:
            button_10_message = "button 10 has been pressed"
            print(button_10_message)
            node.ui_pub.publish(String(data=button_10_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_10_message + "\n")
        #button 11 (cross up)
        if b11_down and not b11_was_down:
            button_11_message = "button 11 has been pressed"
            print(button_11_message)
            node.ui_pub.publish(String(data=button_11_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_11_message + "\n")
        #button 12 (cross down)
        if b12_down and not b12_was_down:
            button_12_message = "button 12 has been pressed"
            print(button_12_message)
            node.ui_pub.publish(String(data=button_12_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_12_message + "\n")
        #button 13 (cross left)
        if b13_down and not b13_was_down:
            button_13_message = "button 13 has been pressed"
            print(button_13_message)
            node.ui_pub.publish(String(data=button_13_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_13_message + "\n")
        #button 14 (cross right)
        if b14_down and not b14_was_down:
            button_14_message = "button 14 has been pressed"
            print(button_14_message)
            node.ui_pub.publish(String(data=button_14_message))
            with open("buttons_pressed.txt", "a") as f:
                f.write(button_14_message + "\n")

        b0_was_down = b0_down
        b1_was_down = b1_down
        b2_was_down = b2_down
        b3_was_down = b3_down
        b4_was_down = b4_down
        b5_was_down = b5_down
        b6_was_down = b6_down
        b7_was_down = b7_down
        b8_was_down = b8_down
        b9_was_down = b9_down
        b10_was_down = b10_down
        b11_was_down = b11_down
        b12_was_down = b12_down
        b13_was_down = b13_down
        b14_was_down = b14_down

        
        zl_down = trigger_pressed(zl) #on of combo press for recording 
        zr_down = trigger_pressed(zr)
        combo_down = zl_down and zr_down

        if combo_down and not combo_was_down:
            recording = not recording
            if recording:
                start_log()
            else:
                stop_log()

        combo_was_down = combo_down


        if recording and log_file: #if this is recording log one row at a time
            t = time.time()
            log_file.write(
                f"{t:.3f},{lx:.3f},{ly:.3f},{rx:.3f},{ry:.3f},{zl:.3f},{zr:.3f},{buttons}\n"
            )

        #this continues to keep looping at 0.1 seconds
        next_t += DT
        sleep_time = next_t - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            next_t = time.time()
            
    node.destroy_node()
    rclpy.shutdown()

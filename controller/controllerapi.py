import rclpy #ros library.
from rclpy.node import Node #creates the node.
from sensor_msgs.msg import Joy #importing joy.
from std_msgs.msg import String #to send text commands.
from geometry_msgs.msg import Twist #used for velocity commands.
'''
this script sends the following mission commands:
- START_MISSION
- END_MISSION
- START_TELEMETRY
- STOP_TELEMETRY
- START_RECORDING_VIDEO
- STOP_RECORDING_VIDEO
- COLLECT_WATER_SAMPLE
to the ROS topic /mission/control & /ui/controller_events.
'''
#----------------------------------------------------------------------------------------
class controllerapi(Node): #creates the ros node.
    def __init__(self):
        super().__init__('controller') #initialize ros node w/ this name.

        self.joy_sub = self.create_subscription( #subscribes to the /joy topic which is published by the ROS joy_node.
            Joy,
            '/joy', #ROS topic name.
            self.joy_callback, #this function runs everytime a message arrives.
            10 #queue size (how many messages to buffer).
        )

        self.mission_pub = self.create_publisher( #publisher used to send mission commands (start_mission, end_mission, etc.)
            String, #message type.
            '/mission/control', #ROS topic where mission commands will publish to.
            10
        )

        self.ui_event_pub = self.create_publisher( #this publisher is used for logging controller events to the UI.
            String,
            '/ui/controller_events', #ROS topic used to display controller actions to UI.
            10
        )
        #do not know if this is nessecary (ask alex)
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/rov/cmd_vel', #would publish movement commands.
            10
        )

        self.prev_buttons = [] #stores previous button states to detect new presses.

        #states
        self.mission_active = False #this is if the mission is currently running.
        self.telemetry_active = False #this is if it is currently recording data.
        self.video_active = False #this is if it is currently recording video.
        self.water_sample_sent = False #this makes sure collect water sample only sends once while triggers are held.
        self.get_logger().info('Controller node started.') #prints to terminal, so we know it started.

    def joy_callback(self, msg: Joy): #function runs everytime new joystick data arrives.
        if not self.prev_buttons: #initialize the previous button list the first time we receive a message
            self.prev_buttons = [0] * len(msg.buttons)
#----------------------------------------------------------------------------------------
        #button mapping for xbox controller.
        A_BUTTON = 0
        B_BUTTON = 1
        X_BUTTON = 3
        Y_BUTTON = 4
        LB_BUTTON = 6 #left bumper.
        RB_BUTTON = 7 #right bumper.
        LT_BUTTON = 8 #left trigger.
        RT_BUTTON = 9 #right trigger.
        SM_L_CIRCLE_BUTTON = 10 #small left circle button.
        SM_R_CIRCLE_BUTTON = 11 #small right circle button.
        XBOX_BUTTON = 12
        L_JOYSTICK = 13
        R_JOYSTICK = 14

        #axis mapping for triggers.
        LT_AXIS = 4 #left trigger axis.
        RT_AXIS = 5 #right trigger axis.
#----------------------------------------------------------------------------------------
        #now we get into the mission commands.

        #start/end mission (button 13 & 14 pressed at the same time.)
        #aka two joysticks PRESSED.
        mission_combo_now = ( #this checks if they are both currently pressed.
            msg.buttons[L_JOYSTICK] == 1 and
            msg.buttons[R_JOYSTICK] == 1
        )

        mission_combo_before = ( #this checks if they were both pressed during the previous message.
            self.prev_buttons[L_JOYSTICK] == 1 and
            self.prev_buttons[R_JOYSTICK] == 1
        )

        if mission_combo_now and not mission_combo_before: #this means if we pressed it for the first time.
            mission_msg = String() #creates new message object.

            if not self.mission_active: #if mission is currenly false.
                mission_msg.data = 'START_MISSION' #then send start mission.
                self.mission_active = True #now we switch mission active from false -> true.

                ui_msg = String() #this displays onto the UI.
                ui_msg.data = 'Controller: START_MISSION pressed'
                self.ui_event_pub.publish(ui_msg) 

                self.get_logger().info('Published START_MISSION')

            else: #else mission IS active.
                mission_msg.data = 'END_MISSION' #then we send end mission command.
                self.mission_active = False #we update mission active status. (true -> false).

                ui_msg = String() #displays onto the UI.
                ui_msg.data = 'Controller: END_MISSION pressed' 
                self.ui_event_pub.publish(ui_msg)

                self.get_logger().info('Published END_MISSION')

            self.mission_pub.publish(mission_msg) #publish the command.
#----------------------------------------------------------------------------------------
        #telemetry recording (if left bumper and right bumper pressed at the same time.)
        telemetry_combo_now = ( #this checks if they are both currently pressed.
            msg.buttons[LB_BUTTON] == 1 and
            msg.buttons[RB_BUTTON] == 1
        )

        telemetry_combo_before = ( #this checks if they were both pressed during the previous message.
            self.prev_buttons[LB_BUTTON] == 1 and
            self.prev_buttons[RB_BUTTON] == 1
        )

        if telemetry_combo_now and not telemetry_combo_before: #this means if we pressed it for the first time.
            telemetry_msg = String() #creates new message object.

            if not self.telemetry_active: #if recording for telemetry data is currenly false.
                telemetry_msg.data = 'START_TELEMETRY' #then send start telemetry.
                self.telemetry_active = True #change state to true. 

                ui_msg = String() #displays onto the UI.
                ui_msg.data = 'Controller: START_TELEMETRY pressed'
                self.ui_event_pub.publish(ui_msg)

                self.get_logger().info('Published START_TELEMETRY')

            else: #else recording IS active.
                telemetry_msg.data = 'STOP_TELEMETRY' #then send stop telemetry.
                self.telemetry_active = False #change state from true -> false.

                ui_msg = String() #displays onto the UI.
                ui_msg.data = 'Controller: STOP_TELEMETRY pressed' 
                self.ui_event_pub.publish(ui_msg)

                self.get_logger().info('Published STOP_TELEMETRY')

            self.mission_pub.publish(telemetry_msg) #sends command.
#----------------------------------------------------------------------------------------
        #record video (button 4, on/off)

        if msg.buttons[Y_BUTTON] == 1 and self.prev_buttons[Y_BUTTON] == 0: #detects new button press on button Y(4).
            video_msg = String() #if that is true then creates message object. 

            if not self.video_active: #if video recording is false.
                video_msg.data = 'START_RECORDING_VIDEO' #send this.
                self.video_active = True #change state to true.

                ui_msg = String() #displays on UI
                ui_msg.data = 'Controller: START_RECORDING_VIDEO pressed' #yay
                self.ui_event_pub.publish(ui_msg) #actually publishes it.

                self.get_logger().info('Published START_RECORDING_VIDEO') 
           
            else: #else means it was actually recording.
                video_msg.data = 'STOP_RECORDING_VIDEO' #send stop video.
                self.video_active = False #change state of video active to false.

                ui_msg = String() #display onto the UI.
                ui_msg.data = 'Controller: STOP_RECORDING_VIDEO pressed'
                self.ui_event_pub.publish(ui_msg)

                self.get_logger().info('Published STOP_RECORDING_VIDEO')

            self.mission_pub.publish(video_msg)
#----------------------------------------------------------------------------------------
        #collect water sample (both triggers need to be pressed at the same time.)
        #trigger values are -1 when not pressed and 1 when fully pressed.
        #this is a one-time event, me thinks.
        left_trigger = msg.axes[LT_AXIS]
        right_trigger = msg.axes[RT_AXIS]

        if len(msg.axes) > max(LT_AXIS, RT_AXIS): #make sure trigger axes exist.
            trigger_sum = left_trigger + right_trigger #adds the two trigger values together.

            if trigger_sum > 1.8 and not self.water_sample_sent: #if both triggers are basically fully pressed for the first time and they were not previously pressed then send command.
                sample_msg = String() #creates message object.
                sample_msg.data = 'COLLECT_WATER_SAMPLE' #send collect water sample command.
                self.mission_pub.publish(sample_msg) #publish command.

                ui_msg = String() #display onto the UI.
                ui_msg.data = 'Controller: COLLECT_WATER_SAMPLE pressed'
                self.ui_event_pub.publish(ui_msg)

                self.get_logger().info('Published COLLECT_WATER_SAMPLE')

                self.water_sample_sent = True #prevents sending again while the triggers are still held.

            elif trigger_sum <= 1.8: #if triggers are released again.
                self.water_sample_sent = False #reset so it can be used again later if needed, which i dont think it will be needed idk omg ugh.
#----------------------------------------------------------------------------------------
        #just joystick movement but might be irrelevant.
        twist = Twist()

        if len(msg.axes) > 1:
            twist.linear.x = msg.axes[1]
            twist.angular.z = msg.axes[0]

        self.cmd_vel_pub.publish(twist)

        self.prev_buttons = list(msg.buttons) #save current button states.



def main(args=None): #my main function.
    rclpy.init(args=args) # initialize ROS communication.
    node = controllerapi() #creates the controller node.
    rclpy.spin(node) #keeps the node active. 
    node.destroy_node() #destroy the node when it shuts down.
    rclpy.shutdown() #shutdown ROS.


if __name__ == '__main__':
    main() #run the main function.
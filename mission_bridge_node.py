import rclpy #creates ros2 node in python.
from rclpy.node import Node
from std_msgs.msg import String #simple ros message type.

class MissionBridgeNode(Node): #node has been created using class.
    def __init__(self): #node starts running.
        super().__init__('mission_bridge_node') #initialize node, and name it (this is how ROS identifies node in the system.)
        #subscriber
        self.mission_control_sub = self.create_subscription(
            String, #message type.
            '/mission/control', #topic name.
            self.mission_control_callback, #this function runs when message arrives.
            10 #queue size
        )
        #publisher
        self.state_event_pub = self.create_publisher(
            String,
            '/state_machine/events',
            10
        )
        #These print on terminal so we know the node started.
        self.get_logger().info('Mission bridge node started.')
        self.get_logger().info('Listening on /mission/control')
        self.get_logger().info('Publishing to /state_machine/events')

    #callback function (it runs whenever a message arrive, or should....)
    def mission_control_callback(self, msg: String) -> None:
        command = msg.data.strip() #removes white space.
        self.get_logger().info(f'Received UI command: {command}')
        event_msg = String()

        if command == 'start_mission':
            event_msg.data = 'start_mission'
            self.state_event_pub.publish(event_msg) #publish to the sm topic.
            self.get_logger().info('Forwarded start_mission to state machine.') #log the action.
        elif command == 'end_mission':
            event_msg.data = 'end_mission'
            self.state_event_pub.publish(event_msg) #publish to the sm topic.
            self.get_logger().info('Forwarded end_mission to state machine.') #log the action.
        else:
            self.get_logger().warn(f'Unknown mission command: {command}')

def main(args=None):
    rclpy.init(args=args) #initializes ROS2 communication.
    node = MissionBridgeNode() #creates instance of Node.

    try:
        rcply.spin(node) #this keeps node running and constantly listening for messages.
    except KeyboardInterrupt:
        node.get_logger().info('Mission bridge node stopped by user.') #if user presses ctrl+c or ends the program.
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__': #just ensures main actually runs, lowk unnecesarry (idk how to spell).
    main()


#! /usr/bin/env python

# Main control loop for Sawyer Handover 

import rospy
from handover_class import Handover

PHASE = 1

def main():
    rospy.init_node('control_functions_py')
    handover = Handover()
    # initialize
    satisfied = False
    counter = 0
    timeout = False
    try:
        while counter < 100:
            if not timeout:
                handover.set_positions(name='OBSERVE')
                
                obj = False
                while not obj:
                    obj = handover.object_CV()
                    
                handover.set_positions(name='PICKUP')
                # Grasping the object
                handover.add_delay(0.50)
                handover.grasp(act='close')
                handover.add_delay(0.50)
                
                handover.set_positions(name='HOME')
                
            else:
                handover.set_positions(name='HOME')
            
                
            person = False
            while not person:
                person = handover.handover_CV()
                
            
            handover.add_delay(0.5) # Delay before starting HO (Param)
            handover.set_positions(name='HANDOVER') # Performing Reach Phase
            handover.add_delay(0.0)


            # Handover period with a 5 second timeout
            handover.interaction_mode(False) #### Currently Turned off #### set 'True' to turn on #####
            
            while not handover.add_timeout(duration=3.0):
                pass

            timeout = handover.get_timeout_state()
            if not timeout:
                handover.grasp(act='open')
                handover.save_log()

            handover.add_delay(0.40)
            handover.interaction_mode(False)
            
            #if counter > 9:
            #    satisfied = handover.is_satisfied()

            counter += 1

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user. Exiting before trajectory completion.')
        return 



if __name__ == '__main__':
    main()
 
from BehaviourTask import BehaviourTask
from util.actioncommand import goalieDiveLeft, goalieStand
from body.skills.Stand import Stand

import robot

class TestFeetBumper(BehaviourTask):
    
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Stand": Stand(self)
        }
    
    def _reset(self):
        self._current_sub_task = "Stand"

    def _transition(self):
        sensorValues = self.world.blackboard.motion.sensors.sensors
        # task 1
        if sensorValues[robot.Sensors.LFoot_Bumper_Left] and sensorValues[robot.Sensors.RFoot_Bumper_Left]:
            self.taskFlag = 1
            print("Selecting task Emote!!!!!!!!!!!!")
        # task 2 
        elif sensorValues[robot.Sensors.LFoot_Bumper_Left] and sensorValues[robot.Sensors.RFoot_Bumper_Right]:
            self.taskFlag = 2
            print("Selecting task HeadTrackBall!!!!!!!!!!!!")
        # task 3
        elif sensorValues[robot.Sensors.LFoot_Bumper_Right] and sensorValues[robot.Sensors.RFoot_Bumper_Left]:
            self.taskFlag = 3
        # task 4
        elif sensorValues[robot.Sensors.LFoot_Bumper_Right] and sensorValues[robot.Sensors.RFoot_Bumper_Right]:
            self.taskFlag = 4

        elif sensorValues[robot.Sensors.LFoot_Bumper_Left] and sensorValues[robot.Sensors.LFoot_Bumper_Right] and sensorValues[robot.Sensors.RFoot_Bumper_Left] and sensorValues[robot.Sensors.RFoot_Bumper_Right]:
            self.taskFlag = 0
            self._current_sub_task = "Stand"
            print("Selecting task Stand!!!!!!!!!!!!")

    def _tick(self):
        self._transition()

        self._tick_sub_task()
        

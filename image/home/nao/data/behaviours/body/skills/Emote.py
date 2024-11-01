from BehaviourTask import BehaviourTask
from body.skills.Walk import Walk
from util.actioncommand import walk, stand, raiseArm
from util.CircularMotion import angular_velocity
from util.Global import myPos, myHeading
from util.Vector2D import Vector2D
from math import pi, radians
from util.MathUtil import normalisedTheta, angleSignedDiff
from util.ObstacleAvoidance import walk_vec_with_avoidance
from util.Timer import Timer, WallTimer, update_timer
import os
import time
import robot

class Emote(BehaviourTask):
    def __init__(self, parent=None, world=None):
        super().__init__(parent, world)

        self.countdown = None
        
    def _initialise_sub_tasks(self):
        self._sub_tasks = {"Walk": Walk(self)}  # Call the subtask

    def _reset(self):
        self._current_sub_task = "Walk"
        os.system("aplay /home/nao/data/emote.wav &")

    # Radius is in mm
    def _tick(self, radius=50, forward=50, clockwise=True):
        # Define angular velocity
        av = angular_velocity(radius, forward)

        if self.countdown is None:
            # Initialise countdown, according to docs, if already running, 
            # it shouldn't restart
            self.countdown = Timer(30 * 1000000).start()

        # If the timer (in us) is the same as the circle distance / walking 
        # speed, then we can assume that the robot has walked in a circle and 
        # can stop
        if not self.countdown.finished():
            if not self.countdown.elapsed() % (10 * 1000000) :
                robot.say("YEAH")
                self.world.b_request.actions.body = raiseArm()
                time.sleep(2)
                self.world.b_request.actions.body = stand()
            else:
                turn = av * (-1 if clockwise else 1)
                self.world.b_request.actions.body = walk(forward, 0, turn)
        else:
            self.world.b_request.actions.body = stand()
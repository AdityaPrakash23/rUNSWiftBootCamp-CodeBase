# This is our main file we are going to use to test our code
import robot
from importlib import import_module
from util.Vector2D import Vector2D
from BehaviourTask import BehaviourTask
from body.skills.Stand import Stand
from body.skills.WalkInLine import WalkInLine   # Not sure if this is right
from body.skills.WalkInCircle import WalkInCircle
from util.Constants import FIELD_LENGTH, PENALTY_AREA_LENGTH, CENTER_CIRCLE_DIAMETER, LEDColour

from util.FieldGeometry import (
    ENEMY_GOAL_BEHIND_CENTER,
    ball_near_our_goal,
    calculateTimeToReachBall,
    calculateTimeToReachPose,
)

from util.Timer import WallTimer
from util import LedOverride

class FieldPlayer(BehaviourTask):
    def _initialise_sub_tasks(self):
        self._sub_tasks = {
            "Stand": Stand(self),
            "WalkInLine": WalkInLine(self),
            "WalkInCircle": WalkInCircle(self)
        }

    def _reset(self):
        self._current_sub_task = "WalkInCircle"

    def _transition(self):
        # If you wanted to write a transition to the subtask it would go here
        pass

    def _tick(self):
        # Tick sub task!
        self._tick_sub_task()

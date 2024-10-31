import robot
from BehaviourTask import BehaviourTask
from util.Global import update_global, ballWorldPos, ballRelPos, ballLostTime, canSeeBall, myPos, myHeading
from body.skills.WalkStraightToPose import WalkStraightToPose
from body.skills.LineUp import LineUp
from head.HeadTrackBall import HeadTrackBall  # Assuming headTrackBall is in `head_tracking`

class FollowBall(BehaviourTask):
    def _initialise_sub_tasks(self):
        # Define each sub-task in a dictionary with string keys
        self._sub_tasks = {
            "HeadTrackBall": HeadTrackBall(self),
            "LineUp": LineUp(self),
            "WalkToPose": WalkStraightToPose(self)
        }

    def _reset(self):
        # Reset initial states for tracking and movement
        self._current_sub_task = "HeadTrackBall"  # Start with head tracking
        self.ball_lost = False
        self._finished_lineup = False
        self._finished_walking = False
        self._mode = "WalkToPose"

    my_pos = myPos()
    my_heading = myHeading()

    # Finding ball distance
    def update_ball_position(self, blackboard):
        # Update global variables for the ball and robot position
        update_global(blackboard)
        self.ball_lost = ballLostTime() > 3  # If the ball is unseen for more than 3 seconds

    def _transition(self):
        # **Step 1: Track the ball with head if the ball is lost or unseen**
        if self._current_sub_task == "HeadTrackBall":
            self._finished_lineup = False
            self._finished_walking = False
            robot.say("Tracking ball with head...")
            self.head_track_task._tick()

            if canSeeBall():  # Move to next step if the ball is seen
                self.current_step = "LineUp"
            elif self.ball_lost:
                robot.say("Searching for ball...")

        # **Step 2: Line up the robot to face the ball**
        elif self._current_sub_task == "LineUp":
            robot.say("Aligning with ball...")
            ball_pos = ballWorldPos()
            rel_theta = 0  # No additional rotation required in LineUp for this case

            # Call the LineUp task to face the ball
            self.line_up_task._tick(rel_theta=rel_theta, kick_position=ball_pos)

            # Move to next step if alignment is complete
            if self.line_up_task.position_aligned and self.line_up_task.heading_aligned:
                robot.say("Aligned with ball. Moving toward it...")
                self.current_step = "WalkToPose"

        # **Step 3: Walk directly toward the ball**
        elif self._current_sub_task == "WalkToPose":
            robot.say("Walking toward ball...")
            ball_pos = ballWorldPos()

            # Call WalkToPose to move directly to the ball’s position
            self.walk_to_pose_task._tick(final_pos=ball_pos, speed=1.0)

            # Continuously track the ball and maintain the WalkToPose task
            if ballLostTime() > 3:  # If the ball is lost during approach
                robot.say("Ball lost while walking. Returning to head tracking...")
                self.current_step = "HeadTrackBall"  # Go back to tracking the ball
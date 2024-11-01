from body.skills.P2PPass import P2PPass
from util.TeamStatus import get_teammate_pos

from BehaviourTask import BehaviourTask


class PassToTeammate(BehaviourTask):
    def _initialise_sub_tasks(self):
        self._sub_tasks = {"PassToTeammate": P2PPass(self)}
    
    def _reset(self):
        self._current_sub_task = "PassToTeammate"

    def _tick(self):
        if self._current_sub_task == "PassToTeammate":
            self._tick_sub_task(pass_target = 100)

    

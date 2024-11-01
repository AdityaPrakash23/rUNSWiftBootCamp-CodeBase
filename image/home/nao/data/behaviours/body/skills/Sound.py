
from BehaviourTask import BehaviourTask
import os

class Sound(BehaviourTask):
    def __init__(self, parent=None, world=None):
        super().__init__(parent, world)

    def _reset(self):
        os.system("aplay /home/nao/data/emote.wav &")

from util.actioncommand import stand

import os

from BehaviourTask import BehaviourTask


class PlayAudio(BehaviourTask):
    def _reset(self):
        # ls -> aplay
        os.system("aplay /home/nao/data/music.wav &")
        # put this in the data folder!
        pass

    def _tick(self):
        pass


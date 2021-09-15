__author__ = "Sergey Karakovskiy, sergey at idsia fullstop ch"
__date__ = "$May 13, 2009 1:29:41 AM$"

from .tcpenvironment import TCPEnvironment
from utils.dataadaptor import extractObservation
import numpy as np


class MarioEnvironment(TCPEnvironment):
    """ An Environment class, wrapping access to the MarioServer, 
    and allowing interactions to a level. """

    _is_debug = False

    # tracking cumulative reward
    _cumReward = 0

    # reward
    _finished = False
    _reward = 0
    _status = 0

    def __init__(self, is_debug=False, agentname='UnnamedClient', **otherargs):
        super(MarioEnvironment, self).__init__(agentname)
        self._is_debug = is_debug

    def getObservation(self):
        ob = extractObservation(TCPEnvironment.getObservation(self))
        if len(ob) == TCPEnvironment._numberOfFitnessValues:
            self._reward = ob[1]
            self._status = ob[0]
            self._finished = True
        if self._is_debug and len(ob) == TCPEnvironment._numberOfObeservationValues:
            self._printLevelScene(ob)
        return ob

    def performAction(self, action):
        if not self.isFinished():
            TCPEnvironment.performAction(self, action)
            self._addReward()

    def isFinished(self):
        return self._finished

    def reset(self):
        """ reinitialize the environment """
        # Note: if a task needs to be reset at the start, the subclass constructor
        # should take care of that.
        TCPEnvironment.reset(self)
        self._cumReward = 0
        self._finished = False
        self._reward = 0
        self._status = 0

    def getTotalReward(self):
        """ the accumulated reward since the start of the episode """
        return self._cumReward

    def getReward(self):
        """ Fitness gained on the level """
        return self._reward

    def getWinStatus(self):
        return self._status

    def _addReward(self):
        """ a filtered mapping towards performAction of the underlying environment. """
        # by default, the cumulative reward is just the sum over the episode
        self._cumReward += self.getReward()

    def _printLevelScene(self, ob):
        ret = ""
        for x in range(22):
            tmpData = ""
            for y in range(22):
                tmpData += self._mapElToStr(ob[4][x][y])
            ret += "\n%s" % tmpData
        print(ret)
        # print(np.array(ob[4]))
        print('mayMarioJump: ', ob[0])
        print('isMarioOnGround: ', ob[1])
        print('marioFloats: ', ob[2])
        print('enemiesFloats: ', ob[3])

    def _mapElToStr(self, el):
        """maps element of levelScene to str representation"""
        s = ""
        if (el == 0):
            s = "##"
        s += "#MM#" if (el == 95) else str(el)
        while (len(s) < 4):
            s += "#"
        return s + " "

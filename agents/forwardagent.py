import numpy
from enum import Enum
from .marioagent import MarioAgent

KEY_LEFT  = 1 << 0
KEY_RIGHT = 1 << 1
KEY_DOWN  = 1 << 2
KEY_JUMP  = 1 << 3
KEY_SPEED = 1 << 4 # can fire if mario mode is 2
class Action(Enum):
    NONE = 0
    LEFT = KEY_LEFT
    RIGHT = KEY_RIGHT
    DOWN = KEY_DOWN
    JUMP = KEY_JUMP
    SPEED = KEY_SPEED
    LEFT_DOWN = KEY_LEFT + KEY_DOWN
    LEFT_JUMP = KEY_LEFT + KEY_JUMP
    LEFT_SPEED = KEY_LEFT + KEY_SPEED
    LEFT_JUMP_SPEED = KEY_LEFT + KEY_JUMP + KEY_SPEED
    RIGHT_DOWN = KEY_RIGHT + KEY_DOWN
    RIGHT_JUMP = KEY_RIGHT + KEY_JUMP
    RIGHT_SPEED =  KEY_RIGHT + KEY_SPEED
    RIGHT_JUMP_SPEED = KEY_RIGHT + KEY_JUMP + KEY_SPEED
    '''
    Notice JUMP_DOWN and SPEED_FIRE is illegal
    '''

JUMP_SET = (e.value for e in Action)
NO_JUMP_SET = (Action.LEFT, Action.RIGHT, Action.DOWN, Action.SPEED, Action.LEFT_DOWN, Action.LEFT_SPEED, Action.RIGHT_DOWN, Action.RIGHT_SPEED)

class ForwardAgent(MarioAgent):
    """ In fact the Python twin of the
        corresponding Java ForwardAgent.
    """
    action = None
    actionStr = None
    KEY_LEFT = 0
    KEY_RIGHT = 1
    KEY_DOWN = 2
    KEY_JUMP = 3
    KEY_SPEED = 4
    levelScene = None
    mayMarioJump = None
    isMarioOnGround = None
    marioFloats = None
    enemiesFloats = None
    isEpisodeOver = False

    trueJumpCounter = 0
    trueSpeedCounter = 0

    def reset(self):
        self.isEpisodeOver = False
        self.trueJumpCounter = 0
        self.trueSpeedCounter = 0

    def __init__(self):
        """Constructor"""
        self.trueJumpCounter = 0
        self.trueSpeedCounter = 0
        self.action = numpy.zeros(5, int)
        # self.action[self.KEY_RIGHT] = 1 # default RIGHT
        self.actionStr = ""
        self.Action = Action.NONE

    def _dangerOfGap(self):
        for x in range(9, 13):
            f = True
            for y in range(12, 22):
                if (self.levelScene[y, x] != 0):
                    f = False
            if (f and self.levelScene[12, 11] != 0):
                return True
        return False

    # def _a2(self):
    #     """ Interesting, sometimes very useful behaviour which might prevent falling down into a gap!
    #     Just substitue getAction by this method and see how it behaves.
    #     """
    #     if (self.mayMarioJump):
    #         print("m: %d, %s, %s, 12: %d, 13: %d, j: %d"
    #               % (self.levelScene[11, 11], self.mayMarioJump, self.isMarioOnGround,
    #                  self.levelScene[11, 12], self.levelScene[11, 12], self.trueJumpCounter))
    #     else:
    #         if self.levelScene == None:
    #             print("Bad news.....")
    #             print("m: %d, 12: %d, 13: %d, j: %d"
    #                   % (self.levelScene[11, 11],
    #                       self.levelScene[11, 12], self.levelScene[11, 12], self.trueJumpCounter))

    #     a = numpy.zeros(5, int)
    #     a[1] = 1

    #     danger = self._dangerOfGap()
    #     if (self.levelScene[11, 12] != 0 or
    #             self.levelScene[11, 13] != 0 or danger):
    #         if (self.mayMarioJump or
    #                 (not self.isMarioOnGround and a[self.KEY_JUMP] == 1)):
    #             a[self.KEY_JUMP] = 1
    #         self.trueJumpCounter += 1
    #     else:
    #         a[self.KEY_JUMP] = 0
    #         self.trueJumpCounter = 0

    #     if (self.trueJumpCounter > 16):
    #         self.trueJumpCounter = 0
    #         self.action[self.KEY_JUMP] = 0

    #     a[self.KEY_SPEED] = danger

    #     actionStr = ""

    #     for i in range(5):
    #         if a[i] == 1:
    #             actionStr += '1'
    #         elif a[i] == 0:
    #             actionStr += '0'
    #         else:
    #             print("something very dangerous happen....")

    #     actionStr += "\r\n"
    #     print("action: ", actionStr)
    #     return actionStr

    def getAction(self):
        """ Possible analysis of current observation and sending an action back
        """
#        print "M: mayJump: %s, onGround: %s, level[11,12]: %d, level[11,13]: %d, jc: %d" \
#            % (self.mayMarioJump, self.isMarioOnGround, self.levelScene[11,12], \
#            self.levelScene[11,13], self.trueJumpCounter)
#        if (self.isEpisodeOver):
#            return numpy.ones(5, int)

        danger = self._dangerOfGap()
        if (self.levelScene[11, 12] != 0 or
                self.levelScene[11, 13] != 0 or danger):
            if (self.mayMarioJump or
                    (not self.isMarioOnGround and self.action[self.KEY_JUMP] == 1)):
                self.action[self.KEY_JUMP] = 1
            self.trueJumpCounter += 1
        else:
            self.action[self.KEY_JUMP] = 0
            self.trueJumpCounter = 0

        if (self.trueJumpCounter > 16):
            self.trueJumpCounter = 0
            self.action[self.KEY_JUMP] = 0

        self.action[self.KEY_SPEED] = danger
        return self.action

    def integrateObservation(self, obs):
        """This method stores the observation inside the agent"""
        if (len(obs) != 6):
            self.isEpisodeOver = True
        else:
            self.mayMarioJump, self.isMarioOnGround, self.marioFloats, self.enemiesFloats, self.levelScene, dummy = obs

    def printObs(self):
        """for debug"""
        print(repr(self.observation))

    def onGround(self):
        return self.isMarioOnGround

    def mayJump(self):
        return self.mayMarioJump

    def encode(self):
        for i in range(5):
            if self.Action & 1 << i:
                self.action[i] = 1
        return self.action

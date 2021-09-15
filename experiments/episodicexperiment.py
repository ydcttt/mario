from pynput.keyboard import Key, Listener
from .Game import Game

class EpisodicExperiment():
    """ The extension of Experiment to handle episodic tasks. """
    _paused = False

    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.stepid = 0
        self._key_listener = Listener(on_press = self._key_pause)
        self._key_listener.start()

    def __del__(self):
        self._key_listener.stop()

    def _oneInteraction(self):
        self.stepid += 1
        # observe
        self.agent.integrateObservation(self.env.getObservation())
        
        # action
        self.env.performAction(self.agent.getAction())

        # reward
        reward = self.env.getReward()
        self.agent.giveReward(reward)
        return reward

    statusStr = ("Loss...", "Win!")
    def doEpisodes(self, number=1):
        """ returns the rewards of each step as a list """
        all_rewards = []
        for i in range(number):
            rewards = []
            # the agent is informed of the start of the episode
            self.agent.newEpisode()
            self.env.reset()
            while not self.env.isFinished():
                if self._paused:
                    # time.sleep(0.1)
                    self.env.pause_game()
                else:
                    r = self._oneInteraction()
                    rewards.append(r)
            all_rewards.append(rewards)

            win = self.env.getWinStatus()
            print('Episode #%d finished with status %s: reward: %d,' % (i, self.statusStr[win], self.env.getReward()))
        return all_rewards

    def _key_pause(self, key):
        if key == Key.space:
            self._paused = ~self._paused
        # if self._paused:
        #     self.env.pause_game()
        # else:
        #     self.env.resume_game()

class Board():
    def __init__(self, n):
        "Set up initial board configuration"
        self.n = n
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

class MarioGame(Game):
    def __init__(self, n, env, agent):
        self.n = n
        self.env = env
        self.agent = agent

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces) 
    
    def getBoardSize(self):
        return (self.n, self.n)

    def getActionSize(self):
        if agent.mayJump:
            return len()


    # def getNextState(self, board, player, action):
    #     # mcts
    
    # def getValidMoves(self, board, player):
    #     # mcts


    # def getGameEnded(self, board, player):
    #     # mcts

    
    # def getCanonicalForm(self, board, player):
    #     # mcts

    # def getSymmetries(self, board, pi):
        # no meaning for mario

    # def stringRepresentation(self, board):
    #     # mcts

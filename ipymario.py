#!/usr/bin/python
__author__ = "Sergey Karakovskiy, sergey at idsia dot ch"
__date__ = "$Apr 30, 2009 1:46:32 AM$"

import sys

from experiments.episodicexperiment import EpisodicExperiment
from client.marioenvironment import MarioEnvironment
from agents.forwardagent import ForwardAgent
from agents.forwardrandomagent import ForwardRandomAgent


# from pybrain.... episodic import EpisodicExperiment
# TODO: reset sends: vis, diff=, lt=, ll=, rs=, mariomode, time limit, pw,
# with creatures, without creatures HIGH.
# send creatures.

def main():
    agent = ForwardAgent()
    env = MarioEnvironment(is_debug=True, agentname=agent.getName())
    exp = EpisodicExperiment(env, agent)
    print('Env Ready')

    # env.setMarioMode(1)
    # env.setDifficulty(1)
    # exp.doEpisodes(1)

    env.setMarioMode(2)
    env.setDifficulty(4)
    exp.doEpisodes(1)

    print("Finished all simulation.")


if __name__ == "__main__":
    main()
else:
    print("This is module to be run rather than imported.")

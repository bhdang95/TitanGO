Learn more or give us feedback
#!/usr/local/bin/python2
from dlgo.gtp import GTPFrontend
from dlgo.agent.predict import load_prediction_agent
from dlgo.agent import termination
import h5py

# model_file = h5py.File("agents/betago.hdf5", "r")
model_file = h5py.File("agents/deep_bot_2.h5", "r")
agent = load_prediction_agent(model_file)
strategy = termination.get("opponent_passes")
termination_agent = termination.TerminationAgent(agent, strategy)

frontend = GTPFrontend(termination_agent)
frontend.run()

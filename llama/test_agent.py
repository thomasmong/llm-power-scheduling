from custom_agents.agents import *
import time

model = "llama3"
classifier = ClassifierAgent(model=model)
start = time.time()
classifier.classify("Here is my request: Charge my EV quickly please", verbose=True)
print(f"Time: {time.time()-start}")
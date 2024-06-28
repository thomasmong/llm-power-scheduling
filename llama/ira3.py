from custom_agents.agents import ClassifierAgent
import os
import time

dir = "../db"

# Create the classifier
model = "llama3-classifier-scenar3"

def ira_for_file(filepath, classifier: ClassifierAgent):

    # Output file
    filename = os.path.basename(filepath)
    output_file = filename[:-4] + f"-ira-{model}-{classifier.number_of_classes}.txt"
    output_path = os.path.join('ira/scenar3', output_file)
    f_out = open(output_path, "w")

    # Treat line after line
    start = time.time()
    with open(filepath, "r", encoding='utf8') as f:
        next(f)
        next(f)
        for line in f:
            req = line[1:-2]
            calls = classifier.classify(req,verbose=True)
            for call in calls:
                op_id = call["arguments"]["ID"]
                print(call)
            f_out.write(str(op_id) + "\n")
            f_out.flush()
            print(op_id)
    end = time.time()

    # Write the time
    f_out.write(f"Time: {end-start}")
    f_out.close()


#####
# Max number of classes
max_classes = 5
dict_problems = {
    "LP": ["CC"],
    "MTL": ["CT"],
    "QP": ["PV"],
    "CP": ["GD"],
    "MM": ["PP"]
}

for i in range(1,max_classes+1):
    classifier = ClassifierAgent(i, model+f"-op{i}")
    ops_to_treat = classifier.op_classes[:i]
    for op_id in ops_to_treat:
        for problem in dict_problems[op_id]:
            # File that starts with "problem"
            for file in os.listdir(dir):
                if file.startswith(problem):
                    # Check if already treated
                    if not os.path.exists(os.path.join('ira/scenar3',file[:-4] + f"-ira-{model}-{i}.txt")):
                        ira_for_file(os.path.join(dir, file), classifier)


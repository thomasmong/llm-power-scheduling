from custom_agents.agents import ClassifierAgent
import os
import time

dir = "../db"
filename = "70b-test.txt"

# Create the classifier
model = "llama3-70b-classifier-scenar3"

def ira_for_file(filepath, classifier: ClassifierAgent):

    # Output file
    filename = os.path.basename(filepath)
    output_file = filename[:-4] + f"-ira-{model}-{classifier.number_of_classes}-bis.txt".replace(":", "-")
    output_path = os.path.join('ira', output_file)
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

# Ira for file
classifier = ClassifierAgent(5, model+f"-op{5}")
ira_for_file(os.path.join(dir, filename), classifier)
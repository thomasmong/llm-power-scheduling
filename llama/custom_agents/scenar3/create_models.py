import ollama

base_models = ["llama3:70b"]

op_classes = ["LP","MTL","MM","QP","CP"]

req_ex = {
    "LP": "Charge my EV tonight at the lowest cost.",
    "MTL": "I need my EV really quickly charged please.",
    "MM": "Charge my car but please, make sure to reduce the power peaks.",
    "QP": "Can you charge the car while making sure to smooth the power at the charger?",
    "CP": "Hey, minimize the damages on the distribution transformer while charging the car."
}

# Classifiers
for base_model in base_models:

    for i in range(1, 6):
        # op class
        model = f"{base_model}-classifier-scenar3-op{i}".replace(":", "-")
        with open("custom_agents/scenar3/classifier-sp.txt", "r") as f:
            system_prompt = f.read().replace("\n", "\\n")
        modelfile = f"FROM {base_model}\nSYSTEM '''{system_prompt}\\nHere is your expert knowledge: "
        for op in op_classes[:i]:
            # Mathematical description of the class
            with open(f"custom_agents/classifier-knowledge/{op}-class.txt", "r") as f:
                knowledge = f.read().replace("\n", "\\n")
                modelfile += f"File: {op}-class.md FILE START {knowledge} FILE END\\n"
            
            # Problems of the class
            with open(f"custom_agents/classifier-knowledge/EV-Charging-{op}-classifier.txt", "r") as f:
                problems = f.read().replace("\n", "\\n")
                modelfile += f"File: EV-Charging-{op}-classifier.md FILE START {problems} FILE END\\n"

            # Request example
            modelfile += f"Assume that the user request is: {req_ex[op]}\\n"
            modelfile += "You have to make the following function call:\\n"
            modelfile += "<functioncall>{ \"name\": \"classify\", \"arguments\":{ \"ID\": \"" + op + "\" } }</functioncall>\\n"

        modelfile += "'''"
        modelfile += "\nPARAMETER num_ctx 8192"
        # Save the modelfile
        with open(f"custom_agents/scenar3/{model}-modelfile.txt", "w") as f:
            f.write(modelfile)
        ollama.create(model=model, modelfile=modelfile)

# Parsers
for base_model in base_models:
    for op in op_classes:
        model = f"{base_model}-parser-{op}"
        with open(f"custom_agents/scenar3/parser-sp-{op}.txt", "r") as f:
            system_prompt = f.read().replace("\n", "\\n")
        modelfile = f"FROM {base_model}\nSYSTEM '''{system_prompt}\\n"
        
        # Class description
        with open(f"custom_agents/classifier-knowledge/{op}-class.txt", "r") as f:
            knowledge = f.read().replace("\n", "\\n")
            modelfile += f"Here is the {op} description:\\n{knowledge}\\n"
        
        # Problems of the class
        with open(f"custom_agents/parser-knowledge/EV-Charging-{op}-parser.txt", "r") as f:
            problems = f.read().replace("\n", "\\n")
            modelfile += f"Here are the problems you might encounter:\\n{problems}\\n"

        # Smart Meter class description
        with open(f"custom_agents/parser-knowledge/SmartMeter-class-description.txt", "r") as f:
            smart_meter = f.read().replace("\n", "\\n")
            modelfile += f"Here is the Smart Meter class description:\\n{smart_meter}\\n"
        modelfile += "You have to use those attributes and methods as Python code to access data from the Smart Meter. You don't need to use all of them. Don't ever invent an attribute or a method.\\n"

        # Functions
        with open(f"custom_agents/parser-knowledge/set_dates.json", "r") as f:
            functions = f.read().replace("\n", "\\n")
            modelfile += f"Here is the set_dates description:\\n{functions}\\n"
        modelfile += "You have to replace starting_datetime, stopping_datetime and duration using the following rules:\\n- starting_datetime and stopping_datetime must be in the date format \"YYYY-MM-DD HH:MM:SS\"\\n- duration must be an float value representing the time duration in hours\\n- if a parameter is implicitely specified, you can refer to the user preferences\\n- stopping_datetime and duration can't be defined at the same time. One of them must be \"None\"\\n- if a parameter is undefined, explicitely nor implicitely, replace it with the string value \"None\", not just None\\n\\nFor example, \"this evening\", \"tonight\" are implicit time parameters. It suggests that:\\n- the user wants to start the request at the end of the day, based on its preferences -> starting_datetime : end of the day\\n- the user needs the request to end at the beggining of the next day, based on its preferences -> stopping_datetime: beginning og the next day"
        with open(f"custom_agents/parser-knowledge/solve_{op}.json", "r") as f:
            functions = f.read().replace("\n", "\\n")
            modelfile += f"Here is the solve_{op} description:\\n{functions}\\n"
        modelfile += "Make two distinct function calls to set the dates and solve the problem.\\n"

        # User preferences
        with open(f"custom_agents/parser-knowledge/user-preferences.txt", "r") as f:
            preferences = f.read().replace("\n", "\\n")
            modelfile += f"Here are the user preferences:\\n{preferences}\\n"
        
    
        modelfile += "'''"
        modelfile += "\nPARAMETER num_ctx 8192"
        # Save the modelfile
        with open(f"custom_agents/scenar3/{model}-modelfile.txt", "w") as f:
            f.write(modelfile)
        ollama.create(model=model, modelfile=modelfile)
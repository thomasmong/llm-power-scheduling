import ollama

base_model = "llama3"

op_classes = ["LP","MTL","MM"]

model = f"{base_model}-classifier-scenar1"
with open("custom_agents/scenar1/classifier-sp-basic.txt", "r") as f:
    system_prompt = f.read().replace("\n", "\\n")
modelfile = f"FROM {base_model}\nSYSTEM '''{system_prompt}\\nHere is your expert knowledge: "
for op in op_classes:
    # Mathematical description of the class
    with open(f"custom_agents/classifier-knowledge/{op}-class.txt", "r") as f:
        knowledge = f.read().replace("\n", "\\n")
        modelfile += f"File: {op}-class.txt FILE START {knowledge} FILE END\\n"

modelfile += "'''"
modelfile += "\nPARAMETER num_ctx 8192"
# Save the modelfile
with open(f"custom_agents/scenar1/{model}-modelfile.txt", "w") as f:
    f.write(modelfile)
ollama.create(model=model, modelfile=modelfile)

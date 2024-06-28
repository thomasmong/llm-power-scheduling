### Custom agents for ASHEM
import ollama
import os
import re
import json
import datetime as dt
import random
import types

default_model = "llama3"

link_dict = {
    "LP":["LP"],
    "QP":["QP","LP"],
    "MT":["MT"],
    "MM":["MM"],
    "CP":["CP","QP","LP"],
}

class Agent():
    """Agent for the ASHEM project"""
    def __init__(self, model=default_model) -> None:
        self.model = model

    def chat(self,messages=[]):
        self.chat_history = []
        self.chat_history.extend(messages)
        while True:
            user_input = input(">>>> ")
            self.chat_history.append({'role':'user','content':user_input})
            if user_input.lower() == "\\bye":
                break
            response = ollama.chat(self.model, self.chat_history, stream=True, options={'temperature': 0})
            content_out = ""
            for chunk in response:
                ctn = chunk['message']['content']
                content_out += ctn
                print(ctn, end="", flush=True)
            print("\n")
            self.chat_history.append({'role':'assistant','content':content_out})
    
    def redefineSystemPrompt(self, new_prompt):
        self.system_prompt = new_prompt
        self.resetHistory()

    def resetHistory(self):
        self.chat_history = []

    def parseFunctionCall(self, answer):
        matches = re.findall(r'<functioncall>(.*?)</functioncall>', answer, re.DOTALL)
        if matches:
            try:
                return [json.loads(match.strip()) for match in matches]
            except json.JSONDecodeError as e:
                return []
        return []

    def readKnowledge(self, path, op_ids):
        files = [os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        files = [f for f in files if any(op_id in f for op_id in op_ids)]
        return self.readFiles(files)

    def readFiles(self, filenames):
        messages = []
        for file in filenames:
            with open(file, "r") as f:
                messages.append({'role':'user','content':f'Can you read and keep in mind the file {file}?'})
                messages.append({'role':'assistant','content':f"Filename: {os.path.basename(file)}\n{f.read()}\n"})
        return messages
    
    def add_user_message(self, message):
        self.chat_history.append({'role':'user','content':message})
    
    def run(self,prompt,verbose=True):
        self.chat_history.append({'role':'user','content':prompt})
        response = ollama.chat(self.model, self.chat_history, stream=verbose, options={'temperature': 0})
        if verbose:
            content_out = ""
            for chunk in response:
                ctn = chunk['message']['content']
                content_out += ctn
                print(ctn, end="", flush=True)
            print("\n")
        else:
            content_out = response['message']['content']
        self.chat_history.append({'role':'assistant','content':content_out})

class ClassifierAgent(Agent):
    def __init__(self, number_of_classes, model='llama3-classifier') -> None:
        self.model = model
        self.number_of_classes = number_of_classes
        self.op_classes = ["LP","MTL","MM","QP","CP"]
        self.op_meanings = ["Linear Program","Minimum Time with Linear dynamics", "Mini-Max","Quadratic Program","Convex Program"]
        super().__init__(model)

    def classify(self, request, verbose=True):
        self.resetHistory()
        # Give the current datetime
        #current_datetime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #self.add_user_message(f'Just so you know, the current datetime is {current_datetime}.')
        #for i,op_id in enumerate(self.op_classes[:self.number_of_classes]):
            #self.add_user_message(f'{op_id} stands for {self.op_meanings[i]}.')
        self.run(request, verbose)
        answer = self.chat_history[-1]['content']
        function_call = self.parseFunctionCall(answer)
        while True:
            try:
                op_id = function_call[0]["arguments"]["ID"]
                if op_id not in self.op_classes[:self.number_of_classes]:
                    raise ValueError
                break
            except ValueError:
                self.add_user_message(f"OP ID error. Please try again. You can only use the following values: {self.op_classes[:self.number_of_classes]}")
                self.run("Let me remind you the format: <functioncall>{ \"name\":\"classify\", \"arguments\":{ \"ID\":\"id\" } }</functioncall>\nValid values for id are "+str(self.op_classes[:self.number_of_classes]), verbose)
                answer = self.chat_history[-1]['content']
                function_call = self.parseFunctionCall(answer)
            except Exception as e:
                self.add_user_message("Got this error: "+str(e))
                
                if random.random() > 0.3:
                    self.add_user_message("Please try again. Mind the number of curly brackets. It is really important. Don't modify your choice.")
                else:
                    self.add_user_message("STOP repeating yourself. You are not listening to me. Try again.")
                self.run("Let me remind you the format: <functioncall>{ \"name\":\"classify\", \"arguments\":{ \"ID\":\"id\" } }</functioncall>\nValid values for id are "+str(self.op_classes[:self.number_of_classes]), verbose)
                answer = self.chat_history[-1]['content']
                function_call = self.parseFunctionCall(answer)
        return function_call


class ParserAgent(Agent):
    def __init__(self, model=default_model) -> None:
        self.model = model
        super().__init__(model)
    
    def parse(self, request, verbose=True):
        # Read the knowledge from the knowledge folder
        self.resetHistory()
        #self.readFiles([f'parser-knowledge/{op_id}-class.md'])
        #for op in link_dict[op_id]:
        #    self.readFiles([f'parser-knowledge/EV-Charging-{op}-parser.md'])
        #self.readFiles(["parser-knowledge/SmartMeter-class-description.txt",
        #                "parser-knowledge/user-preferences.md",
        #                "parser-knowledge/set_dates.json",
        #                f"parser-knowledge/solve_{op_id}.json"])

        ### Call of set_dates
        # Give the current datetime
        current_datetime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_user_message(f'The current datetime is {current_datetime}.')
        self.add_user_message('Use the following syntax for function calling: <functioncall>{ \"name\": \"set_dates\", \"arguments\": { \"t_i_str\": \"initial_datetime\", \"t_f_str\": \"final_datetime\", \"T_str\": \"duration\" } }</functioncall>')
        self.run(f"First, extract the time parameters and call the set_dates function for the following user request: {request}", verbose)
        answer = self.chat_history[-1]['content']
        set_date_calls = self.parseFunctionCall(answer)
        while True:
            try:
                t_i_str = set_date_calls[0]["arguments"]["t_i_str"]
                t_f_str = set_date_calls[0]["arguments"]["t_f_str"]
                T_str = set_date_calls[0]["arguments"]["T_str"]
                if t_i_str != "None":
                    t_i = dt.datetime.strptime(t_i_str, "%Y-%m-%d %H:%M:%S")
                if t_f_str != "None":
                    t_f = dt.datetime.strptime(t_f_str, "%Y-%m-%d %H:%M:%S")
                if T_str != "None":
                    if not isinstance(eval(T_str), (int,float)):
                        raise ValueError
                break
            except Exception as e:
                self.add_user_message("Got this error: "+str(e))
                print(str(e))
                self.add_user_message("You probably wrote None instead of \"None\" as a string but I told you to never write this. Or maybe you wrote hours inside the duration parameter, but I told you to never do this too. Listen to me.")
                self.add_user_message("Please try again. Don't modify your choices. Let me remind you the format: <functioncall>{ \"name\": \"set_dates\", \"arguments\": { \"t_i_str\": \"initial_datetime\", \"t_f_str\": \"final_datetime\", \"T_str\": \"duration\" } }</functioncall>.")
                self.run(f"First, extract the time parameters and call the set_dates function for the following user request: {request}", verbose)
                answer = self.chat_history[-1]['content']
                set_date_calls = self.parseFunctionCall(answer)
        
        ### Call of solve
        self.run(f"Then, call the solve function to solve the problem for the following user request: {request}", verbose)
        answer = self.chat_history[-1]['content']
        solve_calls = self.parseFunctionCall(answer)
        while True:
            try:
                if len(solve_calls) != 1:
                    raise ValueError
                break
            except Exception as e:
                print(str(e))
                self.add_user_message("Got this error: "+str(e))
                self.run("Please try again. Don't modify your choices. Let me remind you to put the solve function call inside the <functioncall> and </functioncall> tags. Each parameter must be a string.", verbose)
                answer = self.chat_history[-1]['content']
                solve_calls = self.parseFunctionCall(answer)
            
        return set_date_calls, solve_calls
    
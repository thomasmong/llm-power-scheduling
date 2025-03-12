# Large Language Models for Power Scheduling: A User-Centric Approach

## Overview
This repository contains the code and data used to generate the results presented in our paper "Large Language Models for Power Scheduling: A User-Centric Approach".


https://github.com/user-attachments/assets/902cc6d8-9a06-463d-a0fd-cd6454ba805d


## Dependencies
ollama is required to run the LLM locally. In addition, you will need the following python packages:
- ollama (0.2.1)
- json
- datetime

## Database
The `EVRQ` folder contains all the user requests that constitute the EVRQ database. The filename indicates:
- the desired performance metric ;
- the fact that the performance metric is expressed explicitly or implicitely ;
- the presence or not of explicit time parameters (TP).

## Code usage
### Model creation
First, you need to create the ollama model that correspond to the agents. In `llama/custom_agents`, you can choose for which scenario you want to create the agent.


| Scenario number | Prompting configuration |
|:---------------:|:-----------------------:|
| 1 | Basic Prompting |
| 2 | Contextualized Prompting |
| 3 | Error-Informed Prompting |


To create the model, run the associated `create_models.py` after defining which ollama base model to use. This code will create one ollama model for each of the number of OP classes that are taken into account.
You can modify the system prompts by modifying the `*-sp.txt` files.

### Agents
The agents in this repository allow you to classify and parse requests using large language models. There are two types of agents:

* `ClassifierAgent`: used to classify a request based on its characteristics.
* `ParserAgent`: used to parse a request and extract relevant information.

To use these agents, instantiate them with the desired ollama model and call their respective methods (`classify` or `parse`) by giving the request as an argument.

## Citation Policy
If you use our code or results, please cite our paper:
 T. Mongaillard et al., “Large Language Models for Power Scheduling: A User-Centric Approach,” Jun. 29, 2024, arXiv: arXiv:2407.00476. Accessed: Jul. 02, 2024. [Online]. Available: http://arxiv.org/abs/2407.00476

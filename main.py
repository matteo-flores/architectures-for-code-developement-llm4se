import json
import os
from utils.llm_client import LLMClient
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.tester import TesterAgent
from agents.commenter import CommenterAgent

TASK_NUMBER = 10
MAX_RETRIES = 10

MODEL_ID_LARGE = "meta-llama/Llama-2-7b-hf" # big LLM
MODEL_ID_SMALL = "gpt2"                      # small LLM

LLM_LARGE_CLIENT = LLMClient(model_id=MODEL_ID_LARGE)
LLM_SMALL_CLIENT = LLMClient(model_id=MODEL_ID_SMALL)

def single_agent_arch(task_data, client):
  return client.ask(task_data['prompt'])

def run_pipeline(task_data, planner_client, coder_client, config_name):
  task_id = task_data['task_id']
  prompt = task_data['prompt']
  unit_tests = task_data['test']
  
  print(f"--- Running {config_name} on {task_id} ---")

  planner = PlannerAgent(llm_client=planner_client)
  plan = planner.plan(prompt)
 
  coder = CoderAgent(llm_client=coder_client)
  tester = TesterAgent()
  
  current_code = ""
  feedback = ""
  is_passing = False
  attempts = 0

  while attempts < MAX_RETRIES and not is_passing:
    current_code = coder.code(prompt, plan, feedback)
    
    success, error_msg = tester.test(current_code, unit_tests)
    
    if success:
      is_passing = True
      print(f"  [Attempt {attempts+1}] Success!")
    else:
      feedback = f"The code failed tests. Error: {error_msg}"
      attempts += 1
      print(f"  [Attempt {attempts}] Failed. Retrying with feedback...")

  commenter = CommenterAgent(llm_client=LLM_SMALL_CLIENT)
  final_code_with_metrics = commenter.comment(current_code)
  
  return {
    "config": config_name,
    "is_correct": is_passing,
    "attempts": attempts + 1,
    "final_code": final_code_with_metrics['code'],
    "metrics": final_code_with_metrics['metrics'] # MI, CC computed by radon
  }


def __main__():

  print("Architetures:")
  print("1.\tSingle agent")
  print("2.\tPlanner (small) -> Coder (big) -> Tester -> Commenter")
  print("3.\tPlanner (big) -> Coder (small) -> Tester -> Commenter")
  print("4.\tPlanner -> Coder -> Reviwer -> Refiner")

  for i in range(TASK_NUMBER):
    task_file = f"tasks/task{i+1}.json"
    if not os.path.exists(task_file): continue

    with open(task_file, 'r') as f:
      task_data = json.load(f)
    
    results = list()

    result = single_agent_arch(task_data, LLM_LARGE_CLIENT)
    results.append(result)
    result = run_pipeline(task_data, LLM_SMALL_CLIENT, LLM_LARGE_CLIENT, "Architeture 2")
    results.append(result)
    result = run_pipeline(task_data, LLM_LARGE_CLIENT, LLM_SMALL_CLIENT, "Architeture 3")
    results.append(result)
    #result = run_pipeline_paper(task_data, LLM_LARGE_CLIENT, LLM_SMALL_CLIENT)
    results.append(result)

    # evaluation
    

    # for now, just returns the second code

    output_path = f"code/task{i+1}.py"
    os.makedirs("code", exist_ok=True)
    with open(output_path, "w") as f_out:
      f_out.write(result['final_code'])

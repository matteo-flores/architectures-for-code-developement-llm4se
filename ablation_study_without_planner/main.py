import json
import os
import re
import time
import csv
import sys
import ast

# --- IMPORT AGENTS ---
from utils.llm_client import LLMClient
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
from agents.commenter import CommenterAgent
from radon.metrics import mi_visit, ComplexityVisitor

# Aumenta il limite per la conversione stringa-int (necessario per task matematici pesanti)
sys.set_int_max_str_digits(0)

# CONFIGURAZIONE GLOBALE
TASK_NUMBER = 30 
MAX_RETRIES = 10
MODEL_ID = "gemini-2.5-flash-lite"

# --- CLIENT ---
LLM_CLIENT = LLMClient(model_id=MODEL_ID)

# ---------------------------------------------------------
# 1. SINGLE AGENT ARCHITECTURE
# ---------------------------------------------------------
def single_agent_arch(task_data, client):
    problem_description = task_data['prompt']
    prompt = f"""### SYSTEM INSTRUCTION
    You are a Python Code Generation Engine. 
    You are NOT a chat assistant. You DO NOT explain code.
    Your output is piped directly into a Python compiler. Any text that is not valid Python code (outside the markdown block) will cause a system crash.

    ### TASK
    Write a complete, self-contained Python solution for the following problem.

    ### PROBLEM SPECIFICATION
    {problem_description}

    ### COMPILER REQUIREMENTS (STRICT):
    1.  **Imports**: Include ALL standard library imports at the top.
    2.  **No Comments**: Do not add comments explaining *how* the code works. Only docstrings inside the function are allowed.
    3.  **Complete Logic**: The code must handle edge cases.
    4.  **Format**: Return the code strictly inside a single markdown block.

    ### OUTPUT GENERATION
    ```python
    """
    
    try:
        response = client.generate_response(prompt, max_new_tokens=1024, temperature=0.3)[0]
        code_match = re.search(r"```python\s*(.*?)```", response, re.DOTALL | re.IGNORECASE)
        if code_match:
            extracted_code = code_match.group(1).strip()
        else:
            extracted_code = response.strip()
        print("  [SingleAgent] Code generated.")
        return extracted_code
    except Exception as e:
        print(f"  [SingleAgent] Error: {e}")
        return ""

# ---------------------------------------------------------
# 2. & 3. MULTI AGENT PIPELINE (Configurable)
# ---------------------------------------------------------
def run_pipeline(task_data, client, config_name, use_planner=True):
    """
    Esegue la pipeline Multi-Agent.
    - Se use_planner=True:  Planner -> Coder -> Reviewer (Full Architecture)
    - Se use_planner=False: Coder -> Reviewer (Coder Only / Reactive Mode)
    """
    task_id = task_data['task_id']
    prompt = task_data['prompt']
    unit_tests = task_data['test']
    entry_point = task_data['entry_point']
    
    print(f"--- Running {config_name} on {task_id} ---")

    # 1. PLANNING PHASE (Opzionale)
    plan = None
    if use_planner:
        print("  [Planner] Generating architectural plan...")
        planner = PlannerAgent(llm_client=client)
        plan = planner.plan(prompt)
    else:
        print("  [Planner] SKIPPED. Running in Direct Coder Mode.")

    # 2. CODING & REVIEW LOOP
    coder = CoderAgent(llm_client=client)
    reviewer = ReviewerAgent(llm_client=client)

    current_code = ""
    feedback = ""
    is_passing = False
    attempts = 0

    while attempts < MAX_RETRIES and not is_passing:
        time.sleep(2) # Rate limit safety
        
        # Il Coder gestisce internamente se plan è None o popolato
        current_code = coder.code(prompt, plan, current_code, feedback)
        print(current_code)
        
        # Logging breve per debug
        snippet = current_code.split('\n')[0] if current_code else "No Code"
        print(f"  [Attempt {attempts+1}] Generated: {snippet}...")
        
        time.sleep(2)
        success, error_msg = reviewer.review(current_code, prompt, unit_tests, entry_point)
        
        if success:
            is_passing = True
            print(f"  [Attempt {attempts+1}] Success! Tests passed.")
        else:
            feedback = f"The code failed tests. Error: {error_msg}"
            attempts += 1
            print(f"  [Attempt {attempts}] Failed. Reviewing error...")

    if not is_passing:
        print(f"  [{config_name}] Failed after {MAX_RETRIES} attempts.")
        return ""
    
    # 3. COMMENTING PHASE
    commenter = CommenterAgent(llm_client=client)
    time.sleep(2)
    final_code = commenter.comment(current_code)
    return final_code

# ---------------------------------------------------------
# METRICS & UTILS
# ---------------------------------------------------------
def save_intermediate_code(task_number, arch_number, code):
    if not code: return
    output_dir = "code"
    os.makedirs(output_dir, exist_ok=True)
    
    # File naming convention:
    # task01_1.py -> Single Agent
    # task01_2.py -> Multi Agent (Full)
    # task01_3.py -> Coder Only (No Planner)
    filename = f"task{task_number:02}_{arch_number}.py"
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, "w") as f:
            f.write(code)
        print(f"[FILE] Saved to: {filepath}")
    except Exception as e:
        print(f"[FILE] Error saving {filepath}: {e}")

def load_stress_input(task_number):
    input_path = f"input/task_{task_number:02}.txt"
    if not os.path.exists(input_path):
        # print(f"  [WARN] Input file {input_path} not found. Using default.")
        return None
    try:
        with open(input_path, "r") as f:
            content = f.read().strip()
        try:
            return ast.literal_eval(content)
        except:
            return content
    except:
        return None

def measure_execution_time(func, input_data):
    if input_data is None: return 0.001
    start_time = time.perf_counter()
    try:
        if isinstance(input_data, tuple):
            func(*input_data)
        else:
            func(input_data)
    except Exception:
        return 1_000_000.0 # Penalty
    return time.perf_counter() - start_time

def clean_code_for_metrics(code):
    try:
        parsed = ast.parse(code)
    except SyntaxError:
        return code
    for node in ast.walk(parsed):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, (ast.Constant, ast.Str)):
                node.body.pop(0)
    try:
        return ast.unparse(parsed)
    except:
        return code

def calculate_maintainability(code):
    try:
        return mi_visit(clean_code_for_metrics(code), multi=True)
    except: return 0.0

def get_cyclomatic_complexity(code):
    try: 
        v = ComplexityVisitor.from_code(code)
        if not v.functions: return 1
        return max(f.complexity for f in v.functions) 
    except: return 1

def save_metrics_to_csv(task_number, arch_name, mi, cc, exec_time, score):
    filename = "metrics_results.csv"
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Task', 'Architecture', 'MI', 'CC', 'Time', 'Score'])
        writer.writerow([task_number, arch_name, f"{mi:.2f}", f"{cc:.2f}", f"{exec_time:.6f}", f"{score:.4f}"])
    print(f"[METRICS] Saved for {arch_name}")

def evaluate_and_log(code, arch_name, task_data, i):
    entry_point = task_data['entry_point']
    if not code:
        save_metrics_to_csv(i+1, arch_name, -1, -1, -1, -1)
        return -1
    
    namespace = {}
    try:
        exec(code, namespace)
    except:
        save_metrics_to_csv(i+1, arch_name, -1, -1, -1, -1)
        return -1

    if entry_point not in namespace:
        save_metrics_to_csv(i+1, arch_name, -1, -1, -1, -1)
        return -1
    
    mi = calculate_maintainability(code)
    cc = get_cyclomatic_complexity(code)
    
    input_data = load_stress_input(i+1)
    func_to_test = namespace[entry_point]
    exec_time = measure_execution_time(func_to_test, input_data)
    
    # Simple normalization for score
    mi_norm = min(max(mi, 0), 100) / 100
    cc_norm = 1.0 if cc <= 1 else 1.0 / cc
    target_time = 0.1 
    exec_time_safe = max(exec_time, 0.00001)
    time_norm = min(target_time / exec_time_safe, 1.0)
    
    score = (time_norm * 0.4) + (mi_norm * 0.2) + (cc_norm * 0.4)
    save_metrics_to_csv(i+1, arch_name, mi, cc, exec_time, score)
    return score

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    print("Architectures Configured:")
    print("1. Single Agent")
    print("2. Multi Agent (Planner + Coder + Reviewer)")
    print("3. Coder Only (Coder + Reviewer)")

    # Esegue un loop su tutti i file presenti
    for i in range(0,1):
        task_file = f"tasks/task_{i+1:02}.json"
        if not os.path.exists(task_file): continue

        with open(task_file, 'r') as f:
            task_data = json.load(f)
        
        print(f"\n===== TASK {i+1} =====")

        """# -----------------------------------------
        # 1. Single Agent
        # -----------------------------------------
        code1 = single_agent_arch(task_data, LLM_CLIENT)
        save_intermediate_code(i+1, 1, code1)
        evaluate_and_log(code1, "1_SingleAgent", task_data, i)

        # -----------------------------------------
        # 2. Multi Agent (FULL: With Planner)
        # -----------------------------------------
        code2 = run_pipeline(task_data, LLM_CLIENT, "2_MultiAgent", use_planner=True)
        save_intermediate_code(i+1, 2, code2)
        evaluate_and_log(code2, "2_MultiAgent", task_data, i) """

        # -----------------------------------------
        # 3. Coder Only (NO PLANNER)
        # -----------------------------------------
        code3 = run_pipeline(task_data, LLM_CLIENT, "3_CoderOnly", use_planner=False)
        save_intermediate_code(i+1, 3, code3)
        evaluate_and_log(code3, "3_CoderOnly", task_data, i)

if __name__ == '__main__':
    main()
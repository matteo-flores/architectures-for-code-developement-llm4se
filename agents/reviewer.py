import textwrap
import io
import contextlib
import traceback

class ReviewerAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def review(self, current_code: str, task_prompt: str, test_code_string: str, entry_point: str) -> tuple[bool, str]:
        """
        Entry point per la revisione.
        1. Esegue i test dinamici forniti come stringa Python.
        2. Se falliscono, chiama l'LLM per l'analisi.
        """
        print("   [Reviewer] Starting dynamic execution...")
        
        # Run real tests
        tests_passed, error_msg = self._execute_tests(current_code, test_code_string, entry_point)

        if tests_passed:
            print("   [Reviewer] Code passed dynamic tests.")
            return True, "Passed"

        # If they fail, we ask the LLM for help by passing the specific error
        print(f"   [Reviewer] Tests failed. Error: {error_msg}")
        return self._analyze_failure(current_code, task_prompt, error_msg, test_code_string)

    def _execute_tests(self, generated_code: str, test_code_string: str, entry_point: str) -> tuple[bool, str]:
        """
        Runs the generated code and then executes the test string 'check(candidate)'.
        """
        namespace = {}
        output_capture = io.StringIO()

        try:
            with contextlib.redirect_stdout(output_capture), contextlib.redirect_stderr(output_capture):

                exec(generated_code, namespace)
                
                if entry_point not in namespace:
                    return False, f"Function '{entry_point}' not found in generated code."
                
                candidate_function = namespace[entry_point]

                exec(test_code_string, namespace)
                
                if 'check' not in namespace:
                    return False, "Test script provided does not define a 'check' function."
                
                check_function = namespace['check']


                check_function(candidate_function)
                
            return True, "Passed"

        except AssertionError:
            return False, "AssertionError: The code produced incorrect results on one of the test cases."
            
        except SyntaxError as e:
            return False, f"Syntax Error in generated code: {e}"
            
        except Exception as e:
            # Catch errors at runtime (e.g. TypeError, IndexError, etc.)
            tb = traceback.format_exc()
            return False, f"Runtime Error during testing: {str(e)}"

    def _analyze_failure(self, code: str, task: str, error_msg: str, test_code: str) -> tuple[bool, str]:
        """
        Ask the LLM how to fix the code based on the error.
        """
        prompt = textwrap.dedent(f"""\
            You are a Senior Python Debugger.
            
            TASK:
            {task}

            BROKEN CODE:
            ```python
            {code}
            ```

            TEST SUITE (Reference):
            ```python
            {test_code}
            ```

            ERROR:
            {error_msg}

            INSTRUCTIONS:
            1. The code failed the tests provided above.
            2. Analyze the error and the test suite logic.
            3. Provide a concise suggestion to fix the code.
            4. Start with "STATUS: FAIL".
            
            RESPONSE FORMAT:
            STATUS: FAIL <Short explanation and fix>
            """)

        response_text, _, _ = self.llm_client.generate_response(
            prompt, 
            max_new_tokens=256, 
            temperature=0.0, 
            deterministic=True
        )

        clean_response = response_text.strip()
        if "STATUS: FAIL" not in clean_response:
            # Fallback if the LLM does not comply with the format
            return False, f"Tests failed: {error_msg}"
            
        parts = clean_response.split("STATUS: FAIL")
        return False, parts[1].strip() if len(parts) > 1 else error_msg

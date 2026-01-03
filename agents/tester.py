import re
import textwrap

class TesterAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def prepare_review_context(self, task_prompt, basic_json_tests, entry_point):
        """
        Prepara il contesto per la revisione statica.
        """
        context = f"""
        TASK DESCRIPTION:
        {task_prompt}

        ENTRY POINT FUNCTION:
        {entry_point}

        REQUIRED BEHAVIOR (JSON TESTS):
        {basic_json_tests}
        """
        return context

    def perform_static_review(self, current_code, context):
        """
        Analizza il codice staticamente usando l'LLM.
        Restituisce (True, "Passed") se il codice sembra corretto,
        altrimenti (False, Feedback).
        """
        
        review_prompt = textwrap.dedent(f"""\
            You are a Senior Python QA Engineer and a Strict Code Compiler.
            
            ### GOAL
            Verify if the provided PYTHON CODE is COMPLETE, EXECUTABLE, and CORRECT.

            ### CRITICAL CHECKS (FAIL IMMEDIATELY IF ANY ARE TRUE)
            1. **EMPTY CODE**: If the code block is empty, contains only comments, or just "pass" -> **FAIL**.
            2. **MISSING IMPORTS**: 
               - If `List`, `Dict`, `Optional`, `Tuple` are used in type hints -> `from typing import ...` MUST be present.
               - If `math`, `re`, `collections` are used -> they MUST be imported.
               - **DO NOT ASSUME imports exist.** If they are not written, the code is BROKEN -> **FAIL**.
            3. **LINE NUMBERS**: If lines start with numbers (e.g., "1. import") -> **FAIL**.
            4. **PLACEHOLDERS**: If the code contains "TODO" or "..." instead of logic -> **FAIL**.

            ### TASK CONTEXT
            {context}
            
            ### CANDIDATE CODE TO REVIEW
            ```python
            {current_code}
            ```
            
            ### INSTRUCTIONS
            1. Act like a Python Interpreter. Scan line-by-line for NameErrors (missing imports).
            2. Mentally trace the execution with the provided JSON inputs.
            3. Check for logical bugs or infinite loops.
            4. Be extremely strict. It is better to reject valid code than to pass broken code.
            
            ### OUTPUT FORMAT
            Start with your reasoning/analysis.
            End your response with exactly one of these two lines:
            - "STATUS: PASS"
            - "STATUS: FAIL" followed by a concise error message (e.g., "Missing typing imports", "Code is empty").
            """)

        # Chiamata all'LLM
        response_text, _, _ = self.llm_client.generate_response(
            review_prompt, 
            max_new_tokens=1024, 
            temperature=0.0, # Temperatura a 0 per massima severità
            deterministic=True
        )

        return self._parse_review_result(response_text)

    def _parse_review_result(self, response):
        """Analizza l'output testuale dell'LLM per determinare Pass/Fail."""
        
        clean_response = response.strip()
        
        # Cerca l'ULTIMA occorrenza di STATUS: PASS/FAIL
        pass_index = clean_response.rfind("STATUS: PASS")
        fail_index = clean_response.rfind("STATUS: FAIL")
        
        # Se non trova nulla
        if pass_index == -1 and fail_index == -1:
            # Fallback: se la risposta è molto breve e contiene parole chiave negative
            lower_resp = clean_response.lower()
            if "fail" in lower_resp or "error" in lower_resp or "missing" in lower_resp or "empty" in lower_resp:
                 return False, f"Reviewer Ambiguous Failure: {clean_response}"
            return False, f"Format Error: Reviewer did not output STATUS: PASS/FAIL.\nFull Response: {clean_response}"

        # Se trova entrambi, vince l'ultimo scritto (ragionamento vs conclusione)
        if pass_index > fail_index:
            return True, "Passed (Static Analysis Approved)"
        else:
            # È un FAIL. Estraiamo la spiegazione
            feedback_start = fail_index + len("STATUS: FAIL")
            feedback = clean_response[feedback_start:].strip()
            
            if not feedback:
                # Se non c'è testo dopo STATUS: FAIL, prendiamo le righe precedenti
                feedback = clean_response[:fail_index].strip()[-500:]
            
            return False, feedback
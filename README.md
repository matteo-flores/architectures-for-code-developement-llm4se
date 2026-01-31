# Architectures for Code Development with LLMs

This repository contains the code for the project 'Architectures for Code Development with LLMs'.
This study aims to investigate whether architectural decomposition improves code generation quality by comparing a Single-Agent baseline with a Multi-Agent architecture, using the same model (Gemini 2.5 Flash Lite).
The Multi-Agent architecture is composed of four specialized roles: Planner, Coder, Reviewer, and Commenter.

The project addresses the following research questions:
- RQ1: Which architectures produce higher-quality and more maintainable code?
- RQ2: How do agent coordination strategies impact correctness?
- RQ3: Does modular role separation improve code generation?

A controlled experimental comparison is conducted, supported by two ablation studies that remove the Planner and the loop-back mechanism to assess their impact on performance.


## Repository Structure
- `ablation_study_without_loopback/` - Ablation experiment without the loop-back mechanism  
- `ablation_study_without_planner/` - Ablation experiment without the Planner agent  
- `agents/` - Agent implementations  
- `code/` - Code generated for the evaluated tasks  
- `input/` - Input files used for execution-time evaluation  
- `tasks/` - Task definitions  
- `utils/` - Contains the LLM client  
- `main.py` - Main experiment runner  
- `metrics_results.csv` - Collected evaluation metrics  
- `report_group03.pdf` - Project report  
- `requirements.txt` - Python dependencies  

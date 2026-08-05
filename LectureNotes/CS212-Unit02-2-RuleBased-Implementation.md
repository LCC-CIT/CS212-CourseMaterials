---
title: Unit 1 Overview
description: What's AI
keywords: Classical AI, Symbolic AI, GOFAI
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Symbolic AI: Rule-Based AI Techniques: Implementation</h1>

| Topics                                    |                           |
| ----------------------------------------- | ------------------------- |
| 1. What is AI, Python                     | 6. ANN: Image recognition |
| 2.  Symbolic AI:  <mark>rule-based</mark> | 7. Generative AI          |
| 3. Classical Machine Learning: Training   | 8. Custom chatbot         |
| 4. Classical Machine Learning: Inference  | 9. LLM fine-tuning        |
| 5. Midterm                                | 10. Ethics                |
|                                           | 11. Final                 |

<h2>Contents</h2>

[TOC]



## Implementing Rule-Based Systems

This technique described here is one of the fundamental symbolic AI approaches. It is essentially a search through a knowledge base of rules.

### Concept: forward chaining

Start with a set of *facts* (initial state) and then repeatedly apply *production rules* (If X, Then Y) to derive new facts. The "search" is for the applicable rules that move the system toward a goal. This is called *Forward Chaining* or *data-driven reasoning*.

### Simple Implementation Algorithm

This can be modeled using simple *lists* (for facts) and a collection of *if/then functions* or a large series of `if-elif` statements (for rules).

- Example Problem: A simple diagnostic system.
- Initial Facts: `['has_fever', 'has_cough']`
- Rules:
  1. IF `has_fever` AND `has_cough`, THEN `suspect_flu`.
  2. IF `suspect_flu` AND `has_headache`, THEN `recommend_rest`.
- The "Search": A main loop repeatedly scans the list of rules. If a rule's "IF" condition is met by the current facts, its "THEN" action (adding a new fact) is executed. The loop stops when the goal fact (e.g., `recommend_rest`) is added.

#### How *Forward Chaining* is Executed in the Algorithm

Forward chaining ( also called *data-driven reasoning*) is an *inference mechanism* where reasoning starts with the known data (facts) and continually applies rules to infer new conclusions (new facts) until a goal is reached.

In the algorithm you provided, this process is implemented by the following two core elements:

##### Fact-Driven Search

The main loop repeatedly scans the list of rules which constitutes the *forward chain*. The system looks at the available facts and tries to see what rules can be *triggered* by those facts.

##### Iterative Inference

- Rule Application: "If a rule's 'IF' condition is met by the current facts, its 'THEN' action (adding a new fact) is executed." This is the moment of *inference*—a new piece of knowledge is added to the system's working memory.
- Chain Continuation: Since a newly added fact might satisfy the condition of a different, unapplied rule, the loop continues to scan the rules list. This *chain* of deductions (Fact A → Fact B → Fact C...) is the "chaining" part of the process.

The process stops because the loop condition is satisfied. The loop condition is based on the *goal fact*, `recommend_rest`, so the chain has successfully completed when this is reached.

### Implementation

#### Rule File

IF,AND,THEN,GOAL. 
fever,cough,suspect_flu,  
headache,nausea,suspect_migraine,  
suspect_flu,body_aches,diagnosis_influenza,  
suspect_flu,sore_throat,diagnosis_common_cold,  
diagnosis_influenza,,recommend_rest,GOAL. 
diagnosis_migraine,,recommend_dark_room,GOAL. 
no_appetite,stomach_pain,diagnosis_food_poisoning,GOAL

#### Python Code

```python
import csv
from io import StringIO
from typing import List, Set, Dict, Any

def load_rules(csv_content: str) -> List[Dict[str, Any]]:
    """
    Loads rules from the CSV content.
    Each rule is parsed into a dictionary with 'if' (set of conditions) and 'then' (new fact).
    """
    rules = []
    # Use StringIO to treat the string content as a file
    reader = csv.DictReader(StringIO(csv_content)) 
    
    for row in reader:
        # Collect conditions from the IF and optional AND columns
        conditions = {row['IF']}
        if row['AND']:
            conditions.add(row['AND'])
        
        rules.append({
            "if": conditions, 
            "then": row['THEN'],
            # The GOAL column helps identify terminal diagnosis or recommendations
            "is_goal": bool(row['GOAL'])
        })
    return rules

def forward_chaining_inference(rules: List[Dict[str, Any]], initial_facts: List[str]) -> Set[str]:
    """
    Performs forward chaining on the facts and rules to derive new facts.
    """
    # Initialize the set of known facts
    facts = set(initial_facts)
    print(f"--- Starting Inference with Initial Facts: {facts} ---\n")
    
    # The loop continues as long as new facts are being added
    new_fact_added = True
    iteration = 0
    
    # Forward chaining occurs in this main loop: repeatedly scan and apply rules
    while new_fact_added:
        new_fact_added = False
        iteration += 1
        
        print(f"--- Iteration {iteration} ---")
        
        for rule in rules:
            conditions_met = rule['if'].issubset(facts)
            new_fact = rule['then']
            
            # 1. Check IF condition (Pattern Matching)
            if conditions_met:
                # 2. IF rule is met AND the conclusion is new (Action/Assertion)
                if new_fact not in facts:
                    facts.add(new_fact)
                    new_fact_added = True
                    # The chain extends here: a new fact is added, potentially triggering other rules
                    print(f"  [APPLY] Rule: {rule['if']} -> {new_fact}")

        # If a goal fact was added in this iteration, we could stop here, 
        # but we let it run one more time to ensure all dependencies are resolved.
        print(f"  Current Derived Facts: {sorted(list(facts))}\n")

    return facts

# --- Main Program Execution ---

# Simulate reading the rules from the 'rules_diagnosis.csv' file content
RULES_CSV_CONTENT = """
IF,AND,THEN,GOAL
fever,cough,suspect_flu,
headache,nausea,suspect_migraine,
suspect_flu,body_aches,diagnosis_influenza,
suspect_flu,sore_throat,diagnosis_common_cold,
diagnosis_influenza,,recommend_rest,GOAL
diagnosis_migraine,,recommend_dark_room,GOAL
no_appetite,stomach_pain,diagnosis_food_poisoning,GOAL
"""

# Load the knowledge base
knowledge_base = load_rules(RULES_CSV_CONTENT)

# --- Scenario 1: Influenza ---
patient_facts_1 = ['fever', 'cough', 'body_aches']
final_facts_1 = forward_chaining_inference(knowledge_base, patient_facts_1)

# Extract goal results
goal_recommendations_1 = [r['then'] for r in knowledge_base if r['is_goal'] and r['then'] in final_facts_1]

print("====================================")
print(f"FINAL RESULT (Scenario 1: {patient_facts_1})")
print(f"Recommendations: {goal_recommendations_1 if goal_recommendations_1 else 'None'}")
print("====================================")

# --- Scenario 2: Food Poisoning ---
patient_facts_2 = ['no_appetite', 'stomach_pain']
final_facts_2 = forward_chaining_inference(knowledge_base, patient_facts_2)

# Extract goal results
goal_recommendations_2 = [r['then'] for r in knowledge_base if r['is_goal'] and r['then'] in final_facts_2]

print("====================================")
print(f"FINAL RESULT (Scenario 2: {patient_facts_2})")
print(f"Recommendations: {goal_recommendations_2 if goal_recommendations_2 else 'None'}")
print("====================================")

```



Note: Some parts of this document were initially drafted with assistance from Gemini 2.5 Flash


---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

[^1]: **A) Architectural Separation:** Rule-based systems established fundamental AI architecture by separating the  *Knowledge Base* from the *inference engine*, allowing rules to be easily modified without changing the program code.  **B) Formal Knowledge Representation:** They pioneered the structured representation of human logic making expert thought machine-readable for the first time. **C) Automated Reasoning:** The introduction of the *Inference Engine* provided computational *models* for deductive reasoning (like Forward and Backward Chaining), demonstrating how a computer could link discrete facts and rules to reach logical, non-obvious conclusions.

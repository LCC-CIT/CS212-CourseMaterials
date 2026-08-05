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

## Single Rule System

### Each Rule Leads to a Goal&mdash;"Hard Coded" Rules (if, elif, else)

In the last lab assignment, you wrote rule-based (expert) systems in which each branch of the if-elif statement lead to a diagnosis (a goal). The rules were very simple with just a few input parameters. This example just has two parameters:

```python
# A Simple Medical Diagnostic System
# Uses combined boolean conditions (AND/OR) within multi-branching to diagnose.

def diagnose_symptoms(has_fever, has_cough):
    """Provides a preliminary diagnosis based on binary symptoms."""
    # Convert booleans to strings for display
    fever_str = "Yes" if has_fever else "No"
    cough_str = "Yes" if has_cough else "No"
    print("-" * 30)
    print(f"Patient Symptoms: Fever ({fever_str}), Persistent Cough ({cough_str})")

    diagnosis = ""

    # Check for the combination of symptoms (Highest concern first)
    if has_fever and has_cough:
        diagnosis = "Flu - Recommend rest and hydration."
    elif has_fever and not has_cough:
        diagnosis = "Possible Infection - Recommend primary care physician visit."
    elif not has_fever and has_cough:
        diagnosis = "Cold/Allergies - Recommend over-the-counter medication."
    else: # not has_fever and not has_cough
        diagnosis = "General Check-up - Patient appears healthy."

    print(f"Diagnosis: {diagnosis}")

# Example 1: True Fever, True Cough (Flu)
diagnose_symptoms(True, True)
# Example 2: False Fever, True Cough (Cold)
diagnose_symptoms(False, True)

```



#### Each Rule Leads to a Goal&mdash;Rules in a List

Let's improve this by separating the rules from the code. In the following program:

- Each rule maps a set of symptoms directly to a final recommendation.
- The rules are in a list of dictionaries with these keys:
  - 'if': the set of facts (symptoms) required.
  - 'then': the final recommendation (the GOAL).

```python
# This function demonstrates simple rule-based classification (Pattern Matching)
# The rules are in lists of dictionaries

KNOWLEDGE_BASE = [
    # Rule 1:Flu/Cold symptoms
    {"if": {"fever", "cough", "sore_throat"}, "then": "Diagnosis: Common Cold - Recommend hot tea."},
    
    # Rule 2: Migraine
    {"if": {"headache", "nausea"}, "then": "Diagnosis: Migraine - Recommend dark room and quiet rest."},
    
    # Rule 3: Food Poisoning
    {"if": {"no_appetite", "stomach_pain"}, "then": "Diagnosis: Food Poisoning - Recommend bland diet and hydration."},
    
    # Rule 4: Fever
    {"if": {"fever"}, "then": "Diagnosis: Unknown Fever - Recommend taking temperature hourly."},
]

def direct_lookup_inference(rules, patient_facts):
    """
    Performs a single-pass search (lookup) for a matching rule.
    """
    facts_set = set(patient_facts)

    # The system only iterates through the rules once.
    for rule in rules:
        conditions_needed = rule['if']

        # Pattern Matching: Check if ALL conditions needed by the rule
        # are present in the patient's facts.
        conditions_met = conditions_needed.issubset(facts_set)

        if conditions_met:
            # We found a direct match! Return the immediate conclusion.
            return rule['then']

    # If the loop finishes without finding a match:
    return "Diagnosis: Undetermined. No direct rule matched all symptoms."
```



#### Chains of Rules Lead to a Goal&mdash;Rules in a List

A better way to do this is to make separate rules that can be chained:

- The rules are again defined as a list of dictionaries. The dictionary keys are:
  - 'if': A set of facts (strings) required to trigger the rule.
  - 'then': The new fact (string) derived when the rule fires.
  - 'is_goal': True if this fact is a final diagnosis or recommendation.

Here is a link to [a more detailed example](CS210-Unit02-2a-RuleDesign.html) of forward chaned rules with an explaination of how they work.

Here is an example program:

```python
# This program demonstrates rule-based forward chaining

# 1. HARDCODED KNOWLEDGE BASE (Rules)
# The rules are defined as a list of dictionaries. 
# The first dicitonary in each rule, with the key "if", has a set as it's value.
# 'if': A set of facts (strings) required to trigger the rule.
# 'then': The new fact (string) derived when the rule fires.
# 'is_goal': True if this fact is a final diagnosis or recommendation.

KNOWLEDGE_BASE = [
    # Rule 1: Suspect Flu
    {
        "if": {"fever", "cough"}, 
        "then": "suspect_flu", 
        "is_goal": False
    },
    
    # Rule 2: Suspect Migraine
    {
        "if": {"headache", "nausea"}, 
        "then": "suspect_migraine", 
        "is_goal": False
    },
    
    # Rule 3: Diagnosis Influenza (Chain 1 step: needs 'suspect_flu' derived from R1)
    {
        "if": {"suspect_flu", "body_aches"}, 
        "then": "diagnosis_influenza", 
        "is_goal": False
    },
    
    # Rule 4: Diagnosis Common Cold (Chain 1 step)
    {
        "if": {"suspect_flu", "sore_throat"}, 
        "then": "diagnosis_common_cold", 
        "is_goal": False
    },
    
    # Rule 5: Recommendation for Influenza (Chain 2 step: needs 'diagnosis_influenza' derived from R3)
    {
        "if": {"diagnosis_influenza"}, 
        "then": "recommend_rest", 
        "is_goal": True
    },
    
    # Rule 6: Recommendation for Migraine (Final Diagnosis)
    {
        "if": {"diagnosis_migraine"}, 
        "then": "recommend_dark_room", 
        "is_goal": True
    },
    
    # Rule 7: Diagnosis Food Poisoning (Final Diagnosis)
    {
        "if": {"no_appetite", "stomach_pain"}, 
        "then": "diagnosis_food_poisoning", 
        "is_goal": True
    },
]

def forward_chaining_inference(rules, initial_facts, verbose: bool = False):
    """
    Performs the core Forward Chaining inference process.
    The goal is to expand the 'facts' set using the 'rules'.

    Parameters:
    - rules: iterable of rule dicts with 'if' (set) and 'then' (conclusion)
    - initial_facts: iterable of starting fact strings
    - verbose: if True, prints iteration/apply/current-facts messages (default False)

    Returns:
    - set of derived facts
    """
    # Convert the list of facts into a set for fast lookup and easy modification.
    facts = set(initial_facts)
    if verbose:
        print(f"--- Starting Inference with Initial Facts: {facts} ---\n")

    # This variable controls the main loop (The Forward Chain).
    # If a rule fires and adds a new fact, this is set to True, and the loop repeats.
    new_fact_added = True
    iteration = 0

    # FORWARD CHAINING LOOP: Repeats until no new facts are found in a complete pass.
    while new_fact_added:
        new_fact_added = False  # Reset the flag for the start of the new pass
        iteration += 1

        if verbose:
            print(f"--- Iteration {iteration} ---")

        for rule in rules:
            conditions_needed = rule['if']
            new_fact = rule['then']

            # Check 1: Pattern Matching
            # Check if ALL conditions_needed are currently present in the 'facts' set.
            conditions_met = conditions_needed.issubset(facts)

            if conditions_met:
                # Check 2: Assertion/Action
                # Only add the new fact if it's not already known.
                if new_fact not in facts:
                    facts.add(new_fact)
                    new_fact_added = True
                    # This tells the 'while' loop to run again.
                    if verbose:
                        print(f"  [APPLY] Rule: Required: {conditions_needed} -> Derived: {new_fact}")

        if verbose:
            print(f"  Current Derived Facts: {sorted(list(facts))}\n")

    return facts

def extract_goals(rules, final_facts):
    """
    Finds all facts that were derived AND are marked as a 'goal' in the rules.
    This replaces the lambda/list comprehension filtering.
    """
    goal_recommendations = []
    
    for rule in rules:
        fact = rule['then']
        is_goal = rule['is_goal']
        
        # Check if the fact is a GOAL and if that fact was successfully derived
        if is_goal and fact in final_facts:
            goal_recommendations.append(fact)
            
    return goal_recommendations


# --- Main Program Execution ---

# --- Scenario 1: Influenza Chain ---
patient_facts_1 = ['fever', 'cough', 'body_aches']
final_facts_1 = forward_chaining_inference(KNOWLEDGE_BASE, patient_facts_1)

# Extract goal results using the simplified function
goal_recommendations_1 = extract_goals(KNOWLEDGE_BASE, final_facts_1)

print("====================================")
print(f"FINAL RESULT (Scenario 1: {patient_facts_1})")
print(f"Recommendations: {goal_recommendations_1 if goal_recommendations_1 else 'None'}")
print("====================================")

# --- Scenario 2: Food Poisoning ---
patient_facts_2 = ['no_appetite', 'stomach_pain']
final_facts_2 = forward_chaining_inference(KNOWLEDGE_BASE, patient_facts_2)

# Extract goal results
goal_recommendations_2 = extract_goals(KNOWLEDGE_BASE, final_facts_2)

print("====================================")
print(f"FINAL RESULT (Scenario 2: {patient_facts_2})")
print(f"Recommendations: {goal_recommendations_2 if goal_recommendations_2 else 'None'}")
print("====================================")


```



#### Chains of Rules Lead to a Goal&mdash;Rules in a File

```python
import csv
from io import StringIO
from typing import List, Set, Dict, Any

def load_rules(csv_content: str) -> List[Dict[str, Any]]:
    """
    Loads rules from the CSV content. Each rule is parsed into a dictionary.
    """
    rules = []
    # Try to parse as CSV with headers first (IF, AND, THEN, GOAL).
    content = csv_content.strip()
    reader = csv.DictReader(StringIO(content))

    fieldnames = reader.fieldnames or []
    normalized_fieldnames = [fn.strip().upper() for fn in fieldnames]

    # Parse positional columns (IF, AND, THEN, [GOAL])
    csv_reader = csv.reader(StringIO(content))
    for row in csv_reader:
        # Skip empty rows
        if not row or all(not cell.strip() for cell in row):
            continue

        # Map positional columns
        if_val = row[0].strip() if len(row) > 0 else ''
        and_val = row[1].strip() if len(row) > 1 else ''
        then_val = row[2].strip() if len(row) > 2 else ''
        goal_val = row[3].strip() if len(row) > 3 else ''

        if not if_val:
            continue

        conditions = {if_val}
        if and_val:
            conditions.add(and_val)

        rules.append({
            "if": conditions,
            "then": then_val,
            "is_goal": bool(goal_val)
        })
    return rules

def load_rules_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read rules from a CSV file path and return parsed rules list.
    Supports both header and header-less CSV files.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return load_rules(content)

def forward_chaining_inference(rules: List[Dict[str, Any]], initial_facts: List[str]) -> Set[str]:
    """
    Performs forward chaining on the facts and rules to derive new facts.

    Parameters:
    - rules: list of rule dicts with 'if' as set and 'then' as conclusion
    - initial_facts: list of starting facts
  
    Returns:
    - set of derived facts (including initial ones)
    """
    # Initialize the set of known facts
    facts = set(initial_facts)

    # The loop continues as long as new facts are being added
    new_fact_added = True
    iteration = 0

    # Forward chaining occurs in this main loop: repeatedly scan and apply rules
    while new_fact_added:
        new_fact_added = False
        iteration += 1

        for rule in rules:
            conditions_met = rule['if'].issubset(facts)
            new_fact = rule['then']

            # 1. Check IF condition (Pattern Matching)
            if conditions_met:
                # 2. IF rule is met AND the conclusion is new (Action/Assertion)
                if new_fact not in facts:
                    facts.add(new_fact)
                    new_fact_added = True
    return facts

def extract_goals(rules: List[Dict[str, Any]], facts: Set[str]) -> List[str]:
    """
    Return the list of rule conclusions that are marked as goals and present in facts.
    """
    return [r['then'] for r in rules if r.get('is_goal') and r['then'] in facts]

# -------- Main Program Execution --------

# Load the knowledge base from CSV file in the same directory
CSV_FILE = 'MedicalDiagnosis.csv'

# Try to load rules from the CSV file path; fall back to empty rules on error
try:
    knowledge_base = load_rules_from_file(CSV_FILE)
except FileNotFoundError:
    print(f"Warning: {CSV_FILE} not found. No rules loaded.")
    knowledge_base = []

# --- Scenario 1: Influenza ---
patient_facts_1 = ['fever', 'cough', 'body_aches']
final_facts_1 = forward_chaining_inference(knowledge_base, patient_facts_1)

# Extract goal results
goal_recommendations_1 = extract_goals(knowledge_base, final_facts_1)

print("====================================")
print(f"FINAL RESULT (Scenario 1: {patient_facts_1})")
print(f"Recommendations: {goal_recommendations_1 if goal_recommendations_1 else 'None'}")
print("====================================")

# --- Scenario 2: Food Poisoning ---
patient_facts_2 = ['no_appetite', 'stomach_pain']
final_facts_2 = forward_chaining_inference(knowledge_base, patient_facts_2)

# Extract goal results
goal_recommendations_2 = extract_goals(knowledge_base, final_facts_2)

print("====================================")
print(f"FINAL RESULT (Scenario 2: {patient_facts_2})")
print(f"Recommendations: {goal_recommendations_2 if goal_recommendations_2 else 'None'}")
print("====================================")

```

## References

- [What are Expert Systems in Artificial Intelligence?](https://www.mygreatlearning.com/blog/expert-systems-in-artificial-intelligence/) By [Samudyata Bhat](https://www.mygreatlearning.com/blog/author/samudyata/) Updated on Feb 6, 2025 on Great Learning.
- 

Note: Some parts of this document were initially drafted with assistance from Gemini 2.5 Flash


---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

[^1]: TBD

<h1>Symbolic AI Lab Assignment Ideas</h1>

<h2>Contents</h2>

[TOC]

## Lab Assignment Ideas

These are potential lab assignments (all in Python) for CS 212

## Rule-Based Reasoning Labs

### 1. Medical Diagnosis Expert System

- **Task:** Implement a forward-chaining rule-based system to diagnose simple diseases from symptoms.

- **Learning Goals:**
- Encode knowledge as IF–THEN rules.
  - Practice forward chaining and inference.

- **Extensions:** Add backward chaining (goal-driven reasoning).

### 2. Animal Classification System

- **Task:** Write a program that classifies animals (e.g., mammal, bird, reptile) based on observable traits using rules.

- **Learning Goals:**

  - Practice building rule bases.
  - Implement efficient matching (mini Rete-style).
  
  

## Logic Programming Labs

### 3. Family Tree Inference

- **Task:** Using kanren, represent family relationships (parent, grandparent, sibling). Query relationships like “Who are Alice’s cousins?”

- **Learning Goals:**

  - Represent knowledge declaratively.
  - Understand unification and relational queries.
  
### 4. Simple Scheduling Problem

- **Task:** Use logic constraints to assign courses, professors, and rooms without conflicts.

- **Learning Goals:**

  - Apply symbolic constraints to solve real-world problems.
  - Compare declarative vs procedural problem-solving.
  
  

## Search & Planning Labs

### 5. Puzzle Solver (8-puzzle, Towers of Hanoi)

- **Task:** Implement BFS, DFS, and A* search to solve a symbolic puzzle.

- **Learning Goals:**
- Understand state-space representation.
  - Compare uninformed vs informed search.


### 6. Robot Pathfinding in a Grid World

- **Task:** Represent a grid world with obstacles; implement A* to find the shortest path.

- **Learning Goals:**

  - Symbolic representation of environment.
  - Heuristic design (Manhattan vs Euclidean distance).
  
  

### 7. Planning with STRIPS-like Actions

- **Task:** Represent actions (preconditions, effects) and goals; implement a simple planner.

- **Learning Goals:**

  - Encode operators symbolically.
  - Connect symbolic reasoning to search.
  
  

## Knowledge Representation Labs

### 8. Semantic Network Explorer

- **Task:** Build a small semantic network (e.g., zoo ontology) and allow queries like “Can a penguin fly?”

- **Learning Goals:**
- Implement inheritance and property lookup.
  - Introduce ontologies and reasoning.


### 9. Frame-Based Restaurant Scenario

- **Task:** Represent a restaurant script (customer orders, eats, pays). Students simulate variations.

- **Learning Goals:**

  - Model stereotypical events with symbolic frames.
  - Understand how knowledge guides reasoning.
  
  

## Symbolic NLP Labs



### 10. CFG Sentence Parser

- **Task:** Use NLTK to write a context-free grammar and parse sentences like “John loves Mary.”

- **Learning Goals:**
- Represent grammar rules symbolically.
  - Link syntax parsing to AI reasoning.


### 11. Rule-Based Chatbot

- **Task:** Build a simple chatbot using pattern matching and rules (mini ELIZA).

- **Learning Goals:**

  - Symbolic natural language understanding.
  - Contrast symbolic rules with modern ML-based NLP.
  
  

## Capstone Mini-Projects

- **Mini Expert System:** Students choose a domain (travel advisor, tech support, medical triage).

- **Knowledge-Based Game:** Implement Tic-Tac-Toe with symbolic reasoning.

- **Hybrid System:** Combine search + rules (e.g., robot planning with symbolic action rules).

  

---

This document was drafted by Brian Bird using ChatGPT 5, 8/22/25

---
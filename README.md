# ER-Breast-Cancer-Boolean-Network-Simulation
This project implements a Boolean network model to simulate signal transduction pathways and drug responses in ER+ (estrogen receptor-positive) breast cancer. By representing genes, proteins, and cellular processes as logical nodes (ON/OFF), the model predicts how different combinatorial drug treatments affect cell fate decisions—specifically, maximizing apoptosis (cell death) and minimizing proliferation (cell growth).

# Project Overview
In this computational model, each node's state is determined by logical rules based on its upstream regulators. The script systematically tests single and combinatorial drug treatments to find the most effective therapeutic strategy.   
Key components of the implementation include:
+ Model Parsing: Parses Boolean rules from a text file (```breast_cancer.txt```), safely mapping expressions to Python dictionaries and utilizing ```eval()``` for logical state updates.
+ Network Categorization: Automatically identifies specific node types:
  + *Drugs* (e.g., Fulvestrant, Alpelisib, Palbociclib, etc.).
  + *Roots* (genetic signatures without upstream parents, initialized randomly).
  + *Phenotypes* (Proliferation and Apoptosis nodes).
+ Attractor Discovery: Simulates state transitions iteratively until the network reaches a steady state or cyclic attractor (i.e., a previously seen state).
+ Drug Efficacy Scoring (V-Score): Evaluates the effectiveness of a drug combination using the formula: ```V = SUM(Apoptosis ON) - SUM(Proliferation ON)```.
+ Combinatorial Testing: Iterates through all possible combinations of drugs for $N=1$ through $N=7$ active drugs, running the simulation 100 times per combination to calculate the average V-Score and determine the absolute best combinatorial treatment.
+ Update Modes (Bonus): Supports both synchronous (updating all nodes simultaneously) and asynchronous (updating one random node per iteration) network updates.

# Setup and Data 
This project relies on a network model from the following publication:
Gómez Tejeda Zañudo J, Scaltriti M, Albert R. A network modeling approach to elucidate drug resistance mechanisms and predict combinatorial drug treatments in breast cancer. Cancer Converg. 2017.
You will need the [```breast_cancer.txt```](https://github.com/kantale/python_lessons/blob/master/projects_2025_2026/project_5/breast_cancer.txt) file containing the Boolean rules in the format ```Node* = expression```.

# Usage
Execute the main script from your terminal:   
```
python Project_5.py
```

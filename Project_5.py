### Simulating Signal Transduction and Drug Response in ER+ Breast Cancer using Boolean Networks

############ Project 5 ############ 

filename="/home/ioanna/metaptixiako/kanterakis/breast_cancer.txt"

####Task 1
rules={}

def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            line=line.strip()
            if line.startswith('#'):
                continue

            if '*=' in line:
                node, expression=line.split('*=', 1)
                rules[node.strip()]=expression.strip()

    return rules

rules=parse_file(filename)


####Task 2
drugs=['Fulvestrant', 'Alpelisib', 'Everolimus', 'Trametinib', 'Ipatasertib', 'Palbociclib', 'Neratinib']
proliferation_nodes=['Proliferation', 'Proliferation_2', 'Proliferation_3', 'Proliferation_4']
apoptosis_nodes=['Apoptosis', 'Apoptosis_2', 'Apoptosis_3']

def find_roots(rules, drugs): #roots are the nodes that are like this: Node*=Node and are not drugs
    roots=set()

    for node, expression in rules.items():
        if node==expression:
            if node not in drugs:
                roots.add(node)
    
    return roots

roots=find_roots(rules,drugs)


####Task 3
import random

def create_initial_state(rules, roots, drugs, proliferation, apoptosis, active_drugs): #creates a dictionary that tells which node in On/Off (we make the list of active_drugs)
    state={}
    all_nodes=list(rules.keys()) #we get all nodes
    random.shuffle(all_nodes) #we shuffle the nodes for random initialization

    for node in all_nodes:
        if node in active_drugs:
            state[node]=True #active drugs are On
        elif node in drugs:
            state[node]=False #the rest drugs are Off
        elif node in proliferation or node in apoptosis: #results (proliferation and apoptosis) are Off
            state[node]=False
        elif node in roots: #roots are random On or Off
            state[node]=random.choice([True, False])
        else: #the rest nodes are random On or Off
            state[node]=random.choice([True, False])
    
    return state

def calculate_next_state(rules, current_state): #creates a dictionary of the next state based on a dictionary of the current state
    next_state={}

    for node, expression in rules.items():
        value=eval(expression, {}, current_state)
        next_state[node]=bool(value)
    
    return next_state


####Bonus
def calculate_next_state_async(rules, current_state):
    next_state=current_state.copy() 
    nodes=list(rules.keys())
    node_to_update=random.choice(nodes)
    expression=rules[node_to_update]
    value=bool(eval(expression, {}, current_state))
    next_state[node_to_update]=value

    return next_state



####Task 4 + Bonus (we add mode)
def run_until_existed_state(initial_state,rules,mode):
    current_state=initial_state
    seen_states=set() #the states we have seen

    while True:
        state=tuple(sorted(current_state.items())) #we make the dictionary in a sorted tuple that can be put in a set and to compare with next states
        if state in seen_states: #if we have seen the current state again, we get that state
            return current_state
        seen_states.add(state) #if not, we add it to seen states
        
        ##Bonus
        if mode=='synchronous':
            current_state=calculate_next_state(rules,current_state) #we calculate the next state
        else:
            current_state=calculate_next_state_async(rules,current_state)


def calculate_v(state, proliferation_nodes, apoptosis_nodes):
    proliferation_on=0
    apoptosis_on=0

    for node in proliferation_nodes:
        if state[node]==True:
            proliferation_on+=1
    for node in apoptosis_nodes:
        if state[node]==True:
            apoptosis_on+=1
    v=apoptosis_on-proliferation_on
    return v


####Tasks 5-7
runs=100

def get_combinations(drugs, N): #gives the combination of drugs for N
    if N==1:
        return [(drug,) for drug in drugs]
    
    combos=[]
    for i in range(len(drugs)):
        first_drugs=drugs[i]
        remaining=drugs[i+1:]
        if len(remaining)<N-1:
            continue
        sub_combos=get_combinations(remaining, N-1)
        for sub_combo in sub_combos:
            combos.append((first_drugs,)+sub_combo)
    return combos

#Bonus (add mode)
def get_average_v_scores_for_N(rules,roots,drugs,proliferation_nodes,apoptosis_nodes,runs,N,mode): #runs the model for N active drugs and returns a dictionary with the v scores
    combos_N=get_combinations(drugs,N)
    print(f'There are {len(combos_N)}')

    combo_scores={}
    
    count=0
    for combo in combos_N:
        active_drugs=list(combo)
        v_scores_for_this_combo=[]
        for i in range(runs):
            initial_state=create_initial_state(rules,roots,drugs,proliferation_nodes,apoptosis_nodes,active_drugs)
            #Bonus
            final_state=run_until_existed_state(initial_state,rules,mode)
            v=calculate_v(final_state,proliferation_nodes,apoptosis_nodes)
            v_scores_for_this_combo.append(v)
        
        average_v=sum(v_scores_for_this_combo)/len(v_scores_for_this_combo)
        combo_scores[combo]=average_v
        count+=1
        print(f'Combo N={N} ({count}/{len(combos_N)}), Completed combo: {combo}, V= {average_v}')
    print(f'Complete for N={N}')
    
    return combo_scores


overall_best_combo=()
overall_best_score=-100
mode='asynchronous'

for n in range(1, len(drugs)+1):
    print(f'Begin for N={n}')
    #Bonus
    scores_for_this_N=get_average_v_scores_for_N(rules,roots,drugs,proliferation_nodes,apoptosis_nodes,runs,n,mode)
    best_score_N=-100
    best_combo_N=()
    for combo, score in scores_for_this_N.items():
        if score>best_score_N:
            best_score_N=score
            best_combo_N=combo

    print(f'Results for N={n}')
    print(f'Best combination: {best_combo_N}')
    print(f'V score= {best_score_N}')

    if best_score_N>overall_best_score:
        overall_best_score=best_score_N
        overall_best_combo=best_combo_N

print(f'For {mode} mode')
print(f'The best overall combo of drugs is: {overall_best_combo}')
print(f'V score= {overall_best_score}')

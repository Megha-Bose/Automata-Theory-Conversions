# Conversion from NFA to DFA
import json
import sys

dfa = {}
nfa = {}
nfa_states = []
dfa_states = []

def get_power_set(nfa_st):
    powerset = [[]]
    for i in nfa_st:
        for sub in powerset:
            powerset = powerset + [list(sub) + [i]]
    return powerset

def load_nfa():
    global nfa
    with open(sys.argv[1], 'r') as inpjson:
        nfa = json.loads(inpjson.read())

def out_dfa():
    global dfa
    with open(sys.argv[2], 'w') as outjson:
        outjson.write(json.dumps(dfa, indent = 4))

if __name__ == "__main__":
    load_nfa()
    
    dfa['states'] = []
    dfa['letters'] = nfa['letters']
    dfa['transition_function'] = []
    
    for state in nfa['states']:
        nfa_states.append(state)

    dfa_states = get_power_set(nfa_states)


    dfa['states'] = []
    for states in dfa_states:
        temp = []
        for state in states:
            temp.append(state)
        dfa['states'].append(temp)

    for states in dfa_states:
        for letter in nfa['letters']:
            q_to = []
            for state in states:
                for val in nfa['transition_function']:
                    start = val[0]
                    inp = val[1]
                    end = val[2]
                    if state == start and letter == inp:
                        if end not in q_to:
                            q_to.append(end)
            q_states = []
            for i in states:
                q_states.append(i)
            dfa['transition_function'].append([q_states, letter, q_to])

    dfa['start_states'] = []
    for state in nfa['start_states']:
        dfa['start_states'].append([state])
    dfa['final_states'] = []
    for states in dfa['states']:
        for state in states:
            if state in nfa['final_states'] and states not in dfa['final_states']:
                dfa['final_states'].append(states)
    
    out_dfa()



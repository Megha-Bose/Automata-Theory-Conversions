# Conversion from DFA to Regex

import json
import sys
import copy

reg_exp = ''
dfa = {}

def get_input_symbol():
    global dfa
    input_symbols = {st: {to: '' for to in dfa['states']} for st in dfa['states']}
    for val in dfa['transition_function']:
        if input_symbols[val[0]][val[2]] == '':
            input_symbols[val[0]][val[2]] = val[1]
        else:
            input_symbols[val[0]][val[2]] += '+' + val[1]
    return input_symbols

def get_pred_succ(state, input_symbols):
    global dfa
    predecessors = []
    successors = []
    curr_dict_for_from = {st: {to: v for to, v in val.items() if to == state} for st, val in input_symbols.items()}

    for predecessor in dfa['states']:
        if predecessor not in curr_dict_for_from.keys() or predecessor == state:
            continue
        if curr_dict_for_from[predecessor][state] != '':
            predecessors.append(predecessor)

    for successor in dfa['states']:
        if successor not in input_symbols[state].keys() or state == successor:
            continue
        if input_symbols[state][successor] != '':
            successors.append(successor)
    return predecessors, successors

def check_self_loop(state):
    if input_symbols[state][state] == '':
        return False
    return True

def DFA_to_regex(input_symbols, state_intitial, state_final):
    global dfa
    for state in dfa['states']:
        if state == state_intitial or state == state_final:
            continue
        predecessors, successors = get_pred_succ(state, input_symbols)
        for predecessor in predecessors:
            if predecessor in input_symbols.keys():
                for successor in successors:
                    if successor in input_symbols[predecessor].keys():

                        pre_suc_input_exp = ''
                        self_loop_input_exp = ''
                        from_pre_input_exp = ''
                        to_suc_input_exp = ''

                        if input_symbols[predecessor][successor] != '':
                            pre_suc_input_exp = '(' + input_symbols[predecessor][successor] + ')'
                        
                        if check_self_loop(state):
                            self_loop_input_exp = '(' + input_symbols[state][state] + ')' + '*'
                        
                        if input_symbols[predecessor][state] != '':
                            from_pre_input_exp = '(' + input_symbols[predecessor][state] + ')'
                        
                        if input_symbols[state][successor] != '':
                            to_suc_input_exp = '(' + input_symbols[state][successor] + ')'

                        new_pre_suc_input_exp = from_pre_input_exp + self_loop_input_exp + to_suc_input_exp

                        if pre_suc_input_exp != '':
                            new_pre_suc_input_exp += ('+' + pre_suc_input_exp)

                        input_symbols[predecessor][successor] = new_pre_suc_input_exp
        # remove the state
        input_symbols = {st: {to: v for to, v in inp.items() if to != state} for st, inp in input_symbols.items() if st != state}
    return input_symbols[state_intitial][state_final]


def start_has_incoming():
    global dfa
    check = False
    initial_state = dfa['start_states'][0]
    for dfa_transition in dfa['transition_function']:
        if dfa_transition[2] == initial_state:
            check = True
            break
    return check

def end_has_outgoing():
    global dfa
    check = False
    if len(dfa['final_states']) > 1:
        return True
    final_state = dfa['final_states'][0]
    for dfa_transition in dfa['transition_function']:
        if dfa_transition[0] == final_state:
            check = True
            break
    return check

def handle_start_incoming():
    global dfa
    if start_has_incoming():
        dfa['states'].append("Qi")
        dfa['transition_function'].append(["Qi", "$", dfa['start_states'][0]])
        dfa['start_states'] = ["Qi"]

def handle_final_outgoing():
    global dfa
    if end_has_outgoing():
        dfa['states'].append("Qf")
        for final_state in dfa['final_states']:
            dfa['transition_function'].append([final_state, "$", "Qf"])
        dfa['final_states'] = ["Qf"]


def load_dfa():
    global dfa
    with open(sys.argv[1], 'r') as inpjson:
        dfa = json.loads(inpjson.read())

def out_regex(regexp):
    reg = {}
    reg['regex'] = regexp
    with open(sys.argv[2], 'w') as outjson:
        outjson.write(json.dumps(reg, indent = 4))

if __name__ == '__main__':
    load_dfa()

    handle_start_incoming()
    handle_final_outgoing()

    input_symbols = get_input_symbol()
    reg_exp = DFA_to_regex(input_symbols, dfa['start_states'][0], dfa['final_states'][0])
    out_regex(reg_exp)

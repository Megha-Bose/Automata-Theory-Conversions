# Automata Theory Assignment

## Conversions covered:

1. Convert regular expression to NFA
2. Convert NFA to DFA
3. Convert DFA to Regular expression.
4. Minimize a DFA 

## Run
`python3 q<no>.py arg1 arg2` where arg1 is the path to the input JSON file and arg2 is the path to the output JSON file.


## Overview

## Symbols 
- '+' : union 
- '*' : star 
- '$' : epsilon 
- '()' : grouping

## I/O formats
Given for each question.

## Problem 1: Converting Regex to NFA

### Approach

1. We first add "." symbol for concatenation for convenience in add_concat().
2. We create the postfix form of the regular expression given according to the precedence order of operations given in compute_postfix().
3. Then we make the expression tree in the make_exp_tree() function from the postfix expression we got.
4. Now we compute_regex() using this expression tree we got. We pass the root of the expression tree to this function.
5. According to the operation encountered, we go to respective function to evaluate it.
6. Each state consists of dictionary contatining (input, next state) pairs.
7. Each computation returns its start and end state.
8. In do_concat(), we concatenate the left and right side of "." after computing them. Then the end of left is joined to start of right using epsilon "$".
9. In do_union(), we compute the left and right side of "+" and then we join the start state created to the start of these two by "$". Similarly, we join the end of these to the end state created by "$". Then we return the start and end node.
10. In do_kleene_star(), we compute the expression to be starred. Then we join its start and end state created to the start state created by "$" and also join them to the end of the computed nfa to complete the loop.
11. Encountering a symbol makes two states, start and end, joined by the symbol and returns the states.
12. Then we make the NFA object as required. We have the states along with their transitions now. We add all the states and transition function.
13. We get start states by adding the start and states connected to it by "$" and similarly we get the final states.
14. We output the nfa as a json object.

## Problem 2: Converting NFA to DFA

### Approach
1. After loading the nfa, we first get the power set of the nfa states to get dfa states.
2. Then for each state in the dfa, we append the states where the nfa states in it transition to and take their union.
3. The start states of the DFA are the start states of the NFA.
4. The final states of DFA consist of all the states that have at least one final NFA state. We include them in the dfa final states.
5. We output the dfa as json object. 


## Problem 3: Converting DFA to Regex

### Approach
1. We use state elimination method to convert the DFA to regex.
3. input_symbols[i][j] stores the expression connecting states i and j.
4. We first check if start state has incoming edge. If it does, we add a start state Qi with no incoming edges and join it to the current start state. Qi becomes new initial state.
5. We check there are multiple final sattes or if the final state has outgoing edges. If that is the case, we add a final state Qf with no outgoing edges and join the final states to it. Qf becomes new final state. 
6. For each of the intermediate states, we eliminate them one by one by joining their predecessors and successors.
7. Input expression on predecessor to current state is added to self loop on the current state, if present with "*" and finally the input expression that joins current_state with successor is added to it. This gives the updated value of joining predecessor with successor.
8. The input expressions on edges joining current state to other states are then eliminated from the input_symbols.
9. After eliminating all the intermediate nodes, we have our regular expresision required as input expression joining initial state to final state.

## Problem 4: Minimising DFA

### Approach
1. After loading the DFA, first we remove the states unreachable from the start state. For that we get the reachable states from start state and then update the states and transition function considering only reachable states.  
2. For minimising DFA, we calculate the 0-equivalence classes, 1-equivalence classes... till we donot need any more split.
3. First we split the final and non-final states. Then, in each iteration we check whether states in the same group transition to states in the same group. If they are not, we split the states considered.
4. We do the grouping using group[(tuple of state pair)] which contains bool for whether the states are in same group or not.
5. Finally to get the groups, we use disjoint set union. We then get the new_states and compute the transition function using these new states taking all transitions from one state set to other.
6. We compute the start and end states by taking the states containing at least one start state and end state respectively.

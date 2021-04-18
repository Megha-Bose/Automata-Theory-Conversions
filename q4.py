# Minimise DFA

import json 
import sys

dfa = {}
reachable_states = []
split_needed = None
dis_set = None

class DisjointSet(object):

	def __init__(self,items):

		self._disjoint_set = list()

		if items:
			for item in set(items):
				self._disjoint_set.append([item])

	def _get_index(self,item):
		for s in self._disjoint_set:
			for _item in s:
				if _item == item:
					return self._disjoint_set.index(s)
		return None

	def find(self,item):
		for s in self._disjoint_set:
			if item in s:
				return s
		return None

	def find_set(self, item):

		s = self._get_index(item)

		return s+1 if s is not None else None 

	def union(self,item1,item2):
		i = self._get_index(item1)
		j = self._get_index(item2)

		if i != j:
			self._disjoint_set[i] += self._disjoint_set[j]
			del self._disjoint_set[j]
	
	def get(self):
		return self._disjoint_set


def reachable_dfs(node):
    global dfa, reachable_states
    for val in dfa['transition_function']:
        start = val[0]
        inp = val[1]
        end = val[2]
        
        if start == node:
            if end not in reachable_states:
                reachable_states.append(end)
                reachable_dfs(end)


def remove_unreachable_states():
    global dfa, reachable_states

    for st in dfa['start_states']:
        reachable_states.append(st)
        reachable_dfs(st)

    dfa['states'] = [state for state in dfa['states'] if state in reachable_states]
    
    dfa['final_states'] = [state for state in dfa['final_states'] if state in reachable_states]

    temp = []

    for val in dfa['transition_function']:
        if val[0] in reachable_states:
            temp.append(val)

    dfa['transition_function'] = temp

def order_tuple(a,b):
	return (a,b) if a < b else (b,a)

def get_to_state(start, inp):
    global dfa
    for val in dfa['transition_function']:
        if start == val[0] and inp == val[1]:
            return val[2]

def minimiseDFA():
    global dfa, split_needed, dis_set
    split_needed = 1
    prev_states = []
    new_states = []

    non_final = []
    final = []

    for state in dfa['states']:
        if state not in dfa['final_states']:
            non_final.append(state)
        else:
            final.append(state)

    prev_states.append(non_final)
    prev_states.append(final)

    group = {}

    sorted_states = sorted(dfa['states'])

    for i, st1 in enumerate(sorted_states):
        for st2 in sorted_states[i+1 : ]:
            group[(st1, st2)] = (st1 in dfa['final_states']) == (st2 in dfa['final_states'])

    split_needed = True

    while split_needed:
        split_needed = False

        for i, st1 in enumerate(sorted_states):
            for st2 in sorted_states[i+1 : ]:

                if not group[(st1, st2)]:
                    continue

                for letter in dfa['letters']:
                    to1 = get_to_state(st1, letter)
                    to2 = get_to_state(st2, letter)

                    if to1 != None and to2 != None and to1 != to2:
                        is_same_grp = group[order_tuple(to1, to2)]
                        split_needed = split_needed or not is_same_grp
                        group[(st1, st2)] = is_same_grp
                        
                        if not is_same_grp:
                            break

    dis_set = DisjointSet(dfa['states'])

    # form new states
    for st_pair, is_same_grp in group.items():
        if is_same_grp:
            dis_set.union(st_pair[0], st_pair[1])

    dfa_new_states = []
    for state in dfa['states']:
        new = dis_set.find(state)
        if new not in dfa_new_states:
            dfa_new_states.append(new)
            
    dfa['states'] = dfa_new_states
    
    dfa_new_transition = []
    for val in dfa['transition_function']:
        start = val[0]
        inp = val[1]
        end = val[2]
        new_state1 = dis_set.find(start)
        new_state2 = dis_set.find(end)
        transition = []
        transition.append(new_state1)
        transition.append(inp)
        transition.append(new_state2)
        if transition not in dfa_new_transition:
            dfa_new_transition.append(transition)
    dfa['transition_function'] = dfa_new_transition

    # dfa['final_states'] = dis_set.get()   
    final_states = []
    for fi_state in dfa['final_states']:
        fi_set = dis_set.find(fi_state)
        if fi_set not in final_states:
            final_states.append(fi_set)

    dfa['final_states'] = final_states
    
    start_states = []
    for st_state in dfa['start_states']:
        st_set = dis_set.find(st_state)
        if st_set not in start_states:
            start_states.append(st_set)
    
    dfa['start_states'] = start_states

def load_dfa():
    global dfa
    with open(sys.argv[1], 'r') as inpjson:
        dfa = json.loads(inpjson.read())

def out_min_dfa():
    global dfa
    with open(sys.argv[2], 'w') as outjson:
        outjson.write(json.dumps(dfa, indent = 4))


if __name__ == "__main__":
    load_dfa()
    remove_unreachable_states()
    minimiseDFA()
    out_min_dfa()

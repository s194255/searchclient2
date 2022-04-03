# coding: utf-8
#
# Copyright 2021 The Technical University of Denmark
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from copy import deepcopy

def OR_search(state, problem, path, results, action_set,d):
    # print("or search", file=sys.stderr)
    if problem.is_goal(state):
        return {}
    if state in path:
        return False
    if d == 0:
        return False
    actions = state.get_applicable_actions(action_set)
    # print("actions!!!:", actions, file=sys.stderr)
    for action in actions:
        plan = AND_search(results(state, action), problem, [state] + path, results, action_set,d)
        if plan != False:
            plan[state] = action
            # print(plan, file=sys.stderr)
            # print("chips", file=sys.stderr)
            return plan
    return False

def AND_search(states, problem, path, results, action_set,d):
    # print("and search", file=sys.stderr)
    plan = {}
    for i in range(len(states)):
        s = states[i]
        p = OR_search(s, problem, path, results, action_set,d-1)
        if p != False:
            plan.update(p)
        if p == False:
            return False
        # print(plan, file=sys.stderr)
        # print("chips2", file=sys.stderr)
    return plan


def and_or_graph_search(initial_state, action_set, goal_description, results):
    d = 20

    # Here you should implement AND-OR-GRAPH-SEARCH. We are going to use a policy format, mapping from states to actions.
    # The algorithm should return a pair (worst_case_length, or_plan)
    # where the or_plan is a dictionary with states as keys and actions as values
    or_plan = OR_search(initial_state, goal_description, [], results, action_set, d)
    if or_plan == False:
        d = None
    # print(or_plan, file=sys.stderr)
    return d, or_plan

    # raise NotImplementedError()
def cyclic_OR_search(state, problem, path, results, action_set,d):
    # print("or search", file=sys.stderr)
    if problem.is_goal(state):
        return {}
    if state in path:
        return 'loop'
    if d == 0:
        return False
    cyclic_plan = None
    actions = state.get_applicable_actions(action_set)
    # print("actions!!!:", actions, file=sys.stderr)
    for action in actions:
        plan = cyclic_AND_search(results(state, action, action_set), problem, [state] + path, results, action_set,d)
        # print("plan",plan, file=sys.stderr)
        if plan != False:
            plan[state] = action
            # print(plan, file=sys.stderr)
            # print("chips", file=sys.stderr)
            return plan
    return False

def cyclic_AND_search(states, problem, path, results, action_set, d):
    # print("and search", file=sys.stderr)
    plan = {}
    loopy = True
    for i in range(len(states)):
        s = states[i]
        p = cyclic_OR_search(s, problem, path, results, action_set, d - 1)
        # print("p",p, file=sys.stderr)
        if p == False:
            return False
        if p != 'loop':
            loopy = False
        if p != False and p != 'loop':
            plan.update(p)
        # print("nothing happened in state {}".format(s), file=sys.stderr)
    if not loopy:
        return plan
        # print(plan, file=sys.stderr)
        # print("chips2", file=sys.stderr)
    return False


def cyclic_and_or_graph_search(initial_state, action_set, goal_description, results):
    d = 20

    # Here you should implement AND-OR-GRAPH-SEARCH. We are going to use a policy format, mapping from states to actions.
    # The algorithm should return a pair (worst_case_length, or_plan)
    # where the or_plan is a dictionary with states as keys and actions as values
    or_plan = cyclic_OR_search(initial_state, goal_description, [], results, action_set, d)
    if or_plan == False:
        d = None
    # print(or_plan, file=sys.stderr)
    return d, or_plan


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

def OR_search(state, problem, path, results, action_set, d):
    print("or search", file=sys.stderr)
    if problem.is_goal(state):
        return {}
    if state in path:
        return False
    if d == 0:
        if problem.is_goal(state):
            return path
        else:
            return False


    actions = state.get_applicable_actions(action_set)
    for action in actions:
        plan = AND_search(results(state, action), problem, [state] + path, results, action_set,d)
        if plan != False:
            plan[state] = action
            return plan

    return False

def AND_search(states, problem, path, results, action_set, d):
    print("and search", file=sys.stderr)
    plan = {}
    for i in range(len(states)):
        s = states[i]
        plan[s] = OR_search(s, problem, path, results, action_set, d-1)
        if plan[s] == False:
            return False
        return plan[s]


def and_or_graph_search(initial_state, action_set, goal_description, results):
    d = 1000

    # Here you should implement AND-OR-GRAPH-SEARCH. We are going to use a policy format, mapping from states to actions.
    # The algorithm should return a pair (worst_case_length, or_plan)
    # where the or_plan is a dictionary with states as keys and actions as values
    or_plan = OR_search(initial_state, goal_description, [], results, action_set, d)
    if or_plan == False:
        d = None
    return d, or_plan

    # raise NotImplementedError()

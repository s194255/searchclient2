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

import random
from search_algorithms.and_or_graph_search import cyclic_and_or_graph_search
from utils import *


def broken_results(state, action, action_set):
    # Building the Results() function containing the indeterminism
    # If performing two of the same actions is possible from the state,
    # this result is added as a possible outcome..
    standard_case = state.result(action)

# action set for problem
# =============================================================================
# [NoOp, Move(N), Move(S), Move(E), Move(W), Push(N, N), Push(E, E), Push(S, S), Push(W, W), Push(N, E),
#  Push(N, W), Push(E, N), Push(E, S), Push(S, E), Push(S, W), Push(W, N), Push(W, S)]
# =============================================================================7
    p = random.random()
    if str(action[0])[0:4] == 'Push':
        action_dic = {action_set[0][5]: action_set[0][9] if p < 0.5 else action_set[0][10],
                      action_set[0][6]: action_set[0][11] if p < 0.5 else action_set[0][12],
                      action_set[0][7]: action_set[0][13] if p < 0.5 else action_set[0][14],
                      action_set[0][8]: action_set[0][15] if p < 0.5 else action_set[0][16],
                      action_set[0][9]: action_set[0][5],
                      action_set[0][10]: action_set[0][5],
                      action_set[0][11]: action_set[0][6],
                      action_set[0][12]: action_set[0][6],
                      action_set[0][13]: action_set[0][7],
                      action_set[0][14]: action_set[0][7],
                      action_set[0][15]: action_set[0][8],
                      action_set[0][16]: action_set[0][8]}

        ortho_action = [action_dic[action[0]]]
        if state.is_applicable(ortho_action):
            broken_case = state.result(ortho_action)
            return [standard_case, broken_case]
        else:
            return [standard_case]
    else:
        return [standard_case]

CHANCE_OF_EXTRA_ACTION = 0.5

def non_deterministic_advanced_agent_type(level, initial_state, action_library, goal_description):
    # Create an action set for a single agent.
    action_library = action_library[0:5] + action_library[17:] # remove the pull actions
    action_set = [action_library]
    print(action_set, file=sys.stderr)

    # Call AND-OR-GRAPH-SEARCH to compute a conditional plan
    worst_case_length, plan = cyclic_and_or_graph_search(initial_state, action_set, goal_description, broken_results)

    if worst_case_length is None:
        print("Failed to find strong plan!", file=sys.stderr)
        return

    print("Found plan of worst-case length", worst_case_length, file=sys.stderr)

    current_state = initial_state

    while True:
        # If we have reached the goal, then we are done
        if goal_description.is_goal(current_state):
            break

        if current_state not in plan:
            # The agent reached a state not covered by the plan; AND-OR-GRAPH-SEARCH failed.
            print(f"Reached state not covered by plan!\n{current_state}", file=sys.stderr)
            break

        # Otherwise, read the correct action to execute
        joint_action = plan[current_state]

        p = random.random()
        if str(joint_action[0])[0:4] == 'Push':
            action_dic = {action_set[0][5]: action_set[0][9] if p < 0.5 else action_set[0][10],
                          action_set[0][6]: action_set[0][11] if p < 0.5 else action_set[0][12],
                          action_set[0][7]: action_set[0][13] if p < 0.5 else action_set[0][14],
                          action_set[0][8]: action_set[0][15] if p < 0.5 else action_set[0][16],
                          action_set[0][9]: action_set[0][5],
                          action_set[0][10]: action_set[0][5],
                          action_set[0][11]: action_set[0][6],
                          action_set[0][12]: action_set[0][6],
                          action_set[0][13]: action_set[0][7],
                          action_set[0][14]: action_set[0][7],
                          action_set[0][15]: action_set[0][8],
                          action_set[0][16]: action_set[0][8]}
            new_joint_action = [action_dic[joint_action[0]]]

            is_broken = random.random() < CHANCE_OF_EXTRA_ACTION
            is_applicable = current_state.is_applicable(new_joint_action)
            if is_broken and is_applicable:
                # Send the joint action to the server (also print it for help)
                print(f"Ups! Orthogonal push: {joint_action_to_string(joint_action)} turned into {joint_action_to_string(new_joint_action)}", flush=True, file=sys.stderr)
                # print(joint_action_to_string(new_joint_action), flush=True, file=sys.stderr)
                print(joint_action_to_string(new_joint_action), flush=True)
                _ = parse_response(read_line())
                current_state = current_state.result(new_joint_action)
            else:
                print(joint_action_to_string(joint_action), flush=True, file=sys.stderr)
                print(joint_action_to_string(joint_action), flush=True)
                _ = parse_response(read_line())
                current_state = current_state.result(joint_action)
        else:
            # Send the joint action to the server (also print it for help)
            print(joint_action_to_string(joint_action), flush=True, file=sys.stderr)
            print(joint_action_to_string(joint_action), flush=True)
            _ = parse_response(read_line())
            current_state = current_state.result(joint_action)

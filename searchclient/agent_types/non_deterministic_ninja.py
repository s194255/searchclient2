# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 16:14:23 2022

@author: malth
"""
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
from search_algorithms.and_or_graph_search import and_or_graph_search, cyclic_and_or_graph_search
from utils import *


def Ninja_box_results(state, action, action_set):
    Ninja_case = None
    standard_case = state.result(action)
    action = action[0]
    action_set = action_set[0]
    if action in action_set[4:8]:
        if action == action_set[5]:
            # if state.is_applicable([action_set[21]]) and state.is_applicable([action_set[22]]) and state.result([action_set[21]]).is_applicable([action_set[1]]) and state.result([action_set[22]]).is_applicable([action_set[1]]):
            #     if random.random()<0.5:
            #         Ninja_case = [state.result([action_set[21]]),state.result([action_set[1]])]
            #     else:
            #         Ninja_case = [state.result([action_set[22]]),state.result([action_set[1]])]
            if state.is_applicable([action_set[9]]):
                Ninja_case = state.result([action_set[9]])
            elif state.is_applicable([action_set[10]]):
                Ninja_case = state.result([action_set[10]])
        
        elif action == action_set[6]:
            # if state.is_applicable([action_set[23]]) and state.is_applicable([action_set[24]]) and state.result([action_set[23]]).is_applicable([action_set[3]]) and state.result([action_set[24]]).is_applicable([action_set[3]]):
            #     if random.random()<0.5:
            #         Ninja_case = [state.result([action_set[23]]),state.result([action_set[3]])]
            #     else:
            #         Ninja_case = [state.result([action_set[24]]),state.result([action_set[3]])]
            if state.is_applicable([action_set[11]]):
                Ninja_case = state.result([action_set[11]])
            elif state.is_applicable([action_set[12]]):
                Ninja_case = state.result([action_set[12]])
        
        elif action == action_set[7]:
            # if state.is_applicable([action_set[25]]) and state.is_applicable([action_set[26]]) and state.result([action_set[25]]).is_applicable([action_set[2]]) and state.result([action_set[26]]).is_applicable([action_set[2]]):
            #     if random.random()<0.5:
            #         Ninja_case = [state.result([action_set[25]]),state.result([action_set[2]])]
            #     else:
            #         Ninja_case = [state.result([action_set[26]]),state.result([action_set[2]])]
            if state.is_applicable([action_set[13]]):
                Ninja_case = state.result([action_set[13]])
            elif state.is_applicable([action_set[14]]):
                Ninja_case = state.result([action_set[14]])
                
        elif action == action_set[8]:
            # if state.is_applicable([action_set[27]]) and state.is_applicable([action_set[28]]) and state.result([action_set[28]]).is_applicable([action_set[4]]) and state.result([action_set[28]]).is_applicable([action_set[4]]):
            #     if random.random()<0.5:
            #         Ninja_case = [state.result([action_set[27]]),state.result([action_set[4]])]
            #     else:
            #         Ninja_case = [state.result([action_set[28]]),state.result([action_set[4]])]
            if state.is_applicable([action_set[15]]):
                Ninja_case = state.result([action_set[15]])
            elif state.is_applicable([action_set[16]]):
                Ninja_case = state.result([action_set[16]])
            
    
    if Ninja_case is not None:
        return [standard_case, Ninja_case]
        # print([standard_case]+Ninja_case,file=sys.stderr)
    else:
        return [standard_case]


CHANCE_OF_NINJA_BOX = 0.5

def Ninja_helper(state, action, action_set):
    Ninja_action = action
    action = action[0]

    action_set = action_set[0]
    if action in action_set[4:8]:
        if action == action_set[5]:
            # if state.is_applicable([action_set[21]]) and state.is_applicable([action_set[22]]) and state.result([action_set[21]]).is_applicable([action_set[1]]) and state.result([action_set[22]]).is_applicable([action_set[1]]):
            #     if random.random()<0.5:
            #         Ninja_action = [[action_set[21]],[action_set[1]]]
            #     else:
            #         Ninja_action = [action_set[22],action_set[1]]
            if state.is_applicable([action_set[9]]):
                Ninja_action = [action_set[9]]
            elif state.is_applicable([action_set[10]]):
                Ninja_action = [action_set[10]]
        
        elif action == action_set[6]:
            # if state.is_applicable([action_set[23]]) and state.is_applicable([action_set[24]]) and state.result([action_set[23]]).is_applicable([action_set[3]]) and state.result([action_set[24]]).is_applicable([action_set[3]]):
            #     if random.random()<0.5:
            #         Ninja_action = [action_set[23],action_set[3]]
            #     else:
            #         Ninja_action = [action_set[24],action_set[3]]
            if state.is_applicable([action_set[11]]):
                Ninja_action = [action_set[11]]
            elif state.is_applicable([action_set[12]]):
                Ninja_action = [action_set[12]]
        
        elif action == action_set[7]:
            # if state.is_applicable([action_set[25]]) and state.is_applicable([action_set[26]]) and state.result([action_set[25]]).is_applicable([action_set[2]]) and state.result([action_set[26]]).is_applicable([action_set[2]]):
            #     if random.random()<0.5:
            #         Ninja_action = [action_set[25],action_set[2]]
            #     else:
            #         Ninja_action = [action_set[26],action_set[2]]
            if state.is_applicable([action_set[13]]):
                Ninja_action = [action_set[13]]
            elif state.is_applicable([action_set[14]]):
                Ninja_action = [action_set[14]]
                
        elif action == action_set[8]:
            # if state.is_applicable([action_set[27]]) and state.is_applicable([action_set[28]]) and state.result([action_set[28]]).is_applicable([action_set[4]]) and state.result([action_set[28]]).is_applicable([action_set[4]]):
            #     if random.random()<0.5:
            #         Ninja_action = [action_set[27],action_set[4]]
            #     else:
            #         Ninja_action = [action_set[28],action_set[4]]
            if state.is_applicable([action_set[15]]):
                Ninja_action = [action_set[15]]
            elif state.is_applicable([action_set[16]]):
                Ninja_action = [action_set[16]]
    return Ninja_action
        #crash and burns
    
def non_deterministic_agent_type_ninja(level, initial_state, action_library, goal_description):
    # Create an action set for a single agent.
    action_set = [action_library[0:5]+action_library[17:]]
    print(action_set,file=sys.stderr)
    # Call AND-OR-GRAPH-SEARCH to compute a conditional plan
    worst_case_length, plan = cyclic_and_or_graph_search(initial_state, action_set, goal_description, Ninja_box_results)

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
        # print(joint_action,file=sys.stderr)
        #check if non-determinism happens
        is_ninja = random.random() < CHANCE_OF_NINJA_BOX
        #check if applicable
        is_applicable = current_state.is_applicable(joint_action)
        ninja_applicable = current_state.is_applicable(Ninja_helper(current_state,joint_action,action_set))
        #If non-determinism happens
        if is_ninja and is_applicable and ninja_applicable:
            if joint_action_to_string(joint_action)[:4] == 'Push' and joint_action_to_string(joint_action)[5]==joint_action_to_string(joint_action)[7]:
                joint_action= Ninja_helper(current_state,joint_action,action_set)
                if current_state.result(joint_action).is_applicable and joint_action is not None:
                    print(f"Ninja box! It dodged with {joint_action_to_string(joint_action)}", flush=True, file=sys.stderr)
                    print(joint_action_to_string(joint_action), flush=True)
                    _ = parse_response(read_line())
                    print(current_state,file=sys.stderr)
                    current_state = current_state.result(joint_action)
                
                # print(joint_action_to_string(joint_action_1), flush=True)
                # _ = parse_response(read_line())
                # current_state = current_state.result(joint_action_1)
                
        # Send the joint action to the server (also print it for help)
        else:
            print(joint_action_to_string(joint_action), flush=True, file=sys.stderr)
            print(joint_action_to_string(joint_action), flush=True)
            _ = parse_response(read_line())
            current_state = current_state.result(joint_action)

            

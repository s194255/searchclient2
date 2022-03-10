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
sys.path.append("..")
from search_algorithms.graph_search import graph_search
from utils import *



def decentralised_agent_type(level, initial_state, action_library, goal_description, frontier):
    # Create an action set where all agents can perform all actions
    action_set = [action_library] * level.num_agents

    # Here you should implement the DECENTRALISED-AGENTS algorithm.
    # You can use the 'classic' agent type as a starting point for how to communicate with the server, i.e.
    # use 'print(joint_action_to_string(joint_action), flush=True)' to send a joint_action to the server and
    # use 'parse_response(read_line())' to read back an array of booleans indicating whether each individual action
    #   in the joint action succeeded.
    num_agents = level.num_agents
    pi = {}
    # joint_action = []

    for i in range(num_agents):
        pos, char = initial_state.agent_positions[i]
        agent_color = level.colors[char]
        monochrome_problem = initial_state.color_filter(agent_color)
        monochrome_goal_description = goal_description.color_filter(agent_color)

        planning_success, plan = graph_search(monochrome_problem, action_set, monochrome_goal_description, frontier)
        pi[i] = plan
        if planning_success == False:
            print("hov", file=sys.stderr)

    print(pi, file=sys.stderr)

    while sum([len(plan) for plan in pi.values()]) != 0:
        joint_action = []
        for i in range(num_agents):
            if len(pi[i]) == 0:
                joint_action.append(action_set[0][0])
            else:
                joint_action.append(pi[i][0][0])

        print(joint_action_to_string(joint_action), flush=True)
        execution_successes = parse_response(read_line())

        for i in range(num_agents):
            if execution_successes[i] and len(pi[i]) != 0:
                pi[i] = pi[i][1:]


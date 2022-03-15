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

from domains.hospital import HospitalGoalDescription
from search_algorithms.graph_search import graph_search
from utils import *





def helper_agent_type(level, initial_state, action_library, goal_description, frontier):

    # Here you should implement the HELPER-AGENT algorithm.
    # Some tips are:
    # - From goal_description, you should look into color_filter and get_sub_goal to create monochrome and subgoal problems.
    # - You should handle communication with the server yourself and check successes of joint actions.
    #   Look into classic.py to see how this is done.
    # - You can create an action set where only a specific agent is allowed to move as follows:
    #   action_set = [[GenericNoOp()]] * level.num_agents
    #   action_set[agent_index] = action_library
    # - You probably want to create a helper function for creating the set of negative obstacle subgoals.
    #   You can then create a new goal description using 'goal_description.create_new_goal_description_of_same_type'
    #   which takes a list of subgoals.

    # agent 0 is the first in list, hopefully always
    actor_index = 0

    action_set = [[GenericNoOp()]] * level.num_agents
    action_set[actor_index] = action_library


    num_helpers = level.num_agents-1
    actor_color = level.colors["0"]
    monochrome_problem = initial_state.color_filter(actor_color)
    monochrome_goal_description = goal_description.color_filter(actor_color)
    pi = {}

    current_state = initial_state
    for i, subgoal in enumerate(monochrome_goal_description):
        planning_success, plan = graph_search(monochrome_problem, action_set, monochrome_goal_description, frontier)
        pi[i] = plan
        if planning_success == False:
            print("execution faulted", file=sys.stderr)

    for plan in pi:
        for action in plan:
            print(joint_action_to_string([action]), flush=True)
            execution_successes = parse_response(read_line())

            if execution_successes[0] == False:

                next_pos = action.calculate_positions(current_state.agent_positions[actor_index][0])

                obstacle_idx, obstacle_char = current_state.object_at(next_pos)









    # raise NotImplementedError()

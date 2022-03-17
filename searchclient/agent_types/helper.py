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



def helper(plan, goal_description, actor_index, current_state):
    pos_actor, actor_char = current_state.agent_positions[actor_index]
    future_pos = []

    for i in range(len(plan)):
        action = plan[i]
        pos_actor = action[0].calculate_agent_positions(pos_actor)
        future_pos.append(pos_actor)

    new_goals = []
    for i in range(len(future_pos)):
        pos = future_pos[i]
        _, char = current_state.object_at(pos)
        if char == '':
            pass
        else:
            new_goal = (pos, char, False)
            new_goals.append(new_goal)

    return goal_description.create_new_goal_description_of_same_type(new_goals)



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

    for i in range(monochrome_goal_description.num_sub_goals()):
        planning_success, plan = graph_search(monochrome_problem, action_set, monochrome_goal_description.get_sub_goal(i), frontier)
        pi[i] = plan
        if planning_success == False:
            print("execution faulted", file=sys.stderr)

    helper_pi = {}
    for plan in pi.values():
        # print("pi", pi, file=sys.stderr)
        # print("plan", plan, file=sys.stderr)
        for action in plan:
            # print(action_set[0][0], file=sys.stderr)
            # print("action",action, file=sys.stderr)
            

            joint_action = [action_set[0][0]] * level.num_agents
            joint_action[actor_index] = action[0]
            print("se her!", joint_action, file=sys.stderr)

            print(joint_action_to_string(list(joint_action)), flush=True)
            execution_successes = parse_response(read_line())


            print(execution_successes, file=sys.stderr)
            for i, execution_success in enumerate(execution_successes):
                if execution_success and len(plan) != 0:
                        plan = plan[1:]

                if execution_success == False:

                    # if execution sucess for
                    if i == actor_index:
                        print("krussedulle", file=sys.stderr)
                        new_goal_description = helper(plan, goal_description, actor_index, current_state)
                        planning_success, plan = graph_search(current_state, action_set, new_goal_description, frontier)


    # raise NotImplementedError()

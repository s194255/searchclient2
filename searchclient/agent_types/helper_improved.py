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

from domains.hospital import HospitalGoalDescription
from search_algorithms.graph_search import graph_search
from utils import *
import time
import copy


def helper(plan, level, actor_index, current_state, actor_goal_description):
    pos_actor, actor_char = current_state.agent_positions[actor_index]

    # get future positions according to the plan
    future_pos = []
    for i in range(len(plan)):
        action = plan[i][0]
        pos_actor = action.calculate_agent_positions(pos_actor)
        future_pos.append(pos_actor)

    # Get color of the actor
    actor_color = level.colors["0"]

    new_goals = []

    char = current_state.object_at(future_pos[0])
    if char == '':
        pass
    else:
        if level.colors[char] == actor_color:
            char = current_state.object_at(future_pos[1])

        for i in range(len(future_pos)):
            pos = future_pos[i]
            # make path spaces negative goals for specific helper
            new_goal = (pos, char, False)
            # goal_description.goals.append(new_goal)
            new_goals.append(new_goal)

            #make goal spaces negative goals for specific helper
            for (actor_goal_pos, _, _) in actor_goal_description.goals:
                new_goals.append((actor_goal_pos, char, False))

            print(new_goals, file=sys.stderr)

    return HospitalGoalDescription(level, new_goals)


def get_conflicting_helper(current_state, plan, agent_idx, level):
    agent_pos, agent_char = current_state.agent_positions[agent_idx]

    # Get color of the actor
    agent_color = level.colors[agent_char]

    future_pos = []
    for i in range(2):
        action = plan[i][agent_idx]
        pos_actor = action.calculate_agent_positions(pos_actor)
        future_pos.append(pos_actor)

    helper_char = current_state.object_at(future_pos[0])

    if level.colors[helper_char] == agent_color:
        helper_char = current_state.object_at(future_pos[1])

    helper_color = level.colors[helper_char]
    for i in range(level.num_agents):
        _, temp_char = current_state.agent_positions[i]
        if temp_char == helper_char:
            helper_idx = i

    # todo: Kasser er ikke implementeret

    return helper_color, helper_char, helper_idx



def helper_improved_agent_type(level, initial_state, action_library, goal_description, frontier):

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

    #Get color of the actor
    actor_color = level.colors["0"]
    current_state = initial_state


    for index in range(goal_description.num_sub_goals()):
        colors = [actor_color]
        indices = [actor_index]
        action_set = [[GenericNoOp()]] * level.num_agents
        action_set[actor_index] = action_library

        sub_goal = goal_description.get_sub_goal(index)

        #while sub_goal is not solved
        while True:

            #Get the monochrome problem
            monochrome_problem = current_state.color_filters(colors)
            monochrome_goal_description = sub_goal.color_filters(colors)

            planning_success, plan = graph_search(monochrome_problem, action_set, monochrome_goal_description, frontier)

            if planning_success == False:
                print("execution faulted", file=sys.stderr)

            if (planning_success == True) and (len(plan) == 0):
                break



            # while actor succeeds in actions
            time_step = 0
            while True:
                joint_action = plan[time_step]
                # pass the joint_action to the server
                print(joint_action_to_string(joint_action), flush=True)
                execution_successes = parse_response(read_line())

                # applicable actions will be used to update current_state
                applicable_actions = []
                for i in range(level.num_agents):
                    if execution_successes[i] == False:
                        # if action is illegal, just do GenericNoOp()
                        applicable_actions.append(GenericNoOp())

                        if i in indices:
                            color_conflict, char_conflict, idx_conflict = get_conflicting_helper(current_state, plan)
                            colors.append(color_conflict)
                            indices.append(idx_conflict)
                            action_set[idx_conflict] = action_library

                    else:
                        applicable_actions.append(joint_action[i])

                # current_state is updated based on legal moves only
                current_state = current_state.result(applicable_actions)
                print(current_state, file=sys.stderr)

                time_step += 1

                # If actor failed action, then we have to replan
                if execution_successes[actor_index] == False:
                    print("jeg fejlede en handling", file=sys.stderr)
                    break






















            #loop until actor is allowed perform an action
            while True:
                #loop through all agents. Get joint_action (some of those actions might be illegal)
                joint_action = []
                for i in range(level.num_agents):
                    agent_pos, agent_char = current_state.agent_positions[i]

                    #If agent is a helper
                    if agent_char != "0":
                        helper_color = level.colors[agent_char]

                        #only the helper is allowed to move
                        action_set_helper = [[GenericNoOp()]] * level.num_agents
                        action_set_helper[i] = action_library

                        #The helper only has to deal with the goals relevant for her
                        monochrome_goal_description_helper = helper_goal_description.color_filter(helper_color)
                        planning_success, plan = graph_search(current_state, action_set_helper,
                                                              monochrome_goal_description_helper, frontier)

                        #If plan is empty, just do GenericNoOp()
                        if len(plan) == 0:
                            joint_action.append(GenericNoOp())
                        else:
                            #get action in plan corresponding to that helper. All the other agents are doing GenericNoOp()
                            helper_action = plan[0][i]
                            joint_action.append(helper_action)
                    elif agent_char == "0":
                        joint_action.append(actor_action[0])




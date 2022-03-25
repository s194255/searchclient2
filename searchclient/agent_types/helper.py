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
import time
import copy


def helper(plan, goal_description, actor_index, current_state):
    pos_actor, actor_char = current_state.agent_positions[actor_index]

    # get future positions according to the plan
    future_pos = []
    for i in range(len(plan)):
        action = plan[i][0]
        pos_actor = action.calculate_agent_positions(pos_actor)
        future_pos.append(pos_actor)



    new_goals = []
    for i in range(len(future_pos)):
        pos = future_pos[i]
        char = current_state.object_at(pos)
        if char == '':
            pass
        else:
            for j in range(i,len(future_pos)):
                pos = future_pos[j]
                new_goal = (pos, char, False)
                # goal_description.goals.append(new_goal)
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
    # action_set = [action_library] * level.num_agents

    # Get color of the actor
    actor_color = level.colors["0"]

    actor_plans = []
    for index in range(goal_description.num_sub_goals()):
        sub_goal = goal_description.get_sub_goal(index)

        #Get the monochrome problem
        monochrome_problem = initial_state.color_filter(actor_color)
        monochrome_goal_description = sub_goal.color_filter(actor_color)

        current_state = initial_state
        planning_success, actor_plan = graph_search(monochrome_problem, action_set, monochrome_goal_description, frontier)
        if planning_success == False:
            print("execution faulted", file=sys.stderr)
        else:
            actor_plans.append(actor_plan)

    # print(actor_plans, file=sys.stderr)
    for actor_plan in actor_plans:
        for time_step in range(len(actor_plan)):
            joint_actor_action = actor_plan[time_step]

            #loop until actor is allowed perform an action
            while True:

                #loop through all agents. Get joint_action (some of those actions might be illegal)
                print("bøøøøørge", goal_description, file=sys.stderr)
                print("bøøøøørge", current_state, file=sys.stderr)

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
                        monochrome_goal_description_helper = goal_description.color_filter(helper_color)
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
                        joint_action.append(joint_actor_action[0])

                # pass the joint_action to the server
                print(joint_action_to_string(joint_action), flush=True)
                execution_successes = parse_response(read_line())

                # applicable actions will be used to update current_state
                applicable_actions = []
                for i in range(level.num_agents):
                    if execution_successes[i] == False:

                        # if action is illegal, just do GenericNoOp()
                        applicable_actions.append(GenericNoOp())
                        if i == actor_index:
                            #actor requests help from her helpers
                            goal_description = helper(actor_plan[time_step:], goal_description, actor_index, current_state)
                    else:
                        applicable_actions.append(joint_action[i])

                #current_state is updated based on legal moves only
                current_state = current_state.result(applicable_actions)

                #If actor managed to do her action, move on to next time step
                if execution_successes[actor_index] == True:
                    print("jeg lavede en handling", file=sys.stderr)
                    break




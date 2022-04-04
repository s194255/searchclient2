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
from domains.hospital.actions import NoOpAction
from utils import *
import time
import copy

def get_actor_path(plan, level, actor_index, current_state, time_step):
    actor_pos, actor_char = current_state.agent_positions[actor_index]
    actor_color = level.colors[actor_char]

    path = [actor_pos]
    for i in range(time_step, len(plan)):
        action = plan[i][actor_index]
        actor_pos = action.calculate_agent_positions(actor_pos)
        path.append(actor_pos)
    return path



def get_helper_goals(path, level, current_state, agent_goals, helper_char):
    # Get color of the helper
    helper_color = level.colors[helper_char]

    helper_goals = set([])

    box_chars = get_boxes_with_color(current_state, level, helper_color)

    for pos in path:
        helper_goals.add((pos, helper_char, False))
        for box_char in box_chars:
            helper_goals.add((pos, box_char, False))

    for (pos, _, _) in agent_goals["0"]:
        helper_goals.add((pos, helper_char, False))

        for box_char in box_chars:
            helper_goals.add((pos, box_char, False))



    return helper_goals

    #apply the negative goals to the agent herself

def get_boxes_with_color(current_state, level, color):
    box_chars = []
    for (box_pos, box_char) in current_state.box_positions:
        box_color = level.colors[box_char]
        if box_color == color:
            box_chars.append(box_char)
    return box_chars


def get_conflicting_helper(current_state, plan, agent_idx, level, time_step):
    agent_pos, agent_char = current_state.agent_positions[agent_idx]

    # Get color of the actor
    agent_color = level.colors[agent_char]

    action = plan[time_step][agent_idx]
    next_pos = action.calculate_agent_positions(agent_pos)
    temp_char = current_state.object_at(next_pos)


    if '0' <= temp_char <= '9':
        helper_idx, helper_char = current_state.agent_at(next_pos)
        helper_color = level.colors[helper_char]
        return helper_color, helper_char, helper_idx

    elif 'A' <= temp_char <= 'Z':
        box_idx, box_char = current_state.box_at(next_pos)
        box_color = level.colors[box_char]

        if box_color == agent_color:
            next_box_pos = action.calculate_box_positions(next_pos)



            temp_char = current_state.object_at(next_box_pos)
            if '0' <= temp_char <= '9':
                helper_idx, helper_char = current_state.agent_at(next_box_pos)
                helper_color = level.colors[helper_char]
                return helper_color, helper_char, helper_idx

            elif 'A' <= temp_char <= 'Z':
                box_idx, box_char = current_state.box_at(next_box_pos)
                box_color = level.colors[box_char]


        for i in range(level.num_agents):
            _, helper_char = current_state.agent_positions[i]
            helper_color = level.colors[helper_char]
            if helper_color == box_color:
                helper_idx = i
                break
        return helper_color, helper_char, helper_idx

    else:
        return False, False, False



def get_joint_action(plan, time_step, controllable_agents, level, current_state):

    joint_action = []
    for agent_idx in range(level.num_agents):
        agent_pos, agent_char = current_state.agent_positions[agent_idx]
        if agent_char in controllable_agents:
            joint_action.append(plan[time_step][agent_idx])
        else:
            joint_action.append(GenericNoOp())

    return joint_action

def convert_plan(plan, current_state, monochrome_state):
    #fra mono til current
    idx_dict = {}
    n_m = len(monochrome_state.agent_positions)
    n_c = len(current_state.agent_positions)

    for i in range(n_m):
        _, char = monochrome_state.agent_positions[i]
        for j in range(n_c):
            _, char_temp = current_state.agent_positions[j]
            if char == char_temp:
                idx_dict[i] = j

    korrigeret_plan = []
    for tidsskridt in plan:

        joint_action = [GenericNoOp()] * n_c
        for mono_idx in idx_dict.keys():
            handling = tidsskridt[mono_idx]

            curr_idx = idx_dict[mono_idx]
            joint_action[curr_idx] = handling
        korrigeret_plan.append(joint_action)
    return korrigeret_plan


    # for i in range(current_state.agent_positions):
    #     pos, char = current_state.agent_positions[i]
    #
    #     for j in range(monochrome_state.agent_positions):
    #         pos_temp, char_temp = current_state.agent_positions[i]

def make_naive_plan(current_state, agent_goals, controllable_agents, level, frontier, action_library):
    agent_plans = []
    planning_successes = []
    longest_plan = 0
    for i in range(level.num_agents):
        agent_pos, agent_char = current_state.agent_positions[i]
        actor_color = level.colors[agent_char]
        mono_state = current_state.color_filter(actor_color)
        mono_goaldes = HospitalGoalDescription(level, agent_goals[agent_char])
        action_set = [[GenericNoOp()]] * level.num_agents
        action_set[i] = action_library


        planning_success, agent_plan = graph_search(mono_state, action_set, mono_goaldes, frontier)
        agent_plans.append(agent_plan)
        planning_successes.append(planning_success)
        if len(agent_plan) > longest_plan:
            longest_plan = len(agent_plan)

    plan = []
    for time_step in range(longest_plan):
        joint_action = []
        for i in range(level.num_agents):
            agent_plan = agent_plans[i]
            if time_step < len(agent_plan):
                joint_action.append( agent_plan[time_step][i])
            else:
                joint_action.append(GenericNoOp())
        plan.append(joint_action)
    return planning_successes[0], plan


def make_plan(current_state, agent_goals, controllable_agents, level, frontier, action_library):
    colors = []
    ggoals = []
    for agent_char in controllable_agents:
        colors.append(level.colors[agent_char])

        # slettemette
        if agent_char != "0":
            ggoals.extend(agent_goals[agent_char])


        # huskemette
        # ggoals.extend(agent_goals[agent_char])

    mono_state = current_state.color_filters(colors)
    mono_goaldes = HospitalGoalDescription(level, ggoals)

    action_set = [action_library] * len(mono_state.agent_positions)


    planning_success, plan = graph_search(mono_state, action_set, mono_goaldes, frontier)
    if planning_success == False:
        pass
    plan = convert_plan(plan, current_state, mono_state)

    return planning_success, plan

def prune_controllable_agents(controllable_agents, actor_path, current_state, agent_goals, level):

    for (agent_pos, agent_char) in current_state.agent_positions:
        if agent_char in controllable_agents:
            path_check = (agent_pos not in actor_path)

            box_check = True
            helper_color = level.colors[agent_char]

            for (box_pos, box_char) in current_state.box_positions:
                box_color = level.colors[box_char]
                if box_color == helper_color:
                    if box_pos in actor_path:
                        box_check = False
                    for (goal_pos, _, _) in agent_goals["0"]:
                        if goal_pos == box_pos:
                            box_check = False

            goal_check = True
            for (goal_pos, _, _) in agent_goals["0"]:
                if goal_pos == agent_pos:
                    goal_check = False

            if path_check and goal_check and box_check:
                controllable_agents.remove(agent_char)


def helper_improved_agent_type(level, initial_state, action_library, actor_goal_description, frontier):

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


    current_state = initial_state

    actor_goals = set([])


    for sub_goal in actor_goal_description.goals:


        actor_goals.add(sub_goal)
        goal_des = HospitalGoalDescription(level, actor_goals)

        controllable_agents = set(["0"])

        agent_goals = {}
        for agent_pos, agent_char in copy.deepcopy(current_state).agent_positions:
            agent_goals[agent_char] = []
        agent_goals["0"] = actor_goals

        hårdknudefaktor = 0

        while goal_des.is_goal(copy.deepcopy(current_state)) == False:
            if hårdknudefaktor < 1:
                planning_success, plan = make_naive_plan(copy.deepcopy(current_state), agent_goals, controllable_agents,
                                                   level, frontier, action_library)
            else:
                planning_success, plan = make_plan(copy.deepcopy(current_state), agent_goals, controllable_agents,
                                                   level, frontier, action_library)



            # while actor succeeds in actions
            time_step = 0
            while time_step < len(plan):
                joint_action = get_joint_action(plan, time_step,
                                                controllable_agents, level, copy.deepcopy(current_state))



                print(joint_action_to_string(joint_action), flush=True)
                execution_successes = parse_response(read_line())


                # applicable actions will be used to update current_state
                applicable_actions = []
                for agent_idx in range(level.num_agents):
                    agent_pos, agent_char = copy.deepcopy(current_state).agent_positions[agent_idx]

                    if execution_successes[agent_idx] == False:
                        applicable_actions.append(GenericNoOp())

                        if agent_char in controllable_agents:
                            color_conflict, char_conflict, idx_conflict = get_conflicting_helper(copy.deepcopy(current_state), plan,
                                                                                                 agent_idx, level,
                                                                                                 time_step)
                            if color_conflict != False:
                                controllable_agents.add(char_conflict)
                                actor_path = get_actor_path(plan, level, actor_index,
                                                            copy.deepcopy(current_state), time_step)
                                negative_goals = get_helper_goals(actor_path, level,
                                                                  copy.deepcopy(current_state),
                                                                  agent_goals, char_conflict)
                                agent_goals[char_conflict] = negative_goals
                    else:
                        applicable_actions.append(joint_action[agent_idx])

                # current_state is updated based on legal moves only
                current_state = current_state.result(applicable_actions)
                # time.sleep(1)


                time_step += 1

                # If actor failed action, then we have to replan
                if execution_successes[actor_index] == False:
                    hårdknudefaktor += 1
                    prune_controllable_agents(controllable_agents,
                                              actor_path, copy.deepcopy(current_state), agent_goals, level)
                    break
                else:
                    # todo hvad hvis helperen er den sidste der bevæger sig?
                    hårdknudefaktor = 0







































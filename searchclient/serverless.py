import sys
import argparse
import memory
import re
from agent_types.classic import classic_agent_type
from domains.hospital import *
from strategies.bfs import FrontierBFS
from strategies.dfs import FrontierDFS
from domains.hospital.heuristics import BFSHeu
from strategies.bestfirst import FrontierAStar, FrontierGreedy

from search_algorithms.graph_search import graph_search
from agent_types.decentralised import decentralised_agent_type


def load_lvl_lines(path):
    with open(path) as f:
        lines = []
        while True:
            line = f.readline()
            lines.append(line)
            if line.startswith("#end"):
                break
    return lines



def main():
    level_path = "../levels/MAPF00.lvl"

    level_lines = load_lvl_lines(level_path)
    level = HospitalLevel.parse_level_lines(level_lines)
    # heuristic = BFSHeu()
    # frontier = FrontierGreedy(heuristic)
    frontier = FrontierBFS()
    initial_state = HospitalState(level, level.initial_agent_positions, level.initial_box_positions)
    goal_description = HospitalGoalDescription(level, level.box_goals + level.agent_goals)
    action_library = DEFAULT_HOSPITAL_ACTION_LIBRARY

    # Create an action set where all agents can perform all actions
    action_set = [action_library] * level.num_agents

    decentralised_agent_type(level, initial_state, action_library, goal_description, frontier)












    #
    # planning_success, plan = graph_search(initial_state, action_set, goal_description, frontier)
    #
    # if planning_success == True:
    #     print("problem solved")
    #
    #     current_state = initial_state
    #     for joint_action in plan:
    #         print(current_state)
    #         print("action", joint_action)
    #         current_state = current_state.result(joint_action)
    #     print(current_state)
    #
    # else:
    #     print("Failed to solve problem")




if __name__ == "__main__":
    main()
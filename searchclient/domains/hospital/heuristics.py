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
from __future__ import annotations
import sys
import itertools
from utils import pos_add, pos_sub, APPROX_INFINITY

import domains.hospital.state as h_state
import domains.hospital.goal_description as h_goal_description
import domains.hospital.level as h_level
from collections import deque


class HospitalGoalCountHeuristics:

    def __init__(self):
        pass

    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        # Your code goes here...
        c = 0

        # loop through the goal indices
        for index in range(goal_description.num_sub_goals()):
            # define subgoal and get its information
            sub_goal = goal_description.get_sub_goal(index)
            (goal_position, goal_char, is_positive_literal) = sub_goal.goals[0]
            # get the character of the object in sub goal
            char = state.object_at(goal_position)

            # if the subgoal is not satisfied, add 1 to the heuristic.
            if is_positive_literal and goal_char != char:
                c += 1
            elif not is_positive_literal and goal_char == char:
                c += 1

        return c


class HospitalAdvancedHeuristics:

    def __init__(self):
        self.DistanceTable = {}
        self.pairs = {}

    def prepare(self, level: h_level.HospitalLevel, state):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        for i in range(len(level.walls)):
            for j in range(len(level.walls[0])):
                for goal in level.box_goals:
                    x, y = goal[0]
                    self.DistanceTable[(i, j), goal[0]] = abs(x - i) + abs(y - j)

        # loop over the goals
        for goal in level.box_goals:
            a_list = {}
            index = []
            # loop over the box
            for box in level.initial_box_positions:
                # check if box character matches goal character
                if box[1] == goal[1]:
                    # get the box dx
                    idx, _ = state.box_at(box[0])
                    index.append(idx)
                    # if box idx has not been assigned to another goal, get Manhattan distance from distance table
                    if idx not in self.pairs.values():
                        a_list[idx] = self.DistanceTable[box[0], goal[0]]

            # get box index with lowest Manhattan
            min_idx = min(a_list, key=a_list.get)
            # assign goal-box pair
            self.pairs[goal[0]] = min_idx

    def preprocess(self, level: h_level.HospitalLevel):
        pass

    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:

        # Your heuristic goes here...
        if len(self.DistanceTable.keys()) == 0:
            self.prepare(goal_description.level, state)

        c = 0

        # compute heuristic
        for goal in self.pairs.keys():
            idx = self.pairs[goal]
            box_position, _ = state.box_positions[idx]

            c += self.DistanceTable[box_position, goal]

        return c


class BFSHeu:
    # This class was added as experiment. We tried looking at the true distances
    # between blocks and goals - not just the manhattan distance
    # In this class, the distances between tiles and goals are found with
    # a BFS.

    # For simplicity, we use an implementation of BFS from the course Algoritmer og Data-
    # strukturer

    def __init__(self):
        self.DistanceTable = {}
        self.pairs = {}

    def getGraphsAndNotes(self, level):
        # Define a dictionary of nodes and edges
        self.G = {}
        self.nodes = {}
        nrows = len(level.walls)
        ncols = len(level.walls[0])

        for i in range(nrows):
            for j in range(ncols):
                new_nodes = []

                if i != 0:
                    if level.wall_at((i - 1, j)) == False:
                        new_nodes.append((i - 1, j))

                if i != nrows - 1:
                    if level.wall_at((i + 1, j)) == False:
                        new_nodes.append((i + 1, j))

                if j != 0:
                    if level.wall_at((i, j - 1)) == False:
                        new_nodes.append((i, j - 1))

                if j != ncols - 1:
                    if level.wall_at((i, j + 1)) == False:
                        new_nodes.append((i, j + 1))

                self.G[(i, j)] = new_nodes
                self.nodes[(i, j)] = node((i, j), "white", 10 ** 5, None)

    def reset(self):
        for key in self.nodes:
            self.nodes[key].color = "white"
            self.nodes[key].d = 10 ** 5
            self.nodes[key].pi = None

    def BFS(self, level, subgoal):
        # This implementation of BFS comes from the course Algoritmer og Datastrukturer

        s = self.nodes[subgoal[0]]
        s.color = "gray"
        s.d = 0
        s.pi = None

        frontier = deque()
        frontier.append(s)

        reached = set([s])

        while not len(frontier) == 0:
            node = frontier.popleft()
            children_cor = self.G[node.koordinat]
            for child_cor in children_cor:
                child = self.nodes[child_cor]
                if child.color == "white":
                    child.color = "gray"
                    child.d = node.d + 1
                    child.pi = node
                    frontier.append(child)
            node.color = "black"
            self.DistanceTable[node.koordinat, subgoal[0]] = node.d

        self.reset()

    def preprocess(self, level):
        self.getGraphsAndNotes(level)
        for subgoal in level.box_goals:
            self.BFS(level, subgoal)

    def prepare(self, level, state):
        # Assign goals to boxes

        for goal in level.box_goals:  # Get index of box with least distance
            a_list = {}
            index = []
            for box in level.initial_box_positions:
                if box[1] == goal[1]:
                    idx, _ = state.box_at(box[0])
                    index.append(idx)
                    a_list[idx] = self.DistanceTable[box[0], goal[0]]

            min_idx = min(a_list, key=a_list.get)
            if min_idx not in self.pairs.values():
                self.pairs[goal[0]] = min_idx

    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        # If distance table has not been created, create it
        if len(self.DistanceTable.keys()) == 0:
            self.preprocess(goal_description.level)
            self.prepare(goal_description.level, state)

        c = 0

        for goal in self.pairs.keys():
            idx = self.pairs[goal]
            box_position, _ = state.box_positions[idx]

            c += self.DistanceTable[box_position, goal]

        return c


class node:
    # class requiered for the BFS implementation
    def __init__(self, koordinat, color, d, pi):
        self.koordinat = koordinat
        self.color = color
        self.d = d
        self.pi = pi
        self.path = []

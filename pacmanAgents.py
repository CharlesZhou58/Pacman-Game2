# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random
import math

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Hill Climber Algorithm instead of returning Directions.STOP
        initialList = []
        length = 5
        for i in range(0, length):
            initialList.append(Directions.STOP)
        curList = initialList
        possible = state.getAllPossibleActions()
        for i in range(0, len(curList)):
            curList[i] = possible[random.randint(0, len(possible)-1)]
        action = initialList[0]
        maxValue = 0
        while True:
            curState = state
            for i in range(0, len(curList)):
                if curState.isWin() + curState.isLose() == 0:
                    tempState = curState
                    curState = curState.generatePacmanSuccessor(curList[i])
                    if curState == None:
                        tempValue = maxValue
                        maxValue = max(maxValue, gameEvaluation(state, tempState))
                        if maxValue > tempValue:
                            action = curList[0]
                        else:
                            action = initialList[0]
                        return action
                else:
                    break
            tempValue = maxValue
            maxValue = max(maxValue, gameEvaluation(state, curState))
            if maxValue > tempValue:
                action = curList[0]
                initialList = curList[:]
            else:
                action = initialList[0]
            for i in range(0, length):
                test = random.randint(0, 9)
                if (test < 5):
                    curList[i] = possible[random.randint(0, len(possible) - 1)]
                else:
                    curList[i] = initialList[i]


class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        memberList = []
        length = 5
        size = 8
        action = Directions.STOP
        possible = state.getAllPossibleActions()
        for k in range(0, size):
            childList = []
            for i in range(0, length):
                childList.append(possible[random.randint(0, len(possible) - 1)])
            memberList.append(childList)
        while True:
            member = []
            for l in range(0, size):
                curState = state
                for i in range(0, length):
                    if curState.isWin() + curState.isLose() == 0:
                        curState = curState.generatePacmanSuccessor(memberList[l][i])
                        if curState == None:
                            return action
                    else:
                        break
                rank = 0
                value = gameEvaluation(state, curState)
                mv = [memberList[l], value, rank]
                member.append(mv)
            rankList = sorted(member, key = lambda member: member[1])
            for i in range(0, size):
                rankIndex = 1
                sameCount = 1
                for j in range(0, size):
                    if j != i and rankList[j][1] < rankList[i][1]:
                        rankIndex += 1
                    if j != i and rankList[j][1] == rankList[i][1]:
                        sameCount += 1
                rankList[i][2] = rankIndex + (sameCount - 1)/2.0
            parentList = []
            for i in range(0, size):
                ranNumber = random.randint(1, 36)
                z = 0
                for j in range(0, size):
                    ranNumber -= (rankList[j][2])
                    z = j
                    if ranNumber <= 0:
                         break
                parentList.append(rankList[z][0])
            for i in range(0, size/2):
                r = random.randint(1, 10)
                if r > 3:
                    for c in range(0, 2):
                        newChild = []
                        for j in range(0, length):
                            newChild.append(parentList[i * 2 + random.randint(0, 1)][j])
                        parentList[i * 2 + c] = newChild
            for i in range(0, size):
                m = random.randint(0, 9)
                if m < 1:
                    parentList[i][random.randint(0, length-1)] = possible[random.randint(0, len(possible)-1)]
            action = parentList[random.randint(0, size-1)][0]
            memberList = parentList[:]

class Node(object):
    def __init__(self):
        self.action = None
        self.parent = None
        self.children = []
        self.quality = 0
        self.visitedTime = 0

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        node = Node()
        while True:
            expandNode = self.treePolicy(state, node)
            if expandNode == None:
                break
            parentList = []
            childNode = expandNode
            while childNode.parent != None:
                parentList.append(childNode.parent)
                childNode = childNode.parent
            parentList.reverse()
            curState = state
            for i in range(len(parentList)):
                curState = curState.generatePacmanSuccessor(parentList[i].action)
                if curState == None or curState.isWin() + curState.isLose() != 0:
                    break
            if curState == None:
                break
            reward = self.defaultPolicy(curState)
            self.backUp(expandNode, reward)
        maxTime = 0
        for child in node.children:
            maxTime = max(child.visitedTime, maxTime)
        actions = []
        for child in node.children:
            if child.visitedTime == maxTime:
                actions.append(child.action)
        if len(actions) > 1:
            mctsAction = actions[random.randint(0, len(actions)-1)]
        else:
            mctsAction = actions[0]
        return mctsAction

    def isFullyExpanded(self, state, node):
        legalAction = state.getLegalPacmanActions()
        return len(node.children) == len(legalAction)

    def treePolicy(self, state, node):
        curState = state
        while curState.isWin() + curState.isLose() == 0:
            if self.isFullyExpanded(curState, node) == False:
                return self.expand(curState, node)
            else:
                node = self.bestChild(node)
                curState = curState.generatePacmanSuccessor(node.action)
                if curState == None:
                    break
        return node

    def expand(self, state, node):
        legalMove = state.getLegalPacmanActions()
        triedAction = []
        for child in node.children:
            triedAction.append(child.action)
        while True:
            nextAction = legalMove[random.randint(0, len(legalMove)-1)]
            if nextAction in triedAction:
                continue
            else:
                break
        child = Node()
        child.action = nextAction
        child.parent = node
        node.children.append(child)
        return child

    def bestChild(self, node):
        maxScore = - 999999
        maxC = None
        cList = []
        for child in node.children:
            score = (child.quality/child.visitedTime) + math.sqrt(2.0 * math.log(node.visitedTime)/child.visitedTime)
            if score > maxScore:
                cList = []
                cList.append(child)
                maxC = child
                maxScore = score
            if score == maxScore:
                cList.append(child)
        if len(cList) > 1:
            maxC = cList[random.randint(0, len(cList)-1)]
        return maxC

    def defaultPolicy(self, state):
        legalMove = state.getLegalPacmanActions()
        curState = state
        i = 0
        rollout = 5
        while i < rollout:
            if curState.isWin() + curState.isLose() == 0:
                tempState = curState
                curState = curState.generatePacmanSuccessor(legalMove[random.randint(0, len(legalMove)-1)])
                if curState == None:
                    return gameEvaluation(state, tempState)
            else:
                break
            i += 1
        return gameEvaluation(state, curState)


    def backUp(self, node, value):
        while node != None:
            node.visitedTime += 1.0
            node.quality += value
            node = node.parent





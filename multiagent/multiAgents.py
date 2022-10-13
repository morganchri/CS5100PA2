# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ghostPos = successorGameState.getGhostPositions()
        ghostDists = []
        foodDists = []
        for i in range(len(ghostPos)):
            if (util.manhattanDistance(newPos, ghostPos[i]) == 0):
                ghostDists.append(0)
            else:
                ghostDists.append(1/util.manhattanDistance(newPos, ghostPos[i]))
        for j in range(len(newFood.asList())):
            if (util.manhattanDistance(newPos, newFood.asList()[j]) == 0):
                foodDists.append(0)
            else:
                foodDists.append(1/util.manhattanDistance(newPos, newFood.asList()[j]))
        if (len(foodDists) == 0):
            return successorGameState.getScore() - max(ghostDists)
        elif (newScaredTimes[0] != 0):
            return max(foodDists) + successorGameState.getScore()
        else:
            return max(foodDists) + successorGameState.getScore() - max(ghostDists)

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def minimax(self, gameState: GameState, depth, player):
        if (self.TerminalTest(depth, gameState) == True):
            return "", self.evaluationFunction(gameState)
        #maximize pac man
        if (player == 0):
            v = -999999
            maxAction = ""
            actions = gameState.getLegalActions(player)
            for action in actions:
                newPlayer = player + 1
                newDepth = depth
                numAgents = gameState.getNumAgents()
                if (newPlayer == numAgents):
                    newPlayer = 0
                    newDepth = depth + 1
                newV = self.minimax(gameState.generateSuccessor(player, action), newDepth, newPlayer)[1]
                if (max(newV ,v) == newV):
                    v = newV
                    maxAction = action
            return maxAction, v
        #minimize the ghosts
        else:
            v = 999999
            minAction = ""
            actions = gameState.getLegalActions(player)
            for action in actions:
                newPlayer = player + 1
                newDepth = depth
                numAgents = gameState.getNumAgents()
                if (newPlayer == numAgents):
                    newPlayer = 0
                    newDepth = depth + 1
                newV = self.minimax(gameState.generateSuccessor(player, action), newDepth, newPlayer)[1]
                if (min(newV ,v) == newV):
                    minAction = action
                    v = newV
            return minAction, v
    def TerminalTest(self, depth, gameState: GameState):
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return True
        else:
            return False

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, 0)[0]
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def TerminalTest(self, depth, gameState: GameState):
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return True
        else:
            return False

    def alpha_beta(self, gameState: GameState, depth, player, a, b):
        if (self.TerminalTest(depth, gameState) == True):
            return "", self.evaluationFunction(gameState)
        # maximize pac man
        if (player == 0):
            v = -999999
            maxAction = ""
            actions = gameState.getLegalActions(player)
            for action in actions:
                newPlayer = player + 1
                newDepth = depth
                numAgents = gameState.getNumAgents()
                if (newPlayer == numAgents):
                    newPlayer = 0
                    newDepth = depth + 1
                newV = max(v, self.alpha_beta(gameState.generateSuccessor(player, action), newDepth, newPlayer, a, b)[1])
                if (newV > b):
                    v = newV
                    break
                a = max(a, newV)
                if (newV > v):
                    maxAction = action
                    v = newV
            return maxAction, v
        #minimize ghosts
        else:
            v = 999999
            minAction = ""
            actions = gameState.getLegalActions(player)
            for action in actions:
                newPlayer = player + 1
                newDepth = depth
                numAgents = gameState.getNumAgents()
                if (newPlayer == numAgents):
                    newPlayer = 0
                    newDepth = depth + 1
                newV = min(v,self.alpha_beta(gameState.generateSuccessor(player, action), newDepth, newPlayer, a, b)[1])
                if (newV < a):
                    v = newV
                    break
                b = min(b, newV)
                if (newV < v):
                    minAction = action
                    v = newV
            return minAction, v
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alpha_beta(gameState, 0, 0, -999999, 999999)[0]
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectimax(self, gameState: GameState, depth, player):
        if (self.TerminalTest(depth, gameState) == True):
            return "", self.evaluationFunction(gameState)
        # maximize pac man
        if (player == 0):
            v = -999999
            maxAction = ""
            actions = gameState.getLegalActions(player)
            for action in actions:
                newPlayer = player + 1
                newDepth = depth
                numAgents = gameState.getNumAgents()
                if (newPlayer == numAgents):
                    newPlayer = 0
                    newDepth = depth + 1
                newV = self.expectimax(gameState.generateSuccessor(player, action), newDepth, newPlayer)[1]
                if (max(newV ,v) == newV):
                    v = newV
                    maxAction = action
            return maxAction, v
        #chance the ghosts
        else:
            v = 0
            actionToUse = ""
            numAgents = gameState.getNumAgents()
            for action in gameState.getLegalActions(player):
                newPlayer = player + 1
                newDepth = depth
                if (newPlayer == numAgents):
                    newPlayer = 0
                    newDepth = depth + 1
                p = (gameState.getNumAgents() - 1) / (gameState.getNumAgents())
                v += p * self.expectimax(gameState.generateSuccessor(player, action), newDepth, newPlayer)[1]
                actionToUse = action
            return actionToUse, v

    def TerminalTest(self, depth, gameState: GameState):
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return True
        else:
            return False
    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState, 0, 0)[0]
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    I designed this similar to the reflex agent, however I started with the current state, then added in the successor
    state score, then started working with adding the food and ghost positions, once I began getting higher and higher
    averages I started changing other things around, so I removed the successorScore from the primary return, and that
    resulted in higher scores and a 4/6, removing it from the rest of the conditionals increased the scores and the
    autograder to a 5/6. One final tweak, which was adding max(ghostDists) to the if (newScaredTimes[0] != 0)
    conditional resulted in even higher scores and thus a 6/6 in the autograder.  The successorScore and the method
    to generate are still in the code below but commented out to show what I was doing during the process for
    developing this evaluation function.  I account for several scenarios, similar to the reflex agent, where I set the
    distance to food to zero if the distance to the food is in fact zero, as it will not calculate due to the food list
    being empty. Similar for the ghost distances, I subtract the distances to the ghosts from the base function, but
    instead of simply ignoring them this time when they are in the scared state, I add the max distance to pac man.
    """
    "*** YOUR CODE HERE ***"
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    #successorScore = 0
    foodDists = []
    ghosts = currentGameState.getGhostPositions()
    ghostDists = []
    #for action in currentGameState.getLegalActions():
    #    successorScore += currentGameState.generateSuccessor(0, action).getScore()
    for ghost in range(len(ghosts)):
        if (util.manhattanDistance(ghosts[ghost], currentGameState.getPacmanPosition()) == 0):
            ghostDists.append(0)
        else:
            ghostDists.append(1/util.manhattanDistance(ghosts[ghost], currentGameState.getPacmanPosition()))
    for food in currentGameState.getFood().asList():
        if (util.manhattanDistance(food, currentGameState.getPacmanPosition()) == 0):
            foodDists.append(0)
        else:
            foodDists.append(1/util.manhattanDistance(food, currentGameState.getPacmanPosition()))
    if (len(foodDists) == 0):
        return currentGameState.getScore() - max(ghostDists)
    if (newScaredTimes[0] != 0):
        return currentGameState.getScore() + max(foodDists) + max(ghostDists)
    return currentGameState.getScore() + max(foodDists) - max(ghostDists)
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

from copy import copy, deepcopy

ROW_COUNT = 3
COL_COUNT = 3

class GameState(object):

    parent = None
    endGameStatus = False
    def __init__(self, gameMatrix, parent, currentPlayer):
        self.gameMatrix = gameMatrix   #Inicializa
        self.parent = parent
        self.currentPlayer = currentPlayer

def switchPlayer(gameState):
    if gameState.currentPlayer == 'X':
        return 'O'
    else:
        return 'X'

def printGameState(gameState):
    for x in range(ROW_COUNT):
        for y in range(COL_COUNT):
            print(gameState.gameMatrix[x][y], end='')
        print()

def verifyWinCondition(gameState):
    #Vitoria em linha
    for x in range(ROW_COUNT):
        if(gameState.gameMatrix[x][0] == gameState.gameMatrix[x][1] and gameState.gameMatrix[x][1] == gameState.gameMatrix[x][2] and gameState.gameMatrix[x][0] != '-'):
            gameState.endGameStatus = True
    #Vitoria em coluna
    for y in range(ROW_COUNT):
        if (gameState.gameMatrix[0][x] == gameState.gameMatrix[1][x] and gameState.gameMatrix[1][x] == gameState.gameMatrix[2][x] and gameState.gameMatrix[0][x] != '-'):
            gameState.endGameStatus = True
    #Vitoria em diagonal
    if (gameState.gameMatrix[0][0] == gameState.gameMatrix[1][1] and gameState.gameMatrix[1][1] == gameState.gameMatrix[2][2] and gameState.gameMatrix[1][1] != '-'):
        gameState.endGameStatus = True
    if (gameState.gameMatrix[0][2] == gameState.gameMatrix[1][1] and gameState.gameMatrix[1][1] == gameState.gameMatrix[2][0] and gameState.gameMatrix[1][1] != '-'):
        gameState.endGameStatus = True

def generateGameStates(currentGame):
    for x in range(ROW_COUNT):
        for y in range(COL_COUNT):
            if (currentGame.gameMatrix[x][y] == '-'):
                # Cria matriz auxiliar para gerar o próximo estado
                auxMatrix = deepcopy(currentGame.gameMatrix)
                # Marca na matriz auxiliar a posição de "escolha" do jogador atual
                auxMatrix[x][y] = currentGame.currentPlayer
                # Gera próximo estado com a nova matriz da velha, referenciando o estado anterior e alternando para o próximo jogador
                newGameState = GameState(auxMatrix, currentGame, switchPlayer(currentGame))
                # Adiciona novo estado a lista de todos os estados
                allGameStates.append(newGameState)
                # Verifica se o estado gerado será um estado terminal (alguém venceu)
                verifyWinCondition(newGameState)
                # Faz recursão para gerar novos estados de jogo a partir desse novo estado criado, se ele não for terminal
                if newGameState.endGameStatus is False:
                    generateGameStates(newGameState)


matrixStandard = [['-' for x in range(ROW_COUNT)] for y in range(COL_COUNT)] #Cria matriz base do jogo da velha
allGameStates = []              #Lista que armazena TODOS os estados gerados
initialGame = GameState(matrixStandard, None, 'X') #Instancia estado inicial do jogo
allGameStates.append(initialGame)   #Adiciona estado inicial a lista de estados gerados
generateGameStates(initialGame) #Inicia processo de gerar estados subsequentes

#Imprime nos terminais (que alguem venceu, nao implementei pra verificar velha)
for state in allGameStates:
    if state.endGameStatus is True:
        printGameState(state)
        print()


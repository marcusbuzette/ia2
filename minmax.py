from copy import copy, deepcopy

ROW_COUNT = 3
COL_COUNT = 3

class GameState(object):

    children = []
    endGameStatus = False
    winner = '-'
    factor = None
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
            print(gameState.gameMatrix[x][y]+'   ', end="")
        print('\n')

def isItMax(gameState):
	if(gameState.currentPlayer == 'X'):
		return True
	else:
		return False

def setEndGameConditions(gameState, velha):
	gameState.endGameStatus = True
	if velha is False:
		# O player vencedor foi anterior, então alterna-se para o outro em relação ao atual
		gameState.winner = switchPlayer(gameState)
	else: 
		gameState.winner = '#'

def verifyWinCondition(gameState):
    #Vitoria em linha
    for x in range(ROW_COUNT):
        if(gameState.gameMatrix[x][0] == gameState.gameMatrix[x][1] and gameState.gameMatrix[x][1] == gameState.gameMatrix[x][2] and gameState.gameMatrix[x][0] != '-'):
            setEndGameConditions(gameState, False)
    #Vitoria em coluna
    for y in range(COL_COUNT):
        if (gameState.gameMatrix[0][y] == gameState.gameMatrix[1][y] and gameState.gameMatrix[1][y] == gameState.gameMatrix[2][y] and gameState.gameMatrix[0][y] != '-'):
            setEndGameConditions(gameState, False)
    #Vitoria em diagonal
    if (gameState.gameMatrix[0][0] == gameState.gameMatrix[1][1] and gameState.gameMatrix[1][1] == gameState.gameMatrix[2][2] and gameState.gameMatrix[1][1] != '-'):
        setEndGameConditions(gameState, False)
    if (gameState.gameMatrix[0][2] == gameState.gameMatrix[1][1] and gameState.gameMatrix[1][1] == gameState.gameMatrix[2][0] and gameState.gameMatrix[1][1] != '-'):
        setEndGameConditions(gameState, False)

    #Verifica se deu velha, se ainda não houver vencedor	
    if gameState.endGameStatus is False:
	    count = 0
	    for x in range(ROW_COUNT):
	        for y in range (COL_COUNT):
	            if gameState.gameMatrix[x][y] == '-':
	                count += 1;

	    if (count == 0 and gameState.winner == '-'): #tabuleiro completo
	        setEndGameConditions(gameState, True) # Deu velha

def setFactorEndGame(state):

    #Coloca o valor para os Nos finais
    if(state.endGameStatus == True):
        if(state.winner == 'X'):
            state.factor = 1
            #state.parent.child_factor.append(1)
        elif state.winner == '#': 
            state.factor = 0
            #state.parent.child_factor.append(0)
        else:
            state.factor = -1
            #state.parent.child_factor.append(1)

#Tentativa de colocar fator nos pais            
'''
    else: #Se nao for um no final
        if state.currentPlayer == '0': # Se for o MIN
            for x in range(len(state.child_factor)):
                if(state.child_factor[x] == -1 and state.factor == ''):
                    state.factor = -1;
                    break;

            if(state.factor == ''):
                for x in range(len(state.child_factor)):
                    if(state.child_factor[x] == 0 and state.factor == ''):
                        state.factor = 0;
                        break;
            if(state.factor == ''):
                for x in range(len(state.child_factor)):
                    if(state.child_factor[x] == 1 and state.factor == ''):
                        state.factor = 1;
                        break;
        
        else: # se for MAX
            for x in range(len(state.child_factor)):
                if(state.child_factor[x] == 1 and state.factor == ''):
                    state.factor = 1;
                    break;

            if(state.factor == ''):
                for x in range(len(state.child_factor)):
                    if(state.child_factor[x] == 0 and state.factor == ''):
                        state.factor = 0;
                        break;
            if(state.factor == ''):
                for x in range(len(state.child_factor)):
                    if(state.child_factor[x] == -1 and state.factor == ''):
                        state.factor = -1;
                        break;
            
'''

def setParentsFactor(gameState):
	if gameState.parent is not None:	#Com exceção do no inicial
		if gameState.parent.factor is None:	# Primeiro nó filho recebe primeiro fator
			gameState.parent.factor = gameState.factor
		elif isItMax(gameState.parent) is True and gameState.factor > gameState.parent.factor:	#Maximize
			gameState.parent.factor = gameState.factor
		elif isItMax(gameState.parent) is False and gameState.factor < gameState.parent.factor:	#Minimize
			gameState.parent.factor = gameState.factor

def generateGameStates(currentGame):
    for x in range(ROW_COUNT):
        for y in range(COL_COUNT):
            if (currentGame.gameMatrix[x][y] == '-'):
                #Cria matriz auxiliar para gerar o proximo estado
                auxMatrix = deepcopy(currentGame.gameMatrix)
                #Marca na matriz auxiliar a posicao de "escolha" do jogador atual
                auxMatrix[x][y] = currentGame.currentPlayer
                # Gera proximo estado com a nova matriz da velha, referenciando o estado anterior e alternando para o proximo jogador
                newGameState = GameState(auxMatrix, currentGame, switchPlayer(currentGame))
                # Adiciona novo estado a lista de todos os estados
                allGameStates.append(newGameState)
                # Adiciona novo estado a lista de filhos do no pai
                currentGame.children.append(newGameState)
                #Verifica se o estado gerado sera um estado terminal (alguem venceu)
                verifyWinCondition(newGameState)
                #Faz recusrao para gerar novos estados de jogo a partir desse novo estado criado, se ele nao for terminal
                if newGameState.endGameStatus is False:
                    generateGameStates(newGameState)
                else:
                	setFactorEndGame(newGameState)
                setParentsFactor(newGameState)


matrixStandard = [['-' for x in range(ROW_COUNT)] for y in range(COL_COUNT)] #Cria matriz base do jogo da velha
allGameStates = []              #Lista que armazena TODOS os estados gerados
initialGame = GameState(matrixStandard, None, 'X') #Instancia estado inicial do jogo
allGameStates.append(initialGame)   #Adiciona estado inicial a lista de estados gerados
generateGameStates(initialGame) #Inicia processo de gerar estados subsequentes

#for state in allGameStates:
#    setFactor(state)

#Imprime nos terminais (que alguem venceu, nao implementei pra verificar velha)
for state in allGameStates:
    #if state.endGameStatus is True:
    printGameState(state)
    print(state.winner)
    print(state.factor)
    print('---------------------')


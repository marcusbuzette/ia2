from copy import copy, deepcopy
import random

ROW_COUNT = 3
COL_COUNT = 3

class GameState(object):

    endGameStatus = False
    winner = '-'
    factor = None
    def __init__(self, gameMatrix, parent, currentPlayer):
        self.gameMatrix = gameMatrix   #Inicializa
        self.parent = parent
        self.currentPlayer = currentPlayer
        self.children = []

    def addChild(self, newChild):
        self.children.append(newChild)

def switchPlayer(currentPlayer):
    if currentPlayer == 'X':
        return 'O'
    else:
        return 'X'

def printGameState(gameState):
    for x in range(ROW_COUNT):
        for y in range(COL_COUNT):
            print(gameState.gameMatrix[x][y], end="")
        print()

def isItMax(gameState):
	if(gameState.currentPlayer == 'X'):
		return True
	else:
		return False

def setEndGameConditions(gameState, velha):
	gameState.endGameStatus = True
	if velha is False:
		# O player vencedor foi anterior, então alterna-se para o outro em relação ao atual
		gameState.winner = switchPlayer(gameState.currentPlayer)
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
        elif state.winner == '#': 
            state.factor = 0
        else:
            state.factor = -1

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
                newGameState = GameState(auxMatrix, currentGame, switchPlayer(currentGame.currentPlayer))
                # Adiciona novo estado a lista de filhos do no pai
                currentGame.addChild(newGameState)
                #Verifica se o estado gerado sera um estado terminal (alguem venceu)
                verifyWinCondition(newGameState)
                #Faz recusrao para gerar novos estados de jogo a partir desse novo estado criado, se ele nao for terminal
                if newGameState.endGameStatus is False:
                    generateGameStates(newGameState)
                else:
                    setFactorEndGame(newGameState)
                    endGames.append(newGameState)
                setParentsFactor(newGameState)

def getPlayerChoice(currentState):
    chosenRow, chosenCol = map(int, input('Escolha linha e coluna para X (0-2)(0-2): ').split())
    while not (0 <= chosenRow <= 2 and 0 <= chosenCol <= 2 and currentState.gameMatrix[chosenRow][chosenCol] == '-'):
        chosenRow, chosenCol = map(int, input('ERRO. Escolha linha e coluna para X (0-2)(0-2): ').split())
    return chosenRow, chosenCol

def startGame(currentState):
    currentPlayer = 'X' #Quem inicia é o X, o humano
    while currentState.endGameStatus is False:
        countState = 0
        if currentPlayer == 'X':    # Se for vez do humano (MAX)
            print('**** Vez do X: ****')
            printGameState(currentState)
            chosenRow, chosenCol = getPlayerChoice(currentState)    # Recebe onde o usuário quer marcar o X
            for possibleState in currentState.children: # Procura o próximo estado baseado na posição que o usuário decidiu marcar
                if possibleState.gameMatrix[chosenRow][chosenCol] == 'X':
                    currentState = possibleState
                    break
        else:
            print('**** Vez do O (BOT): ****')    # Se for vez do BOT (MIN)
            printGameState(currentState)
            lowestFactor = None
            lowestChildren = []
            print('**** Opções e respectivos fatores: ****') # Verifica melhores opções de MIN para o BOT
            for possibleState in currentState.children:
                print('** Opção %s **' % countState)
                printGameState(possibleState)
                print("Fator MINIMAX: "+str(possibleState.factor))
                print()
                countState += 1
                if lowestFactor is None:    # Primeiro estado é o parametro inicial de MIN
                    lowestFactor = possibleState.factor
                    lowestChildren.append(possibleState)
                elif possibleState.factor < lowestFactor:   # Se encontrar um estado com MIN melhor, limpa lista de possiveis escolhas e atualiza o fator de MIN
                    lowestFactor = possibleState.factor
                    lowestChildren.clear()
                    lowestChildren.append(possibleState)
                elif possibleState.factor == lowestFactor:  # Se encontrar um estado com MIN igual, adiciona ele a lista de opções
                    lowestChildren.append(possibleState)

            currentState = random.choice(lowestChildren)    # Escolha um estado aleatório dentro da lista de MIN estados
        currentPlayer = switchPlayer(currentPlayer)

    print('\n**** FIM DE JOGO ****\n')
    if(currentState.winner != '#'):
        print('O jogador ' + currentState.winner + ' venceu!')
    else:
        print('Velha!')

    printGameState(currentState)

endGames = []
matrixStandard = [['-' for x in range(ROW_COUNT)] for y in range(COL_COUNT)] #Cria matriz base do jogo da velha
initialGame = GameState(matrixStandard, None, 'X') #Instancia estado inicial do jogo
print('Gerando todos os estados possíveis e aplicando MINIMAX')
generateGameStates(initialGame) #Inicia processo de gerar estados subsequentes
print('Iniciando jogo')
startGame(initialGame)
while str(input('\nReiniciar jogo (S para continuar)? ')) == 'S':
    startGame(initialGame)

'''
# Verifica probabilidade de vitória para cada jogador e velha
countWinX = 0
countWinO = 0
countVelha = 0
for game in endGames:
    if game.winner == 'X':
        countWinX+=1
    elif game.winner == 'O':
        countWinO+=1
    else:
        countVelha+=1
print('Probabilidade de vitória do X: %s' % (countWinX/(countWinX+countWinO+countVelha)))
print('Probabilidade de vitória do O: %s' % (countWinO/(countWinX+countWinO+countVelha)))
print('Probabilidade de velha: %s' % (countVelha/(countWinX+countWinO+countVelha)))
'''

'''#Imprime nos
for state in initialGame.children:
    printGameState(state)
    print(state.winner)
    print(state.factor)
    print('---------------------')'''




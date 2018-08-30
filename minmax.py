ESCOLHAS = [1,2,3,4,5,6,7,8,9];

J1 = [];
J2 = [];



def marcar(numero):
	index = 0;
	for opcao in ESCOLHAS:
		if opcao == numero:
			del ESCOLHAS [index]
			print(ESCOLHAS);
			return opcao;
			
		else:
			index += 1;


def verificar_15(escolhas_jogador):
	index = 0;
	j = index + 1;
	for escolha in escolhas_jogador:
		for i in range(j,len(escolhas_jogador)):
			if()


J1.append(marcar(7));
J1.append(marcar(3));
J1.append(marcar(2));
J1.append(marcar(1));

verificar_15(J1)
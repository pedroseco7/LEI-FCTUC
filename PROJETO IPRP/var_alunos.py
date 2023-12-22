import foosball_alunos


def le_replay(nome_ficheiro):
    '''
    Função que recebe o nome de um ficheiro contendo um replay, e que deverá
    retornar um dicionário com as seguintes chaves:
    bola - lista contendo tuplos com as coordenadas xx e yy da bola
    jogador_vermelho - lista contendo tuplos com as coordenadas xx e yy da do jogador\_vermelho
    jogador_azul - lista contendo tuplos com as coordenadas xx e yy da do jogador\_azul
    '''
    replay = {
        "bola": [],
        "jogador_vermelho": [],
        "jogador_azul": []
    }

    numero_da_linha = 0

    with open(nome_ficheiro, "r") as ficheiro:

        for linha in ficheiro:

            numero_da_linha += 1 #sao strings

            coordenadas = linha.strip().split(";") #lista com strings
            print(coordenadas)

            for i in range(len(coordenadas)):
                cria_tuplos_com_valores_string = tuple(coordenadas[i].split(",")) # TIRA AS VIRGULAS DAS LISTAS E TRANSFORMA EM UM TUPLO - MAS O NUMERO LA DENTRO CONTINUA STRING
                cria_tuplos_com_valores_float = tuple((float(cria_tuplos_com_valores_string[0]),float(cria_tuplos_com_valores_string[1]))) # É UM TUPLO COM OS VALOR EM FLOAT

                if numero_da_linha == 1:
                    replay["bola"].append(cria_tuplos_com_valores_float)
                if numero_da_linha == 2:
                    replay["jogador_vermelho"].append(cria_tuplos_com_valores_float)
                if numero_da_linha == 3:
                    replay["jogador_azul"].append(cria_tuplos_com_valores_float)

    return replay

def main():
    estado_jogo = foosball_alunos.init_state()
    foosball_alunos.setup(estado_jogo, False)
    replay = le_replay('replay_golo_jv_0_ja_1.txt')
    for i in range(len(replay['bola'])):
        estado_jogo['janela'].update()
        estado_jogo['jogador_vermelho'].setpos(replay['jogador_vermelho'][i])
        estado_jogo['jogador_azul'].setpos(replay['jogador_azul'][i])
        estado_jogo['bola']['objeto'].setpos(replay['bola'][i])

    estado_jogo['janela'].exitonclick()


if __name__ == '__main__':
    main()
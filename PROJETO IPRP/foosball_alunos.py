import turtle as t
import functools
import random
import pygame #É NECESSÁRIO INSTALAR O PYGAME!!
import time

LARGURA_JANELA = 1024
ALTURA_JANELA = 600
DEFAULT_TURTLE_SIZE = 40
DEFAULT_TURTLE_SCALE = 3
RAIO_JOGADOR = DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
RAIO_BOLA = DEFAULT_TURTLE_SIZE / 2
PIXEIS_MOVIMENTO = 90
LADO_MAIOR_AREA = ALTURA_JANELA / 3
LADO_MENOR_AREA = 50
RAIO_MEIO_CAMPO = LADO_MAIOR_AREA / 4
START_POS_BALIZAS = ALTURA_JANELA / 4
BOLA_START_POS = (0, 0)  # Alterado para (0,0)


# Função utilizada para movimentar as turtles responsáveis por desenhar as linhas de campo

def vai_para(xcor, ycor, objeto):
    objeto.pu()
    objeto.goto(xcor, ycor)
    objeto.pd()


pygame.init()
pygame.mixer.init()

# Carregar os arquivos de áudio
som_de_fundo = pygame.mixer.Sound('grito da torcida, som áudio ambiente do estádio de futebol. . (1).mp3')
som_bater_parede = pygame.mixer.Sound('soccer-ball-kick-sound-effects_nFivUDEf.mp3')
som_rede_golos = pygame.mixer.Sound('soccer-ball-in-net-sound-effect_QxoDcbMt.mp3')
som_chutar_bola = pygame.mixer.Sound('football-kick-sound-effect_173mOqy7.mp3')
pop_up = pygame.mixer.Sound('pop-bubble-sound-effect-2022_eotG9kha.mp3')
contagem_decrescente = pygame.mixer.Sound('race-countdown-sound-effect_8FlEqtvU.mp3')
apito = pygame.mixer.Sound('Whistle Sound Effect.mp3')
background_channel = som_de_fundo.play(loops=-1)
    
def cronometragem_inicial():
    cronometragem = t.Turtle()
    pop_up.play()
    cronometragem.goto(0,0)
    cronometragem.write("LIGA", align="center", font=('Monaco', 100, "bold"))
    cronometragem.goto(0,-110)
    cronometragem.write("DOS ÚLTIMOS", align="center", font=('Monaco', 100, "bold"))
    time.sleep(2)
    cronometragem.clear()

    for i in range(1,4):
        
        cronometragem.goto(0,-130)
        cronometragem.write(4-i, align="center", font=('Monaco', 200, "bold"))
        contagem_decrescente.play()
        time.sleep(1)
        cronometragem.clear()

    cronometragem.goto(0,-130)
    cronometragem.write("GO!", align="center", font=('Monaco', 200, "bold"))
    apito.play()
    time.sleep(0.5)
    cronometragem.clear()
    cronometragem.hideturtle()

def cronometragem_depois_golo():

    cronometragem = t.Turtle()
    pop_up.play()

    for i in range(1,4):
        
        cronometragem.goto(0,-130)
        cronometragem.write(4-i, align="center", font=('Monaco', 200, "bold"))
        contagem_decrescente.play()
        time.sleep(1)
        cronometragem.clear()

    cronometragem.goto(0,-130)
    cronometragem.write("GO!", align="center", font=('Monaco', 200, "bold"))
    apito.play()
    time.sleep(0.5)
    cronometragem.clear()
    cronometragem.hideturtle()

def cronometragem_VAR():

    cronometragem = t.Turtle()
    pop_up.play()


    cronometragem.goto(-20,-130)
    cronometragem.write("VAR", align="center", font=('Monaco', 250, "bold"))
    cronometragem.goto(-20,-150)
    cronometragem.write("Oh jovem, está fora de jogo?", align="center", font=('Monaco', 30, "bold"))
    apito.play()
    time.sleep(3)
    cronometragem.clear()
    cronometragem.hideturtle()
# Funções responsáveis pelo movimento dos jogadores no ambiente.
# O número de unidades que o jogador se pode movimentar é definida pela constante
# PIXEIS_MOVIMENTO. As funções recebem um dicionário que contém o estado
# do jogo e o jogador que se está a movimentar.


def jogador_cima(estado_jogo, jogador):
    if (estado_jogo[jogador].ycor()  < ALTURA_JANELA/2 -(PIXEIS_MOVIMENTO)):
        estado_jogo[jogador].seth(90) #acede À turtle do jogador
        estado_jogo[jogador].forward(PIXEIS_MOVIMENTO)


def jogador_baixo(estado_jogo, jogador):
    if (estado_jogo[jogador].ycor() - PIXEIS_MOVIMENTO > -ALTURA_JANELA/2  ):
        estado_jogo[jogador].seth(-90)
        estado_jogo[jogador].forward(PIXEIS_MOVIMENTO)


def jogador_direita(estado_jogo, jogador):
    if (estado_jogo[jogador].xcor()  < LARGURA_JANELA/2 - PIXEIS_MOVIMENTO/2  ):
        estado_jogo[jogador].seth(0)
        estado_jogo[jogador].forward(PIXEIS_MOVIMENTO)

def jogador_esquerda(estado_jogo, jogador):
    if (estado_jogo[jogador].xcor() > -LARGURA_JANELA/2 + PIXEIS_MOVIMENTO/2):
        estado_jogo[jogador].seth(180)
        estado_jogo[jogador].forward(PIXEIS_MOVIMENTO)

def desenha_linhas_campo():
    linhas = t.Turtle()
    linhas.width(5)
    linhas.color("white")

    # Desenha a linha central do meio campo

    vai_para(0, ALTURA_JANELA / 2, linhas)

    linhas.rt(90)
    linhas.fd(ALTURA_JANELA)

    # Desenha o círculo central do meio campo

    vai_para(-RAIO_MEIO_CAMPO, 0, linhas)
    linhas.circle(RAIO_MEIO_CAMPO)

    # Faz a baliza vermelha

    vai_para(-LARGURA_JANELA / 2, RAIO_MEIO_CAMPO * 2, linhas)
    for i in range(2):
        linhas.fd(LADO_MAIOR_AREA)
        linhas.lt(90)
        linhas.fd(LADO_MENOR_AREA)
        linhas.lt(90)

    # Faz a baliza azul

    vai_para(LARGURA_JANELA / 2, RAIO_MEIO_CAMPO * 2, linhas)
    for i in range(2):
        linhas.fd(LADO_MAIOR_AREA)
        linhas.rt(90)
        linhas.fd(LADO_MENOR_AREA)
        linhas.rt(90)

    linhas.hideturtle()


def criar_bola():

    '''
    Função responsável pela criação da bola.
    Deverá considerar que esta tem uma forma redonda, é de cor preta,
    começa na posição BOLA_START_POS com uma direção aleatória.
    Deverá ter em conta que a velocidade da bola deverá ser superior à dos jogadores.
    A função deverá devolver um dicionário contendo 4 elementos: o objeto bola,
    a sua direção no eixo dos xx, a sua direção no eixo dos yy,
    e um elemento inicialmente a None que corresponde à posição anterior da mesma.
    '''

    direcao_x = random.uniform(-1, 1) #vai fazer um float entre o -1 e 1
    direcao_y = random.uniform(-1, 1)

    bola = t.Turtle()
    bola.up()
    bola.shape("circle")
    bola.color("black")

    return {
        'objeto': bola,
        'direcao_x': direcao_x,
        'direcao_y': direcao_y,
        'posicao_anterior': None  # Inicializa com None
    }


def cria_jogador(x_pos_inicial, y_pos_inicial, cor):

    ''' Função responsável por criar e devolver o objeto que corresponde a um jogador (um objecto Turtle).
    A função recebe 3 argumentos que correspondem às coordenadas da posição inicial
    em xx e yy, e a cor do jogador. A forma dos jogadores deverá ser um círculo,
    cujo seu tamanho deverá ser definido através da função shapesize
    do módulo \texttt{turtle}, usando os seguintes parâmetros:
    stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE. '''

    jogador = t.Turtle()

    jogador.up()
    jogador.shape("circle")
    jogador.shapesize(DEFAULT_TURTLE_SCALE, DEFAULT_TURTLE_SCALE)
    jogador.color(cor)
    jogador.goto(x_pos_inicial, y_pos_inicial)

    return jogador


def init_state():

    estado_jogo = {}
    estado_jogo['bola'] = None
    estado_jogo['jogador_vermelho'] = None
    estado_jogo['jogador_azul'] = None
    estado_jogo['var'] = {
        'bola': [],
        'jogador_vermelho': [],
        'jogador_azul': [],
    }
    estado_jogo['pontuacao_jogador_vermelho'] = 0
    estado_jogo['pontuacao_jogador_azul'] = 0

    return estado_jogo


def cria_janela():

    # create a window and declare a variable called window and call the screen()
    window = t.Screen()
    window.title("Foosball Game")
    window.bgcolor("green")
    window.setup(width=LARGURA_JANELA, height=ALTURA_JANELA)
    window.tracer(0)

    return window


def cria_quadro_resultados():
    # Code for creating pen for scorecard update

    quadro = t.Turtle()
    quadro.speed(0)
    quadro.color("Blue")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(0, 260)
    quadro.write("Player A: 0\t\tPlayer B: 0 ", align="center", font=('Monaco', 24, "normal"))

    return quadro


def terminar_jogo(estado_jogo):

    '''
     Função responsável por terminar o jogo. Nesta função, deverá atualizar o ficheiro
     ''historico_resultados.csv'' com o número total de jogos até ao momento,
     e o resultado final do jogo. Caso o ficheiro não exista,
     ele deverá ser criado com o seguinte cabeçalho:
     NJogo,JogadorVermelho,JogadorAzul.
    '''

    print("Adeus")
    estado_jogo['janela'].bye()


    with open('historico_resultados.csv', 'a+') as arquivo:
    # O modo "a+" abre o ficheiro para leitura e escrita, adiciona conteúdo no final do ficheiro caso este exista

        arquivo.seek(0)
        linhas = arquivo.readlines()
        #print linhas = se ainda nao existir devolve uma lista vazia

        if not linhas:
            # Verifica se o arquivo está vazio. Se sim isso significa que não há nenhuma linha

            arquivo.write("Njogos, JogadorVermelho, JogadorAzul\n")
            total_jogos = 0 

        else: # Se o arquivo não estiver vazio:
            # O código conta o número de linhas no arquivo menos 1 pois a primeira linha é a de cabeçalho

            total_jogos = len(linhas) -1

        linha = f"{total_jogos+1}, {estado_jogo['pontuacao_jogador_vermelho']}, {estado_jogo['pontuacao_jogador_azul']}"
        arquivo.write(linha)
        arquivo.write('\n')

def setup(estado_jogo, jogar):
    janela = cria_janela()
    if jogar == True: #Ou seja, se for para jogar, a cronometragem é a normal
        cronometragem_inicial()
    elif jogar == False:#Se for, o VAR, vai ser a cronometragem do VAR
        cronometragem_VAR()

    # Assign keys to play
    janela.listen()
    if jogar:
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_vermelho'), 'w')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_vermelho'), 's')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_vermelho'), 'a')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_vermelho'), 'd')
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_azul'), 'Up')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_azul'), 'Down')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_azul'), 'Left')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_azul'), 'Right')
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo), 'Escape')
        quadro = cria_quadro_resultados()
        estado_jogo['quadro'] = quadro
    desenha_linhas_campo()
    bola = criar_bola()
    jogador_vermelho = cria_jogador(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "red")
    jogador_azul = cria_jogador(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "blue")
    estado_jogo['janela'] = janela
    estado_jogo['bola'] = bola
    estado_jogo['jogador_vermelho'] = jogador_vermelho
    estado_jogo['jogador_azul'] = jogador_azul
    



def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write("Player A: {}\t\tPlayer B: {} ".format(estado_jogo['pontuacao_jogador_vermelho'],
                                                                       estado_jogo['pontuacao_jogador_azul']),
                                                                align="center", font=('Monaco', 24, "normal"))


def movimenta_bola(estado_jogo):

    '''
    Função responsável pelo movimento da bola que deverá ser feito tendo em conta a
    posição atual da bola e a direção em xx e yy.
    '''

    bola = estado_jogo['bola']

    # Guarda a posição anterior da bola

    bola['posicao_anterior'] = bola['objeto'].pos()

    # Atualiza a posição da bola com base nas direções x e y

    nova_posicao_x = bola['objeto'].xcor() + bola['direcao_x'] * 1 #ajustar velocidade da bola
    nova_posicao_y = bola['objeto'].ycor() + bola['direcao_y'] * 1 #ajustar velocidade da bola

    # Define a nova posição da bola

    
    bola['objeto'].goto(nova_posicao_x, nova_posicao_y)
    


def verifica_colisoes_ambiente(estado_jogo):
    '''
    Função responsável por verificar se há colisões com os limites do ambiente,
    atualizando a direção da bola. Não se esqueça de considerar que nas laterais,
    fora da zona das balizas, a bola deverá inverter a direção onde atingiu o limite.
    '''
    bola = estado_jogo['bola']

    # Limites do ambiente
    limite_superior = ALTURA_JANELA / 2
    limite_inferior = -ALTURA_JANELA / 2
    limite_direito = LARGURA_JANELA / 2
    limite_esquerdo = -LARGURA_JANELA / 2

    # Posição atual da bola
    posicao_x = bola['objeto'].xcor()
    posicao_y = bola['objeto'].ycor()

    # Verificação de colisões no limite superior ou inferior

    if (posicao_y >= limite_superior - 1) or (posicao_y <= limite_inferior + 1):

        bola['direcao_y'] *= -1  # Inverte a direção no eixo yy
        som_bater_parede.play()

    # Verificação de colisões no limite esquerdo ou direito

    if (posicao_x >= limite_direito - 1) or (posicao_x <= limite_esquerdo + 1):

        bola['direcao_x'] *= -1 # Inverte a direção no eixo xx
        som_bater_parede.play()



# Função  utilizada para escrever as coordenadas no ficheiro do replay

def cord_ficheiros(ficheiro,estado_jogo,objeto):

        for i in range(len(estado_jogo['var'][objeto])):

            for j in range(2):
                ficheiro.write(f"{estado_jogo['var'][objeto][i][j]:.3f}")

                if j == 0:
                    ficheiro.write(",")

            if i != len(estado_jogo['var'][objeto]) - 1: # Para não colocar o último ";"
                ficheiro.write(";")


def verifica_golo_jogador_vermelho(estado_jogo):

    '''
    Função responsável por verificar se um determinado jogador marcou golo.
    Para fazer esta verificação poderá fazer uso das constantes:
    LADO_MAIOR_AREA e
    START_POS_BALIZAS.
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador,
    criar um ficheiro que permita fazer a análise da jogada pelo VAR,
    e reiniciar o jogo com a bola ao centro.
    O ficheiro para o VAR deverá conter todas as informações necessárias
    para repetir a jogada, usando as informações disponíveis no objeto
    estado_jogo['var']. O ficheiro deverá ter o nome

    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt

    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul]
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;

    Em cada linha, os valores de xx e yy das coordenadas são separados por uma
    ',', e cada coordenada é separada por um ';'.
    '''

    bola = estado_jogo['bola']  # Acedemos ao dicionario da bola

    if (bola["objeto"].xcor() >= LARGURA_JANELA / 2 - 1 and -RAIO_MEIO_CAMPO * 2 <= bola[ "objeto"].ycor() <= RAIO_MEIO_CAMPO * 2): # -1 porque é o raio da bola

        estado_jogo["pontuacao_jogador_vermelho"] += 1
        update_board(estado_jogo)

        som_rede_golos.play()

        estado_jogo["jogador_vermelho"].goto(-ALTURA_JANELA / 2 - LADO_MENOR_AREA, 0)
        estado_jogo["jogador_azul"].goto(ALTURA_JANELA / 2 + LADO_MENOR_AREA , 0) 


        TotalGolosJogadorVermelho = estado_jogo['pontuacao_jogador_vermelho']
        TotalGolosJogadorAzul = estado_jogo['pontuacao_jogador_azul']

        nome_ficheiro = f"replay_golo_jv_{TotalGolosJogadorVermelho}_ja_{TotalGolosJogadorAzul}.txt"

        with open(nome_ficheiro, "a") as ficheiro:

            cord_ficheiros(ficheiro,estado_jogo,"bola")

            ficheiro.write("\n")

            cord_ficheiros(ficheiro,estado_jogo, "jogador_vermelho")

            ficheiro.write("\n")

            cord_ficheiros(ficheiro,estado_jogo,"jogador_azul")

        # Volta a colocar a bola na posição inicial

        
        bola['objeto'].goto(BOLA_START_POS)
        

        # Escolhe aleatoriamente a nova direção da bola

        nova_direcao_x = random.uniform(-1, 1)
        nova_direcao_y = random.uniform(-1, 1)

        bola['direcao_x'] = nova_direcao_x
        bola['direcao_y'] = nova_direcao_y

        # Apaga tudo o que está escrito nas listas para que no próximo golo só guarde as posições dessa jogada

        estado_jogo["var"]["bola"] = []
        estado_jogo["var"]["jogador_vermelho"] = []
        estado_jogo["var"]["jogador_azul"] = []

        cronometragem_depois_golo()

    pass


def verifica_golo_jogador_azul(estado_jogo):
    '''
    Função responsável por verificar se um determinado jogador marcou golo.
    Para fazer esta verificação poderá fazer uso das constantes:
    LADO_MAIOR_AREA e
    START_POS_BALIZAS.
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador,
    criar um ficheiro que permita fazer a análise da jogada pelo VAR,
    e reiniciar o jogo com a bola ao centro.
    O ficheiro para o VAR deverá conter todas as informações necessárias
    para repetir a jogada, usando as informações disponíveis no objeto
    estado_jogo['var']. O ficheiro deverá ter o nome

    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt

    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul]
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;

    Em cada linha, os valores de xx e yy das coordenadas são separados por uma
    ',', e cada coordenada é separada por um ';'.
    '''

    bola = estado_jogo['bola']


    if (bola["objeto"].xcor() <= -LARGURA_JANELA / 2 + 1 and -RAIO_MEIO_CAMPO * 2 <= bola["objeto"].ycor() <= RAIO_MEIO_CAMPO * 2):  # +1 pois é o raio da bola

        estado_jogo["pontuacao_jogador_azul"] += 1
        update_board(estado_jogo)

        som_rede_golos.play()

        estado_jogo["jogador_vermelho"].goto(-ALTURA_JANELA / 2 - LADO_MENOR_AREA, 0)
        estado_jogo["jogador_azul"].goto(ALTURA_JANELA / 2 + LADO_MENOR_AREA , 0) 

        TotalGolosJogadorVermelho = estado_jogo['pontuacao_jogador_vermelho']
        TotalGolosJogadorAzul = estado_jogo['pontuacao_jogador_azul']

        nome_ficheiro = f"replay_golo_jv_{TotalGolosJogadorVermelho}_ja_{TotalGolosJogadorAzul}.txt"

        with open(nome_ficheiro, "a") as ficheiro:

            cord_ficheiros(ficheiro,estado_jogo,"bola")

            ficheiro.write("\n")

            cord_ficheiros(ficheiro,estado_jogo, "jogador_vermelho")

            ficheiro.write("\n")

            cord_ficheiros(ficheiro,estado_jogo,"jogador_azul")

        # Volta a colocar a bola na posição inicial
        
        bola['objeto'].goto(BOLA_START_POS)
       

        # Escolhe aleatoriamente a nova direção da bola

        nova_direcao_x = random.uniform(-1, 1)
        nova_direcao_y = random.uniform(-1, 1)

        bola['direcao_x'] = nova_direcao_x
        bola['direcao_y'] = nova_direcao_y


        # Apaga tudo o que está escrito nas listas para que no próximo golo só guarde as posições dessa jogada

        estado_jogo["var"]["bola"] = []
        estado_jogo["var"]["jogador_vermelho"] = []
        estado_jogo["var"]["jogador_azul"] = []

        cronometragem_depois_golo()  


def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)


def verifica_toque_jogador_azul(estado_jogo):
    '''
    Função responsável por verificar se o jogador tocou na bola.
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''

    bola = estado_jogo['bola']['objeto']
    jogador_azul = estado_jogo['jogador_azul']

    if (jogador_azul.distance(bola)) < (RAIO_JOGADOR*DEFAULT_TURTLE_SCALE + 1):

        som_chutar_bola.play()

        vetor_x = jogador_azul.xcor() - bola.xcor()
        vetor_y = jogador_azul.ycor() - bola.ycor()

        hipotenusa = (vetor_x**2 + vetor_y**2)**(1/2)

        vetor_x = vetor_x / hipotenusa
        vetor_y = vetor_y / hipotenusa


        estado_jogo['bola']['direcao_x']= -vetor_x
        estado_jogo['bola']['direcao_y'] = -vetor_y


def verifica_toque_jogador_vermelho(estado_jogo):
    '''
    Função responsável por verificar se o jogador tocou na bola.
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''

    bola = estado_jogo['bola']['objeto']
    jogador_vermelho = estado_jogo['jogador_vermelho']

    if (jogador_vermelho.distance(bola)) < (RAIO_JOGADOR*DEFAULT_TURTLE_SCALE + 1):

        som_chutar_bola.play()

        vetor_x = jogador_vermelho.xcor() - bola.xcor()
        vetor_y = jogador_vermelho.ycor() - bola.ycor()

        hipotenusa = (vetor_x**2 + vetor_y**2)**(1/2)

        vetor_x = vetor_x / hipotenusa
        vetor_y = vetor_y / hipotenusa


        estado_jogo['bola']['direcao_x']= -vetor_x
        estado_jogo['bola']['direcao_y'] = -vetor_y


def guarda_posicoes_para_var(estado_jogo):
    estado_jogo['var']['bola'].append(estado_jogo['bola']['objeto'].pos())
    estado_jogo['var']['jogador_vermelho'].append(estado_jogo['jogador_vermelho'].pos())
    estado_jogo['var']['jogador_azul'].append(estado_jogo['jogador_azul'].pos())


def main():
    estado_jogo = init_state()
    setup(estado_jogo, True)
    while True:
        estado_jogo['janela'].update()

        guarda_posicoes_para_var(estado_jogo) # Vamos ler as posições da bola e dos jogadores a cada instante

        if estado_jogo['bola'] is not None:
            movimenta_bola(estado_jogo)
        verifica_colisoes_ambiente(estado_jogo)
        verifica_golos(estado_jogo)
        if estado_jogo['jogador_vermelho'] is not None:
            verifica_toque_jogador_azul(estado_jogo)
        if estado_jogo['jogador_azul'] is not None:
            verifica_toque_jogador_vermelho(estado_jogo)


if __name__ == '__main__':
    main()
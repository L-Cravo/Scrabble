"""
Segundo projeto de Fundamentos da Programação: 
Scrabble 2! 

Outubro de 2025

Autor: Lourenço Cravo, LEIC-A, IST.
Email para contacto: lourencocravo8@gmail.com
Número de aluno: ist1117782
"""

#Constantes globais
LETRAS = ('A','B','C','Ç','D','E','F','G','H','I','J','L','M','N','O','P','Q','R','S','T','U','V','X','Z') #Para ordenar letras

SET_LETRAS = {'A','B','C','Ç','D','E','F','G','H','I','J','L','M','N','O','P','Q','R','S','T','U','V','X','Z'} #Para verificar que letras existem no alfabeto

SACO = {
    'A': 14, 'B': 3,  'C': 4, 'Ç': 2, 'D': 5,  'E': 11, 'F': 2,  'G': 2,
    'H': 2,  'I': 10, 'J': 2,  'L': 5,  'M': 6,  'N': 4,  'O': 10,
    'P': 4,  'Q': 1,  'R': 6,  'S': 8,  'T': 5,  'U': 7,  'V': 2,
    'X': 1,  'Z': 1  
}

TABELA_PONTOS = {
    'A': 1, 'B': 3, 'C': 2, 'Ç': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 4, 'H': 4,
    'I': 1, 'J': 5, 'L': 2, 'M': 1, 'N': 3, 'O': 1, 'P': 2, 'Q': 6,
    'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'X': 8, 'Z': 8}

TAMANHO_TAB = 15


####################
# TAD casa (2.1.1) #
####################

#Representação interna: tuplo de dois inteiros (linha, coluna)

#Construtor

def cria_casa(lin: int, col: int) -> tuple[int, int]:
    """Criar uma casa do tabuleiro."""
    
    if type(lin) != int or type(col) != int or not ((1 <= lin <= 15) and (1 <= col <= 15)):
        raise ValueError("cria_casa: argumentos inválidos")
    
    return (lin, col)


#Seletores   

def obtem_col(c: tuple[int, int]) -> int:
    """Obter a coluna de uma casa do tabuleiro."""
    
    _ = cria_casa(c[0], c[1])
    
    return c[1]


def obtem_lin(c: tuple[int, int]) -> int:
    """Obter a linha de uma casa do tabuleiro."""
    
    _ = cria_casa(c[0], c[1])
    
    return c[0]


#Reconhecedor

def eh_casa(arg) -> bool:
    """Verificar se um argumento (de tipo universal) é uma casa do tabuleiro."""
    
    if not (type(arg) == tuple and len(arg) == 2):
        return False
    
    return (type(arg[0]) == int and type(arg[1]) == int and (1 <= arg[0] <= 15) and (1 <= arg[1] <= 15))


#Teste

def casas_iguais(c1, c2) -> bool:
    """Verificar se duas casas do tabuleiro são iguais."""
    
    return (eh_casa(c1) and eh_casa(c2) and c1[0] == c2[0] and c1[1] == c2[1])


#Transformadores  

def casa_para_str(c: tuple[int, int]) -> str:
    """Representar uma casa do tabuleiro em string."""
    
    return f"({obtem_lin(c)},{obtem_col(c)})"


def str_para_casa(s: str) -> tuple[int, int]:  
    """Converter uma string numa casa do tabuleiro."""
    
    s = s.strip()
    coordenadas = s[1:-1].split(',')    
    lin = int(coordenadas[0].strip())
    col = int(coordenadas[1].strip())
    
    return cria_casa(lin, col) 


#Função de alto nível

def incrementa_casa(c: tuple[int, int], direcao: str, distancia: int) -> tuple[int, int]: 
    """Incrementar uma casa do tabuleiro numa dada direção e distância, validando os argumentos e a nova casa."""
    
    if not eh_casa(c) or direcao not in ['H', 'V'] or distancia <= 0:
        return c
    
    if direcao == 'H':
        try:
            casa = cria_casa(obtem_lin(c), obtem_col(c) + distancia)
        except ValueError:
            return c
    
    elif direcao == 'V':
        try:
            casa = cria_casa(obtem_lin(c) + distancia, obtem_col(c))
        except ValueError:
            return c
    
    return casa


#######################
# TAD jogador (2.1.2) #
#######################

#Representação interna: dicionário com as keys 'id' (str), 'tipo' (str), 'pontos' (int) e 'letras' (dict[str: int]).
# 'id' -> nome do jogador (humano) ou nível do agente (agente)

#Construtores

def cria_humano(nome: str) -> dict['id': str, 'tipo': str, 'pontos': int, 'letras': dict[str: int]]:
    """Criar um jogador humano, validando o argumento."""
    
    if not isinstance(nome, str) or not len(nome) > 0:
        raise ValueError("cria_humano: argumento inválido")
    
    humano = {'id': nome,'tipo': 'HUMANO', 'pontos': 0, 'letras': {}}
    
    return humano


def cria_agente(nivel: str) -> dict['id': str, 'tipo': str, 'pontos': int, 'letras': dict[str: int]]:
    """Criar um jogador agente, validando o argumento."""
    
    if nivel not in ['FACIL', 'MEDIO', 'DIFICIL']:
        raise ValueError("cria_agente: argumento inválido")
    
    agente = {'id': nivel,'tipo': 'AGENTE', 'pontos': 0, 'letras': {}}

    return agente


#seletores

def jogador_identidade(jog: dict) -> str:  
    """Devolver a identidade (id) do jogador."""
    
    return jog['id']


def jogador_pontos(jog: dict) -> int:        
    """Devolver os pontos do jogador."""
    
    return jog['pontos']


#Auxiliar
def ordena_conjunto(conj: dict[str: int]) -> list[str]:  
    """
    Providênciar uma lista de letras ordenada alfabeticamente.

    Função auxiliar da jogador_letras.
    Ordena alfabeticamente um dicionário de letras e ocorrências numa lista.
    Input:
    -conj: conjunto (dicionário) de letras no formato "Letra: ocorrências"
    Output: 
    Lista ordenada alfabeticamente com as ocorrências respetivas de cada letra 
    """
    
    letras_sorted = []
    
    for l in LETRAS:
        if l in conj:                   
            for _ in range(conj[l]):    
                letras_sorted.append(l)
    
    return letras_sorted 


def jogador_letras(jog: dict[str: int]) -> str:     
    """Representa o conjunto de letras do jogador como uma string ordenada alfabeticamente."""
    
    conj_letras = jog['letras']
    return ''.join(ordena_conjunto(conj_letras))


#Modificadores


def recebe_letra(jog: dict, letra: str) -> dict['id': str, 'tipo': str, 'pontos': int, 'letras': dict[str: int]]:
    """Adicionar uma letra ao conjunto de letras do jogador."""
    
    conj_letras_jogador = jog['letras']
    conj_letras_jogador[letra] = conj_letras_jogador.get(letra, 0) + 1

    return jog


def usa_letra(jog: dict, letra: str) -> dict['id': str, 'tipo': str, 'pontos': int, 'letras': dict[str: int]]:  
    """Remover uma letra do conjunto de letras do jogador."""
    
    conj_letras_jogador = jog['letras']
    
    if letra not in conj_letras_jogador:
        return jog
    
    conj_letras_jogador[letra] -= 1
    if conj_letras_jogador[letra] == 0:
        del conj_letras_jogador[letra]
    
    return jog


def soma_pontos(jog: dict, pontos: int) -> dict['id': str, 'tipo': str, 'pontos': int, 'letras': dict[str: int]]:
    """Adicionar pontos ao total de pontos do jogador."""
    
    jog['pontos'] += pontos
    return jog


#Reconhecedores


def eh_jogador(arg) -> bool:
    """Verificar se um argumento (de tipo universal) é um jogador."""
    
    if not isinstance(arg, dict) or len(arg) != 4:
        return False
    
    if not ('letras' in arg.keys() and type(arg['letras']) == dict):
        return False
    
    if arg['letras'] != {} and not (all(letra in SET_LETRAS for letra in arg['letras'].keys()) and
            all((type(arg['letras'][letra]) == int and arg['letras'][letra] > 0) for letra in arg['letras'].keys())):
        return False
    
    return ('id' in arg and isinstance(arg['id'], str) and 
            'pontos' in arg and type(arg['pontos']) == int and
            'tipo' in arg and arg['tipo'] in {'HUMANO', 'AGENTE'})


def eh_humano(arg) -> bool:
    """Verificar se um argumento (de tipo universal) é um jogador humano."""
    
    return eh_jogador(arg) and arg['tipo'] == 'HUMANO'


def eh_agente(arg) -> bool:
    """Verificar se um argumento (de tipo universal) é um jogador agente."""
    
    return eh_jogador(arg) and arg['tipo'] == 'AGENTE'


#Teste

def jogadores_iguais(j1, j2) -> bool:
    """Verificar se dois jogadores são iguais."""
    
    if not eh_jogador(j1) or not eh_jogador(j2):
        return False
    
    return j1 == j2


#Transformador

def jogador_para_str(jog: dict[str: int, str: int, str: dict[str: int]]) -> str:
   """Representa o jogador visualmente, em forma de string."""
   
   id = jogador_identidade(jog)
   pontos = jogador_pontos(jog)
   letras = jogador_letras(jog)
   
   if eh_agente(jog):
       id = f"BOT({id})"
   
   #String final
   jogador_str = "{} ({:>3}): {}".format(id, pontos, ' '.join(list(letras)))

   return jogador_str.rstrip()


#Função de alto nível


def distribui_letras(jog: dict[str: int, str: int, str: dict[str: int]], saco: list, num: int) -> dict['id': str, 'tipo': str, 'pontos': int, 'letras': dict[str: int]]:
    """
    Utiliza uma lista de letras como uma pilha para adicionar a última da lista ao conjunto de letras do jogador, 
    devolvendo True or False consoante o sucesso da operação.
    Args:
    -letras: lista de letras 
    -jogador: o jogador cujo conjunto de letras se pretende modificar.
    Output:
    O jogador modificado com as letras adicionadas ao seu conjunto de letras.
    """
    
    #Verificar se a lista está vazia (não há operações para realizar)
    if len(saco) == 0:
        return jog
    
    i = 0
    while i < num:
        #Verificar se o saco ficou vazio
        if len(saco) == 0:
            break
    
        ultima_letra_saco = saco.pop()
    
        #Verificar se a letra é válida, por segurança.
        if ultima_letra_saco not in SET_LETRAS:
            return jog
        
        jog = recebe_letra(jog, ultima_letra_saco)

        i += 1
    
    return jog 


###########################
# TAD vocabulario (2.1.3) #
###########################

#Representação interna: tuplo de dois dicionários.
# Primeiro dicionário: key -> (comprimento, primeira letra); value -> lista de tuplos (palavra, pontos)
# Segundo dicionário: key -> palavra; value -> pontos

#Construtor

def cria_vocabulario(palavras: tuple[str, ...]) -> tuple[dict[tuple[int, str]: list[tuple[str, int]]], dict[str: int]]:
    """Criar um vocabulário a partir de um tuplo de palavras, validando o argumento."""
    
    #Validação do argumento
    if not isinstance(palavras, tuple) or not palavras:
        raise ValueError("cria_vocabulario: argumento inválido")
    if not len(set(palavras)) == len(palavras):  #Verifica se há palavras repetidas
        raise ValueError("cria_vocabulario: argumento inválido")
    for palavra in palavras:
        if not isinstance(palavra, str):
            raise ValueError("cria_vocabulario: argumento inválido")
        if not 2 <= len(palavra) <= 15:
            raise ValueError("cria_vocabulario: argumento inválido")
        for letra in palavra:
            if letra not in SET_LETRAS:
                raise ValueError("cria_vocabulario: argumento inválido")
     
    #Construção do vocabulário
    vocabulario = ({},{})
    for palavra in palavras:
        comp = len(palavra)
        letra = palavra[0]
        pontos = sum(TABELA_PONTOS[letra] for letra in palavra)

        vocabulario[1][palavra] = pontos
        
        if (comp, letra) not in vocabulario[0]:
            vocabulario[0][(comp, letra)] = []
        vocabulario[0][(comp, letra)].append((palavra, pontos)) 
    
    #Vamos já ordenar as listas do primeiro dicionário para o obtem_palavra

    #A função que servirá como key do sort 
    def chave_ordenacao(palavra_pontos: tuple) -> tuple[int, list[int]]:
        palavra, pontos = palavra_pontos
        return (-(pontos), [LETRAS.index(letra) for letra in palavra])  #Primeiro critério é ordem descendente de pontos. Segundo critério é ordem alfabética.
    
    #Ordernar cada lista de cada primeira letra com cada comprimento
    for key in vocabulario[0]:
        lista = vocabulario[0][key]
        #O sort irá comparar a pontuação de cada tuplo da lista e colocar os tuplos com maior pontuação primeiro (por isso é que usámos '-pontos' na chave de ordenação: lembrar que o valor default do parâmetro reverse é False). 
        #Se houver empates de pontos, irá comparar as listas dos índices das letras (os quais correspondem com os índices das letras da lista LETRAS) das palavras. 
        #Exemplo do segundo critério:
        # "CAO" -> C (2), A (0), O (14) -> [2,0,14]
        # "CAÇA" -> C (2), A (0), Ç (3), A (0) -> [2,0,3,0]
        # "CASA" -> C (2), A (0), S (18), A (0) -> [2,0,18,0]
        # Ordem final: CAÇA, CAO, CASA
        lista.sort(key = chave_ordenacao)   
    
    return vocabulario

#Seletores

#Auxiliar
def verifica_comp_letra(vocab: tuple, comp: int, letra: str) -> bool:
    """Verifica se um comprimento e uma primeira letra existem no vocabulário fornecido."""
    
    if (comp, letra) not in vocab[0]:
        return False
    
    return True
    

def obtem_pontos(vocabulario: tuple, palavra: str) -> int:
    """Obter a pontuação de uma palavra no vocabulário. Se a palavra não existir, devolve 0."""
    
    return vocabulario[1].get(palavra, 0)


def obtem_palavras(vocabulario: tuple, comp: int, letra: str) -> tuple:
    """
    Obter um tuplo de pares (palavra, pontuação) de palavras do vocabulário com um determinado comprimento e primeira letra, ordenadas por pontuação decrescente e ordem alfabética.
    Devolver um tuplo vazio se não existirem palavras com esse comprimento e primeira letra no vocabulário.
    
    Args:   
    -vocabulario: vocabulário do jogo.
    -comp: comprimento das palavras a obter.
    -letra: primeira letra das palavras a obter.
    Output:
    Tuplo de pares (palavra, pontuação) ou tuplo vazio.
    """
    
    if not verifica_comp_letra(vocabulario, comp, letra):
        return ()
    
    return tuple(vocabulario[0][(comp, letra)])  
    

#Teste

def testa_palavra_padrao(vocabulario: tuple[dict, dict], palavra: str, padrao: str, letras: str) -> bool:
    """Testar se uma palavra existe no vocabulário do jogo e pode ser inserida num padrão do tabuleiro, dadas as letras do jogador."""
    
    if palavra not in vocabulario[1]:
        return False
    
    if len(palavra) != len(padrao):
        return False

    for letra_palavra, letra_padrao in zip(palavra, padrao):    #Percorre os caracteres da palavra e do padrão com o mesmo índice
        if letra_padrao == '.':
            # Verifica se a string letras tem quantidade suficiente de uma determinada letra da palavra para satisfazer a correspondência entre palavra e padrão.
            # Exemplo: se a palavra contem 4 ocorrências da letra 'A' e o padrão tem 2 ocorrências da letra 'A', então o jogador necessita de ter 4-2 = 2 ocorrências da letra A para conseguir completar o padrão de forma a construir a palavra. 
            if letras.count(letra_palavra) < palavra.count(letra_palavra) - padrao.count(letra_palavra):
                return False
        else:
            # Verifica se letras fixas no padrão coincidem com as letras correspondentes na palavra
            if letra_padrao == letra_palavra:
                continue
            else:
                return False  
    
    return True 


#Transformadores

def ficheiro_para_vocabulario(nome_fich: str) -> tuple[dict[tuple[int, str]: list[tuple[str, int]]], dict[str: int]]:
    """Transformar um ficheiro de texto num vocabulário do jogo."""
    
    with open(nome_fich, 'r', encoding = 'utf-8') as file:
        palavras = {linha.strip().upper() for linha in file 
                    if 2 <= len(linha.strip().upper()) <= 15 and 
                    all(c in SET_LETRAS for c in linha.strip().upper())}
    
    #Criar o vocabulário do 0, para evitar chamar o cria_vocabulario, que repetiria as verificações já feitas acima.
    
    #Construção do vocabulário
    vocabulario = ({},{})
    for palavra in palavras:
        comp = len(palavra)
        letra = palavra[0]
        pontos = sum(TABELA_PONTOS[letra] for letra in palavra)
        
        if palavra not in vocabulario[1]: 
            vocabulario[1][palavra] = pontos
        
        if (comp, letra) not in vocabulario[0]:
            vocabulario[0][(comp, letra)] = []
        vocabulario[0][(comp, letra)].append((palavra, pontos)) 
    
    def chave_ordenacao(palavra_pontos: tuple) -> tuple[int, list[int]]:
        palavra, pontos = palavra_pontos
        return (-(pontos), [LETRAS.index(letra) for letra in palavra])  #Primeiro critério é ordem descendente de pontos. Segundo critério é ordem alfabética.
    
    for key in vocabulario[0]:
        lista = vocabulario[0][key]
        lista.sort(key = chave_ordenacao)   
    
    return vocabulario
                    

def vocabulario_para_str(vocabulario: tuple[dict[tuple[int, str]: list[tuple[str, int]]], dict[str: int]]) -> str:
    """Representar o vocabulário do jogo em forma de string, ordenado por comprimento, primeira letra, pontuação e ordem alfabética."""
    
    vocab_list = list(vocabulario[1].keys())

    vocab_list.sort(key = lambda x: (len(x), LETRAS.index(x[0]), -sum(TABELA_PONTOS[letra] for letra in x), [LETRAS.index(letra) for letra in x]))

    return '\n'.join(vocab_list)


#Função de alto de nível

def procura_palavra_padrao(vocabulario, padrao: str, letras: str, min_pontos: int) -> tuple:
    """
    Procurar a palavra com melhor pontuação do vocabulário que se encaixe num padrão do tabuleiro, dadas as letras do jogador e uma pontuação mínima.
    
    Args:
    -vocabulario: vocabulário do jogo.
    -padrao: padrão do tabuleiro.
    -letras: letras do jogador.
    -min_pontos: pontuação mínima da palavra a procurar.

    Output:
    Tuplo (palavra, pontuação) da melhor palavra encontrada ou ('', 0) se não existir nenhuma palavra válida.
    """
    
    res = ('', 0)
    c_inicial_padrao = padrao[0]

    if c_inicial_padrao != '.':
        tuplo_pares = obtem_palavras(vocabulario, len(padrao), c_inicial_padrao)
        if tuplo_pares:
            for palavra, pontuacao in tuplo_pares:
                if pontuacao < min_pontos:
                    break #Se a primeira palavra tem pontuação < min_pontos, nenhuma outra terá pontuação aceitável
                if testa_palavra_padrao(vocabulario, palavra, padrao, letras) and pontuacao >= min_pontos:
                    res = (palavra, pontuacao)
                    break #A primeira palavra válida no tuplo_pares é a que tem a maior pontuação, logo não vale a pena verificar as outras.
    else:
        letras_sorted = sorted(set(letras)) #usar set melhora eficiência ao evitar letras duplicadas se a string letras tem duplicados 
        melhor_palavra = ''
        melhor_pontuacao = 0
        
        for letra_inicial in letras_sorted:
            tuplo_pares_possiveis = obtem_palavras(vocabulario, len(padrao), letra_inicial)
            if tuplo_pares_possiveis:
                for palavra, pontuacao in tuplo_pares_possiveis:
                    if pontuacao < min_pontos:
                        break
                    if testa_palavra_padrao(vocabulario, palavra, padrao, letras) and pontuacao >= min_pontos:
                        #A primeira palavra válida com cada letra_inicial será a que tem maior pontuação no tuplo_pares_possiveis. 
                        #Esta é a melhor candidata do tuplo inteiro, não vale a pena verificar as outras
                        if pontuacao > melhor_pontuacao:
                            melhor_pontuacao = pontuacao
                            melhor_palavra = palavra
                        break  #Melhora eficiência
        
        #Atualiza o resultado apenas se encontrou uma palavra melhor
        if melhor_palavra:
            res = (melhor_palavra, melhor_pontuacao)
    
    return res


#########################
# TAD tabuleiro (2.1.4) #
#########################

#Representação interna: lista de listas de strings (cada string é uma letra ou um ponto)


#Construtor

def cria_tabuleiro() -> list[list[str]]:  #Lembrar que o tabuleiro é uma lista de listas                       
    """Função que cria o tabuleiro, uma lista de 15 listas que contêm 15 pontos cada uma."""
    
    #Utilizando list comprehension, o código é mais conciso e não copia a referência para uma mesma lista 15 vezes.
    #Apesar de ser uma shallow copy, não existe problema pois strings (o contéudo das sublistas) são imutáveis.
    tab = [['.' for _ in range(TAMANHO_TAB)] for _ in range(TAMANHO_TAB)]   
    
    return tab


#Seletores

def obtem_letra(tab: list[list[str]], casa: tuple[int, int]) -> str:
    """Devolve o valor contido numa casa do tabuleiro."""
    
    l, c = obtem_lin(casa), obtem_col(casa)
    
    #Retorno do seu valor, acedendo ao tabuleiro. Lembrar que o indexing do python começa em zero, mas a linha e coluna do tabuleiro começa em 1. 
    return str(tab[l-1][c-1]) 


#Modificadores

def insere_letra(tab: list[list[str]], casa: tuple[int, int], letra: str) -> list[list[str]]:
    """Insere uma letra numa determinada casa de um tabuleiro."""
    
    linha,coluna = obtem_lin(casa), obtem_col(casa)           

    tab[linha-1][coluna-1] = letra    #Insere as varíaveis no tabuleiro, destrutivamente. Lembrar o indexing do python comparado com o indexing do tabuleiro.
    
    return tab  


#Reconhecedores

def eh_tabuleiro(tab):
    """Verifica se um argumento (de tipo universal) é um tabuleiro."""
    
    if not isinstance(tab, list) or len(tab) != TAMANHO_TAB:
        return False
    for linha in tab:
        if not isinstance(linha, list) or len(linha) != TAMANHO_TAB:
            return False
        for c in linha:
            if len(c) != 1 or not isinstance(c, str) or (c != '.' and not c in SET_LETRAS):
                return False
    
    return True


def eh_tabuleiro_vazio(arg) -> bool:
    """
    """
    if not eh_tabuleiro(arg):
        return False
    
    return tabuleiros_iguais(arg, cria_tabuleiro())


#Teste

def tabuleiros_iguais(t1, t2):
    """Verifica se dois tabuleiros são iguais, validando os argumentos."""
    
    if not (eh_tabuleiro(t1) and eh_tabuleiro(t2)):
        return False
    
    # Compara casa por casa
    for linha in range(1, TAMANHO_TAB + 1):  
        for coluna in range(1, TAMANHO_TAB + 1):
            casa = cria_casa(linha, coluna)
            if obtem_letra(t1, casa) != obtem_letra(t2, casa):
                return False
    
    return True


#Transformador

def tabuleiro_para_str(tab: list[list[str]]) -> str:
    """Converte a representação interna do tabuleiro numa string formatada para exibição."""
    
    # O tamanho do tabuleiro é derivado do argumento recebido.
    tamanho_tabuleiro = len(tab)
    
    # --- Construção do Cabeçalho (números das colunas) ---
    
    # Dígitos das unidades (ex: 1 2 3 ... 9 0 1 ... 5)
    unidades_cols = " ".join([str((i % 10)) for i in range(1, tamanho_tabuleiro + 1)])  #lembrar que o range é exclusivo no segundo argumento e que queremos contar a partir de 1
    # Dígitos das dezenas (ex:           1 1 ... 1): espaços se os números não tiverem componente de dezena, e "1" se forem > 10.
    dezenas_cols = " ".join([' ' if i < 10 else '1' for i in range(1, tamanho_tabuleiro + 1)]) #Repare-se que as duas linhas que numeram as colunas do tabuleiro têm o mesmo comprimento, logo estão perfeitamente alinhadas

    #----Alinhamento das linhas da numeração das colunas com as casas do tabuleiro----
    # O prefixo alinha os números das colunas com as letras do tabuleiro.
    # O conteúdo de uma linha começa após "N | ", que tem 5 caracteres (ex: "15 | A...").
    prefixo_cabecalho = ' ' * 5
    linha_dezenas = f"{prefixo_cabecalho}{dezenas_cols}"
    linha_unidades = f"{prefixo_cabecalho}{unidades_cols}"

    # --- Construção da Borda ---

    # O conteúdo da borda (-) deve abranger todas as colunas e os espaços entre elas.
    conteudo_borda = '-' * (tamanho_tabuleiro * 2 + 1) # x2 porque as casas do tabuleiro terão espaços entre elas. O +1 serve para ter em conta os espaços entre as bordas "|" e a primeira e última letra. 
                                                       
    
    # O prefixo alinha a borda com as barras verticais "|" do tabuleiro.
    # A borda começa após "N ", que tem 3 caracteres (ex: "15 |...").
    prefixo_borda = ' ' * 3
    linha_borda = f"{prefixo_borda}+{conteudo_borda}+"
    
    # --- Montagem da String Final ---
    
    # Começamos a lista de linhas com os componentes já criados
    linhas_finais = [   
        linha_dezenas,
        linha_unidades,
        linha_borda]
    
    # Adicionamos cada linha do tabuleiro, formatada com o seu número à esquerda
    for i in range(len(tab)):
        num_linha = i + 1
        letras_linha = " ".join(tab[i])
        linhas_finais.append(f"{num_linha:>2} | {letras_linha} |") #Alinhar os números à direita, conforme o enunciado
        
    # Adicionamos a borda inferior
    linhas_finais.append(linha_borda)
    
    # Juntamos todas as linhas numa única string, separadas por quebras de linha
    return "\n".join(linhas_finais)


#Funções de alto nível


def obtem_padrao(tab, casa_i, casa_j) -> str:
    """
    Obtem o padrão entre duas casas (casa_i e casa_j) do tabuleiro que estejam na mesma linha ou coluna.
    
    Args:
    -tab: um tabuleiro.
    -casa_i: um tuplo contendo a linha e a coluna da casa inicial do padrão.
    -casa_j: um tuplo contendo a linha e a coluna da casa final do padrão.
    
    Output:
    String com o padrão obtido entre as duas casas.
    """
    if obtem_lin(casa_i) == obtem_lin(casa_j):
        direcao = 'H'
    elif obtem_col(casa_i) == obtem_col(casa_j):
        direcao = 'V'
    
    padrao = ""
    
    #Constrói a sequência, obtendo o valor contido no tabuleiro, casa a casa.
    if direcao == "H": 
        for i in range(obtem_col(casa_i), obtem_col(casa_j) + 1):
            padrao += obtem_letra(tab, cria_casa(obtem_lin(casa_i), i))  #Valida a casa com a função cria casa, em cada iteração.
    
    elif direcao == "V":
        for i in range(obtem_lin(casa_i), obtem_lin(casa_j) + 1):
            padrao += obtem_letra(tab, cria_casa(i, obtem_col(casa_i)))
    
    return padrao


def insere_palavra(tab, casa, direcao, palavra):
    """
    Insere uma palavra no tabuleiro.
    
    Usa a função insere_letra para inserir palavras completas no tabuleiro, destrutivamente (ou seja, substituindo os pontos pela palavra).
    Args:
    -tab: um tabuleiro.
    -casa: um tuplo contendo a linha e a coluna da casa inicial da palavra.
    -direcao: a direção em que a palavra é formada ('H' ou 'V').
    -palavra: palavra a inserir.
    
    Output: 
    Modifica destrutivamente o tabuleiro com a palavra inserida no sítio e direção especificados.
    """
   
    linha, coluna = obtem_lin(casa), obtem_col(casa)
    
    if direcao == "H":
        for i in range(len(palavra)):   #Percorre os indices da palavra, um a um.
            insere_letra(tab, cria_casa(linha, coluna+i), palavra[i])  #Usa a função insere_letra para inserir as letras uma a uma na direção especificada, validando as casas a cada iteração.
    
    elif direcao == "V":
        for i in range(len(palavra)):
            insere_letra(tab, cria_casa(linha+i, coluna), palavra[i])
    
    return tab  


def obtem_subpadroes(tab, i, f, l_espacos: int) -> tuple[tuple[str, ...], tuple[tuple[int, int], ...]]:
    """
    Obtem todos os subpadrões válidos entre duas casas (i e f) do tabuleiro que estejam na mesma linha ou coluna,
    com um número máximo de espaços definido por l_espacos.
    
    Args:
    -tab: um tabuleiro.
    -i: casa inicial do padrão original.
    -f: casa final do padrão original.
    -l_espacos: número máximo de espaços livres ('.') permitidos num subpadrão.
    
    Output:
    Tuplo com dois tuplos: o primeiro contém os subpadrões obtidos (strings) e o segundo contém as casas iniciais de cada subpadrão.
    """
    
    if obtem_lin(i) == obtem_lin(f):
        direcao = 'H'
    elif obtem_col(i) == obtem_col(f):
        direcao = 'V'
    
    padrao = obtem_padrao(tab, i, f)
    lista_subpadroes = []
    lista_casas = []
    
    for i_idx in range(len(padrao)):
        for j_idx in range(len(padrao), i_idx, -1):
            subpadrao = padrao[i_idx:j_idx]
            
            if all(c == '.' for c in subpadrao):
                continue
            if all(c != '.' for c in subpadrao):
                continue
            if (i_idx > 0 and padrao[i_idx-1] != '.') or (j_idx < len(padrao) and padrao[j_idx] != '.'):
                continue
            
            if subpadrao.count('.') > l_espacos:
                continue

            lista_subpadroes.append(subpadrao)
            
            casa_inicio = incrementa_casa(i, direcao, i_idx)
            lista_casas.append(casa_inicio)
    
    return (tuple(lista_subpadroes), tuple(lista_casas))
    

def gera_todos_padroes(tab, l_espacos) -> tuple[tuple[str, ...], tuple[tuple[int, int], ...], tuple[str, ...]]:
    """
    Gerar todos os subpadrões válidos do tabuleiro, com um número máximo de espaços definido por l_espacos.
    
    Args:
    -tab: um tabuleiro.
    -l_espacos: número máximo de espaços livres ('.') permitidos num subpadrão.
    Output:
    Três tuplos: o primeiro contém os subpadrões obtidos (strings), o segundo contém as casas iniciais de cada subpadrão 
    e o terceiro contém as direções ('H' ou 'V') de cada subpadrão.
    """
    
    lista_subpadroes, lista_casas, lista_dirs = [], [], []
    
    for linha in range(1,TAMANHO_TAB + 1):
        casa_inicio = cria_casa(linha, 1)
        casa_fim = cria_casa(linha, 15)
        
        padroes_linha, casas_linha = obtem_subpadroes(tab, casa_inicio, casa_fim, l_espacos)
        
        lista_subpadroes.extend(padroes_linha)
        lista_casas.extend(casas_linha)
        lista_dirs.extend(['H'] * len(padroes_linha))
    
    for coluna in range(1,TAMANHO_TAB + 1):
        casa_inicio = cria_casa(1, coluna)
        casa_fim = cria_casa(15, coluna)
        
        padroes_coluna, casas_coluna = obtem_subpadroes(tab, casa_inicio, casa_fim, l_espacos)
        
        lista_subpadroes.extend(padroes_coluna)
        lista_casas.extend(casas_coluna)
        lista_dirs.extend(['V'] * len(padroes_coluna))
    
    return tuple(lista_subpadroes), tuple(lista_casas), tuple(lista_dirs)


############################
# Funções adicionais (2.2) #
############################


def baralha_saco(estado: int) -> list[int]:
    """
    Cria uma lista com as letras de um conjunto permutadas.
    
    Utiliza a função auxiliar ordena_saco para transformar o saco de letras do scrabble (dicionário) numa lista ordenada alfabeticamente
    e depois permuta essa lista utilizando a função permuta_letras.
    Args:
    -estado: estado inicial (seed) para o gerador de números pseudo-aleatórios
    Output:
    Lista permutada de letras com as ocorrências respetivas
    """
    def gera_numero_aleatorio(estado: int) -> int:
        """
        Gera um número inteiro pseudo-aleatório. Auxiliar da permuta_letras.

        Usa o algoritmo xorshift para gerar um número pseudo-aleatório. 
        O algoritmo é determinístico e funciona através da transformação sucessiva do seu estado, ou seja, o número anterior gerado.
        O primeiro estado do algoritmo, definido pelo utilizador, chama-se "seed".
        Args:
        -estado: seed (primeiro estado) 
        Output:
        Um nº inteiro pseudo-aleatório
        """
        seed = estado
    
        seed ^= ( seed << 13 ) & 0xFFFFFFFF
        seed ^= ( seed >> 17 ) & 0xFFFFFFFF
        seed ^= ( seed << 5 ) & 0xFFFFFFFF
    
        return seed
    
    def permuta_letras(letras: list[str], estado: int):
        """
        Baralha as letras de uma lista. Auxiliar da baralha_saco.
        
        Permuta as letras de uma lista de acordo com o algoritmo Fisher-Yates. 
        Para a geração do índice aleatório j, aplica a função gera_numero_aleatorio e uma operação módulo de i+1.
        Args: 
        -letras: lista de letras (potencialmente vazia)
        -estado: seed para o gerador de número pseudo-aleatório
        Output:
        Lista letras alterada de forma a estar permutada.
        """
        
        
        n = len(letras)
        s = estado

        if len(letras) == 0:         #Não há operações a realizar se não houver letras
            return

        for i in range(n-1, 0, -1):     #Percorre os índices da lista letras, desde o último(n-1) até ao 1 (lembrar que o segundo argumento do range é exclusivo) 
            s = gera_numero_aleatorio(s)
            j = s % (i+1)
            letras[i], letras[j] = letras[j], letras[i] 
        return                      #Não retorna nada, apenas alterou a lista inicial
    
    def ordena_saco(saco: dict[str: int]) -> list:
        """
        Providência uma lista ordenada alfabeticamente para a função baralha_saco permutá-la. Auxiliar da baralha_saco.

        Função auxiliar da baralha_saco.
        Ordena alfabeticamente um dicionário de letras e ocorrências numa lista.
        Args:
        -saco: conjunto (dicionário) de letras no formato "Letra: ocorrências"
        
        Output: 
        Lista ordenada alfabeticamente com as ocorrências respetivas de cada letra 
        """
     
        lista_letras = []
    
        for letra, occ in saco.items():
            lista_letras.extend([letra] * occ)
        
        return sorted(lista_letras, key = lambda x: LETRAS.index(x))
    
    letras_ordenadas = ordena_saco(SACO)
    
    permuta_letras(letras_ordenadas, estado)
    
    return letras_ordenadas 


#Auxiliar
def ordenar_tuplo(tup:tuple) -> tuple:
    """Ordena tuplo de letras pela ordem definida em LETRAS."""
    
    #Retorna em forma de tuplo ordenado por ordem ascendente do índice com que a letra aparece no tuplo LETRAS.
    return tuple(sorted(tup, key=lambda x: LETRAS.index(x)))


#Auxiliar
def trocar_letras(jog, letras_fora: tuple[str, ...], pilha: list[str]) -> bool:
    """
    Função auxiliar da jogada_humano que faz a troca de letras entre pilha e jogador, caso os parâmetros estejam válidos.
    
    Args:
    -jog: o jogador.
    -letras_fora: as letras do jogador a trocar (tuplo).
    -pilha: a pilha (ou saco) de letras do Scrabble.
    Output:
    Booleano que retorna True caso a operação seja bem-sucedida, False em caso contrário.
    """
    letras_jogador = jogador_letras(jog)

    #Verificar se o jogador tem as letras a serem removidas e se elas são válidas
    #Contar as ocorrências de cada letra no letras_fora
    contador_letras = {}
    for letra in letras_fora:
        contador_letras[letra] = contador_letras.get(letra, 0) + 1
    #Verificar se o jogador tem letras suficientes
    for letra in letras_fora:
        if letra not in SET_LETRAS or letra not in letras_jogador or letras_jogador.count(letra) < contador_letras[letra]:
            return False
    
    #Retirar as letras do saco do jogador 
    for letra in letras_fora:
        usa_letra(jog, letra)
        
    #Número de letras que serão removidas e que têm de ser repostas no conj_letras do jogador
    n_letras = len(letras_fora)
    
    #Repõe o número de letras perdidas de acordo com as regras da função distribui_letras, se houver letras suficientes na pilha
    
    _ = distribui_letras(jog, pilha, n_letras)
        
    return True  #Se nenhum failsafe foi ativado, a operação teve sucesso, mesmo que as letras não tenham sido todas repostas devido a insuficiência da pilha.


#Auxiliar
def joga_palavra(tab, palavra: str, casa, direcao: str, jog, vocab, primeira: bool) -> tuple[str, ...]:
    """
    Joga a palavra pretendida no tabuleiro. Auxiliar da função jogada_humano e jogada_agente.
    
    Caso a jogada esteja de acordo com as regras do Scrabble e os argumentos estejam corretos, a função insere a palavra jogada no tabuleiro, utilizando múltiplas funções auxiliares.
    Input:
    -tab: um tabuleiro. 
    -palavra: a palavra a ser jogada.
    -casa: a casa incial onde será jogada a palavra.
    -direcao: a direção de inserção da palavra no tabuleiro.
    -conj_letras: o conjunto de letras do jogador 
    -primeira: um booleano que indica se é a primeira jogada.
    
    Output:
    Modifica o tabuleiro, se aplicável, e retorna um tuplo, ordenado alfabeticamente, com as letras utilizadas pelo jogador.
    """
    
    #Validar as letras da palavra:
    for letra in palavra:
        if letra not in SET_LETRAS:
            return ()
    
    #Validar a casa, se a palavra cabe no tabuleiro e se a direção é aceitável
    if not eh_casa(casa):
        return ()
    
    lin, col = obtem_lin(casa), obtem_col(casa)
    
    if not (direcao == 'H' or direcao == 'V'):
        return ()  
    
    #Validar se é possível formar a palavra com as letras do conjunto do jogador no padrão do tabuleiro
    tamanho_palavra = len(palavra)
    casa_final = incrementa_casa(casa, direcao, tamanho_palavra - 1)
    padrao = obtem_padrao(tab, casa, casa_final)
    if lin == obtem_lin(casa_final) and col == obtem_col(casa_final):
        return()
    
    # Verificar se é possível formar a palavra com as letras do jogador no padrão do tabuleiro
    if not testa_palavra_padrao(vocab, palavra, padrao, jogador_letras(jog)):
        return ()
   
    #Função interna auxiliar 
    def verifica_centro_coberto(casa, direcao: str, palavra: str) -> bool:
        """
        Validar a cobertura do centro do tabuleiro na primeira jogada.
        
        Verificar se a primeira jogada cobre o centro do tabuleiro (8,8), tendo em conta os parâmetros establecidos pelo jogador.
        Args:
        -casa: tuplo que contem casa inicial onde o jogador quer colocar a palavra.
        -direcao: a direção de inserção da palavra.
        -palavra: palavra a inserir.
        
        Output:
        Booleano que identifica a cobertura do centro do tabuleiro.
        """
        
        centro = cria_casa(8,8)
        l, c = obtem_lin(casa), obtem_col(casa)
        
        #A cada iteração, avançar uma casa (próxima coluna ou linha dependendo da direção) e verificar se coincide com o centro
        for i in range(len(palavra)):
            if direcao == "H":
                casa_atual = cria_casa(l, c + i)   #Validação constante com a função cria_casa
            elif direcao == "V":
                casa_atual = cria_casa(l + i, c)
            
            if casas_iguais(casa_atual, centro):
                return True
        return False   #Se nenhuma das casas coincidiu com o centro, retorna False.
    
    if primeira:               
        if len(palavra) < 2 or not verifica_centro_coberto(casa, direcao, palavra):  #Regras especiais da primeira jogada do Scrabble
            return ()
    else:            #Validação das regras das jogadas subsequentes à primeira
        tem_letra_nova = False
        tem_letra_existente = False
        
        #Verificação de que o jogador utilizou uma letra existente no tabuleiro e pelo menos uma do seu conjunto
        #Verificar cada posição no padrão
        if '.' not in padrao or padrao.count('.') == len(padrao):
            return () 
        
        #Vericar que o jogador não está a colar palavras
        if direcao == 'H':
            if ((col > 1 and obtem_letra(tab, cria_casa(lin, col - 1)) != '.') or 
                (obtem_col(casa_final) < TAMANHO_TAB and obtem_letra(tab, cria_casa(obtem_lin(casa_final), obtem_col(casa_final) + 1)) != '.')):
                return ()
        elif direcao == 'V':
            if ((lin > 1 and obtem_letra(tab, cria_casa(lin - 1, col)) != '.') or 
                (obtem_lin(casa_final) < TAMANHO_TAB and obtem_letra(tab, cria_casa(obtem_lin(casa_final) + 1, obtem_col(casa_final))) != '.')):
                return ()

    
    #Se os args passaram todas as validações, podemos então inserir a palavra no tabuleiro
    _ = insere_palavra(tab, casa, direcao, palavra)
    
    #Verificar quais foram as letras utilizadas, subtraindo às letras da palavra as letras do padrão.
    letras_utilizadas = list(palavra)
    for c in padrao:
        if c != '.':
            letras_utilizadas.remove(c)
    
    #Transformar a lista de letras em tuplo      
    letras_utilizadas = tuple(letras_utilizadas)
    
    #Ordenar o tuplo de letras utilizadas
    tuplo_ordenado = ordenar_tuplo(letras_utilizadas)

    return tuplo_ordenado   


def jogada_humano(tab, jog, vocab, pilha: list[str]) -> bool:
    """
    Processar a jogada de um jogador humano.

    Args:
    -tab: o tabuleiro.
    -jog: o jogador.
    -vocab: o vocabulário do jogo.
    -pilha: a pilha (ou saco) de letras do Scrabble.
    
    Output:
    Booleano que indica se a jogada foi bem-sucedida (True) ou se o jogador passou a vez (False).
    """
    while True:
        
        jogada = input("Jogada {}: ".format(jogador_identidade(jog)))
        
        if not jogada:                #ignorar inputs vazios (o python considera strings vazias como falso)
            continue

        #Se a jogada for 'passar':
        if jogada == 'P':
            return False

        #Dividir os argumentos do input da jogada.
        args = jogada.strip().split()
        
        #Se a jogada não tiver letras, pedir input outra vez.
        if len(args) == 0:
            continue
        
        #Se a jogada for 'trocar', validar o input e certificar-se que a pilha tem letras suficientes, de acordo com as regras do Scrabble.
        if args[0] == 'T' and len(args) >= 2 and all(len(arg) == 1 and arg in SET_LETRAS for arg in args[1:]) and len(pilha) >= 7:
            letras_a_trocar = tuple(args[1:])
            validade_da_op = trocar_letras(jog, letras_a_trocar, pilha)
            if validade_da_op:
                return True
        
        #Se a jogada for 'jogar', é necessário validar todos os argumentos e capturar possíveis Value e index errors que podem derivar das tentativas de conversão de tipo e
        #da função cria_casa
        if args[0] == 'J' and len(args) == 5:
            
            try:
                linha = int(args[1])
                coluna = int(args[2])
                dir = args[3]
                palavra = args[4]
                casa = cria_casa(linha, coluna)

            except (ValueError, IndexError):   
                continue
            
            primeira = eh_tabuleiro_vazio(tab)
            
            letras_usadas = joga_palavra(tab, palavra, casa, dir, jog, vocab, primeira)  
            
            if letras_usadas:          
                soma_pontos(jog, obtem_pontos(vocab, palavra)) 
                
                #Remover as letras utilizadas do conjunto do jogador e distribuir novas
                _ = trocar_letras(jog, letras_usadas, pilha)
                
                n_let_jogador = len(jogador_letras(jog))
                
                if n_let_jogador < 7 and len(pilha) > 0:
                    distribui_letras(jog, pilha, 7 - n_let_jogador) #Repor as letras do jogador até 7 novamente

                return True 


def jogada_agente(tab, jog, vocab, pilha) -> bool:
    """
    Processar a jogada de um agente.
    
    Args:
    -tab: o tabuleiro.
    -jog: o jogador (agente).
    -vocab: o vocabulário do jogo.
    -pilha: a pilha (ou saco) de letras do Scrabble.
    Output:
    Booleano que indica se a jogada foi bem-sucedida (True) ou se o agente passou a vez (False).
    """
    
    nivel = jogador_identidade(jog)
    
    #Passar se é a primeira jogada
    if eh_tabuleiro_vazio(tab):
        print(f'Jogada {nivel}: P')
        return False
    
    letras_jogador = jogador_letras(jog)
    n_letras = len(letras_jogador)

    padroes, casas, dirs = gera_todos_padroes(tab, n_letras)

    if nivel == 'FACIL':
        N = 100
    elif nivel == 'MEDIO':
        N = 50
    elif nivel == 'DIFICIL':
        N = 10

    padroes_filtrados = padroes[::N]
    casas_filtradas = casas[::N]
    dirs_filtradas = dirs[::N]

    melhor_palavra = ''
    melhor_pts = 0
    melhor_casa = None
    melhor_dir = None

    for padrao, casa, dir in zip(padroes_filtrados, casas_filtradas, dirs_filtradas):
        pal, pts = procura_palavra_padrao(vocab, padrao, letras_jogador, melhor_pts)

        if pal and pts > melhor_pts:
            melhor_palavra, melhor_pts, melhor_casa, melhor_dir = pal, pts, casa, dir
    
    # Se encontrou palavra a jogar:
    if melhor_palavra:
        print(f"Jogada {nivel}: J {obtem_lin(melhor_casa)} {obtem_col(melhor_casa)} {melhor_dir} {melhor_palavra}")
        
        primeira = eh_tabuleiro_vazio(tab)
        letras_usadas = joga_palavra(tab, melhor_palavra, melhor_casa, melhor_dir, jog, vocab, primeira)
        if letras_usadas:
            # Atualiza pontos e troca letras usadas
            soma_pontos(jog, obtem_pontos(vocab, melhor_palavra))
            _ = trocar_letras(jog, letras_usadas, pilha)
        return True
    
    #Se não encontrou palavra para jogar
    if len(pilha) >= 7:
        letras_a_trocar = tuple(jogador_letras(jog))
        validade = trocar_letras(jog, letras_a_trocar, pilha)
        if validade:
            # imprime as letras trocadas no mesmo formato: separadas por espaço
            print(f"Jogada {nivel}: T " + " ".join(letras_a_trocar))
            return True
        else:
            # se por alguma razão não pôde trocar, passa
            print(f"Jogada {nivel}: P")
            return False

    else:
        # Não há letras suficientes para trocar -> passa
        print(f"Jogada {nivel}: P")
        return False


def scrabble2(jogadores: tuple[str, ...], nome_fich: str, seed: int) -> tuple[int, ...]:
    """
    Função principal do jogo Scrabble2.
    
    Args:
    -jogadores: tuplo com os nomes dos jogadores (strings). Se o nome começar com '@', o jogador é um agente.
    -nome_fich: nome do ficheiro (string) que contém o vocabulário do jogo.
    -seed: valor inteiro positivo para inicializar o gerador de números pseudo-aleatórios.
    
    Output:
    Tuplo com as pontuações finais de cada jogador, na ordem em que foram passados os nomes dos jogadores.
    """
    #------------Validação de argumentos: tipo e valor, de acordo com as regras do Scrabble.------------
    if (not isinstance(jogadores, tuple) or
        not (2 <=len(jogadores) <= 4) or    #O jogo é jogado com 2 a 4 jogadores
        not all(isinstance(jog, str) for jog in jogadores) or
        not isinstance(nome_fich, str) or
        len(nome_fich) == 0 or 
        not type(seed) == int or seed <= 0):  #A seed tem que ser inteira e positiva 
        raise ValueError("scrabble2: argumentos inválidos")
    
    #Ficheiro tem que existir e ser possível de ler
    try:
        file = open(nome_fich, 'r', encoding='utf-8') 
        file.close()
    except (FileNotFoundError, IOError):
        raise ValueError("scrabble2: argumentos inválidos")

    
    #Inicialização do jogo
    tab = cria_tabuleiro()  #Criação do tabuleiro
    print("Bem-vindo ao SCRABBLE2.")  #Impressão da mensagem de Boas-vindas
    vocab = ficheiro_para_vocabulario(nome_fich)
    pilha = baralha_saco(seed)  #Criação e permutação da pilha de letras
    lista_jogadores = []  #Criação da lista de jogadores
    
    for nome in jogadores:
        if nome[0] == '@':
            try:
                lista_jogadores.append(cria_agente(nome[1:]))
            except ValueError:
                raise ValueError("scrabble2: argumentos inválidos")
        else:
            try:
                lista_jogadores.append(cria_humano(nome))
            except ValueError:
                raise ValueError("scrabble2: argumentos inválidos")

    for jogador in lista_jogadores:
        distribui_letras(jogador, pilha, 7)
    
    #Controlo do jogo
    jogo_terminado = False   
    primeira_jogada = True   
    passes_consecutivos = 0  

    #Execution loop principal do jogo
    while not jogo_terminado:   #Corre enquanto as condições de término de jogo não forem atingidas
        for jogador_atual in lista_jogadores:
            if jogo_terminado:   #Verifica a cada turno de cada jogador se as condições de término foram atingidas, acabando o jogo de imediato.
                break
            
            #Exibir o estado do jogo (estado do tabuleiro, pontuação dos jogadores e letras na posse de cada jogador)
            print(tabuleiro_para_str(tab))
            for j in lista_jogadores:
                print(jogador_para_str(j))
            
            #Permitir a jogada
            if eh_agente(jogador_atual):
                jogada = jogada_agente(tab, jogador_atual, vocab, pilha)
            elif eh_humano(jogador_atual):
                jogada = jogada_humano(tab, jogador_atual, vocab, pilha)
        
            if not jogada:   
                passes_consecutivos += 1
            
            if jogada:       
                passes_consecutivos = 0   #Fazer o reset dos passes consecutivos
                primeira_jogada = False   #Se chegar a esta condição, significa que esta é a primeira jogada ou jogadas posteriores

            #Condições de término
            if len(pilha) == 0 and len(jogador_letras(jogador_atual)) == 0:  
                break
            if passes_consecutivos >= len(lista_jogadores): #Verificar se todos os jogadores passaram a vez
                jogo_terminado = True
                break  
    
    #Se as condições de término foram atingidas, o execution loop parou e podemos retornar as pontuações finais
    return tuple([jogador_pontos(jogador) for jogador in lista_jogadores])  









# Script para dividir o arquivo 'fasta', de forma a igualar o proces-
#   samento entre os nucleos (max de 20)

# Nome do arquivo a ser processado abaixo, associado a esta variavel

proteins_fasta = 'GCF_000240185.1_ASM24018v2_protein'

new_file = open(proteins_fasta + '.txt', 'w')

# Numero de divisoes para a proteina ser processada

num_divisions = 20

# Funcao para ler um arquivo, recebendo o nome do arquivo como entrada

def read_file(filename):
    fasta_file = open(filename + '.faa')
    return fasta_file

# Funcao que recebe um arquivo como entrada, e retorna uma lista com
#   os cabecalhos e proteinas

def save_splitted(fasta_file):

# Declaracao de uma lista vazia, onde vao ser inseridos os cabecalhos
#   com sua respectiva sequencia em seguida. Modelo de lista abaixo:
#   ['cabecalho_1', 'sequencia1', 'cabecalho_2', 'sequencia_2'] ...

    splitted_elements = []

# Leitura do arquivo e atribuicao de cada linha do arquivo a um elemen-
#   to de uma lista

    lines = fasta_file.readlines()

# 'element' eh uma variavel que ira armazenar cada elemento da lista
#   final. Caso a linha inicie com '>', significa que o elemento em
#   questao eh um cabecalho. Caso nao, significa que o elemento eh uma
#   proteina, portanto, deve-se concatenar cada linha de proteina ate
#   que se encontre uma linha de cabecalho

    element = ""
    for line in lines:

# Neste if, caso ele encontre uma linha com um cabecalho, como ele ja
#   concatenou as linhas de proteina, ele vai anexar a lista a protei-
#   na concatenada, e depois vai anexar a linha com o cabecalho. Apos
#   isso, vai zerar o elemento para que ele passe a concatenar a proxi-
#   ma proteina ate que o proximo cabecalho chegue.

        if line[0] == ">":
            splitted_elements.append(element)
            splitted_elements.append(line.strip())
            element = ""
        else:
            element += line.strip()

# Aqui ele anexa a ultima proteina, e remove o primeiro termo, que eh
#   sempre um "", e depois retorna a lista

    splitted_elements.append(element)
    splitted_elements.pop(0)
    return splitted_elements

# proteins eh uma lista contendo apenas as proteinas, sem seus devidos
#   cabecalhos no indice anterior, lista essa criada para se obter o
#   numero total de aminoacidos

# Esta formatacao ([1::2]) indica apenas as posicoes impares da lista

def proteins(complete_list):

    proteins_list = complete_list[1::2]
    return proteins_list


# A funcao total_size recebe uma lista ja pre-formatada com cabecalhos
#   e proteinas e retorna o numero total de aminoacidos contida nela

def total_size(proteins_list):

    size = 0

# Este laco percorre cada elemento da lista de proteinas, e em cada um,
#   incrementa o numero de aminoacidos

    for element in proteins_list:
        size += len(element)

    return size

# A funcao division recebe como parametro uma lista contendo as prote-
#   inas em sequencia e recebe tambem a quantidade total de aminoacidos
#   do arquivo. Alem disso, utiliza tambem a variavel num_divisions,
#   que corresponde ao numero de divisoes que o arquivo deve ser parti-
#   cionado para ser processado

def division(proteins_list, size):

# A variavel partition_size eh a quantidade de aminoacidos que cada
#   particao, em media, deve ter, e não ira passar desse valor

    partition_size = int(size / num_divisions)

# A variavel partial_size eh o valor de comparacao a ser feito com a
#   posicao atual (inicia em 0 e vai incrementando o tamanho de cada
#   aminoacido que percorre)

    partial_size = 0

# A variavel count eh a posicao ordinal da particao, contada como in-
#   dice de uma lista (sendo 0 a primeira posicao), e utilizada como
#   fator multiplicador do tamanho da particao

    count = 0

# A variavel partition eh a posicao atual de busca do tomanho ideal das
#   divisoes. A cada ponto de encontro (onde eh definido o tamanho ide-
#   al da particao, o valor da variavel partition eh incrementado com
#   o valor da particao, para que seja encontrado o novo ponto de
#   encontro)

    partition = partition_size

# Loop que percorre toda a cadeia de proteinas, analisando cada protei-
#   na, e se ja chegou no tamanho ideal

    for element in proteins_list:

# if para definir se ja chegou no tamanho ideal (se o numero de amino-
#   acidos contado ate agora ultrapassou o numero ideal da particao)

        if(partial_size > partition):

# A proxima linha volta para o inicio desta proteina

            position = partition - partial_size

# No proximo if, eh feita uma analise se deve ou nao incluir a proteina
#   avaliada nesta posicao, ou seja, se o ponto de encontro esta antes
#   ou depois da metade dela



            if(position <= (len(element)/2)):
                print(proteins_list[proteins_list.index(element) - 1])
                print(proteins_list.index(element) - 1)
                new_file.write('Partition number ')
                new_file.write(str(count+1))
                new_file.write(' finishes in ')
                new_file.write(str(proteins_list[proteins_list.index(element) - 1]))
                new_file.write('\n')
            else:
                print(element)
                print(proteins_list.index(element))
                new_file.write('Partition number ')
                new_file.write(str(count+1))
                new_file.write(' finishes in ')
                new_file.write(str(proteins_list[proteins_list.index(element) - 1]))
                new_file.write('\n')
            count += 1
            partition = partition_size * (count+1)
            if (count == num_divisions-1):
                break

        partial_size += len(element)


# fasta_file eh uma variavel do tipo arquivo que ira ler o arquivo a
#   ser trabalhado

fasta_file = read_file(proteins_fasta)

# splitted_elements eh a lista contendo os cabecalhos e proteinas

splitted_elements = save_splitted(fasta_file)

proteins_list = proteins(splitted_elements)

# amino_acids eh a quantidade total de aminoacidos do arquivo

amino_acids = total_size(proteins_list)

print (amino_acids)

new_file.write('Number of aminoacids = ')
new_file.write(str(amino_acids))
new_file.write('\n')

division(proteins_list, amino_acids)

fasta_file.close()

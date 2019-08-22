## \ |

# Importacao da biblioteca para trabalhar com expressões regulares
import re

# Nome do arquivo que contem a proteina a ser avaliada
filename = 'Tc04_g018130'


def main(filename):

    # Funcao clean_initial_lines desenvolvida para limpar as primeiras
    #   linhas de registro vazias e deixar o indice da lista correspon-
    #   dente a posicao na lista

    def clean_initial_lines(lists):

        for element in lists:

            if element:
                start_index = lists.index(element) - 1
                break

        lists = lists[start_index:]

        return lists

    # Funcao split_regions criada para dividir a lista a ser trabalhada,
    #   transformando-a em uma lista de listas, em que cada lista inter-
    #   na possui uma regiao desordenada

    def split_regions(lists):

        new_list = []
        division = 0
        i = 1

        # print (lists)

        for i in range(len(lists)):
            # print ('iteracao ')
            # print(i)
            # print(new_list)
            if not lists[i]:

                #if (lists[division+1 : i]):
                new_list.append(lists[division+1 : i])

                division = i

                # print(division)

        if lists[-1]:
            new_list.append(lists[division+1:])
            # print (lists[-1])


        newer_list = list(filter(lambda element: (element != []), new_list))
        return newer_list


    def remove_small_residues(lists):

        for element in lists:

            if len(element) < 3:

                # print(element)

                lists.remove(element)

        for element in lists:

            if len(element) < 3:

                # print(element)

                lists.remove(element)

        return lists

    def save_file(filename, divided_list):

        new_file = open(filename + '.txt', 'w')
        short_residues = 0
        long_residues = 0

        for element in divided_list:

            new_file.write(str(element[0]))
            new_file.write(' - ')
            new_file.write(str(element[-1]))
            new_file.write(' = ')
            new_file.write(str(len(element)))
            new_file.write('\n')


            if len(element) < 31:

                long_residues = long_residues + 1

            else:

                short_residues = short_residues + 1

        new_file.write('\n')
        new_file.write('Long residues = ')
        new_file.write(str(long_residues))
        new_file.write('\n')
        new_file.write('Short residues = ')
        new_file.write(str(short_residues))
        new_file.close()



    # Execucao da expressao regular no arquivo .diso, com a finalidade
    #   de transformar o arquivo em uma lista, com cada posicao corres-
    #   pondente a posicao no arquivo, ou seja, se a posicao existir na
    #   lista, ela e um residuo desordenado
    diso_lines = [re.findall("[0-9]+(?=[ ][A-Z][ ][\*])", line)
      for line in open(filename + '.diso')]

    diso_lines = clean_initial_lines(diso_lines)
    # print ('lista completa: ', diso_lines)
    diso_divided = split_regions(diso_lines)
    # print ('lista dividida: ', diso_divided)
    diso_divided2 = remove_small_residues(diso_divided)

    # print ('lista dividida: ')
    # print (diso_divided2)

    save_file(filename, diso_divided2)

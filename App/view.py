"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


playersfile = 'FIFA//fifa-players-2022-utf8-small.csv'
cont = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________
def newAnalyzer():
    """
    Se crea una instancia del controlador
    """
    analyzer = controller.init()
    return analyzer

analyzer = newAnalyzer()

def printInfoplayer(playerList):
    """
    Imprime los mejores libros solicitados
    """
    size = lt.size(playerList)
    contador = 1

    if size:
        print('Esta es la información de los últimos 5 jugadores: ')
        for player in lt.iterator(playerList):
            print('\n' + '\n---------------------------------------------' + '\nJugador #' + str(contador)
            + '\nFecha de entrada: ' + player['club_joined'] + '\nNombre: ' + player['short_name'] + 
            '\nEdad: ' + player['age'] + '\nFecha nacimiento: ' + player['dob']
            + '\n======================='
            + '\nDesempeño: ' + player['overall']
            + '\nNacionalidad: ' + player['nationality_name'] + '\nPrecio: € ' + player['value_eur'] + '\nSalario: € ' + player['wage_eur']
            + '\nPrecio de terminación: € ' + player['release_clause_eur'] + '\nFecha límite del contrato: ' + player['club_contract_valid_until']
            + '\nPosición del jugador: ' + player['player_positions'] + '\nPosición el el club: ' + player['club_position'] + '\nTags: ' + player['player_tags']
            + '\nCaracterísticas del jugador: ' + player['player_traits']  
            + '\n---------------------------------------------')
            contador = contador+1
    else:
        print("ERROR")


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de jugadores")
    print("3- Consultar últimos 5 jugadores en unirse a un club")
    print("8- Consultar jugadores por rango salarial y tag")
    print("9- Consultar histograma")
    print("0- Salir")
    print("*******************************************")

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de jugadores ....")
        controller.loadData(cont, playersfile)
        print('Jugadores cargados: ' + str(controller.playerSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        inputs2 = input("\nIntroduzca el nombre del club: ")
        playerList = controller.getLastFiveAdquisitions(controller.getPlayersByClubName(cont, inputs2))
        printInfoplayer(playerList)
        

    elif int(inputs[0]) == 8:
        input1 = input("\nIntroduzca el salario mínimo: ")
        input2 = input("\nIntroduzca el salario máximo: ")
        input3 = input("\nIntroduzca el tag a buscar: ")
        playerList1 = controller.getPlayersByWageRange(controller.getPlayersByTag(cont, input3), input2, input1)
        printInfoplayer(playerList1)
    elif int(inputs[0]) == 9:
        input11 = input("\nSeleccione un atributo: \n1. Overall\n2. Potential\n3. value_eu\n4. wage_eur\n5. height_cm\n6. weight_cm\n7. release_clause_eur\n\nIntroduzca el numero de atributo: ")
        input12 = input("\nIntroduzca cuantos jugadores por marca: ")
        input13 = input("\nIntroduzca el número de segmentos: ")
        controller.graphHistogramByParameter1(cont, input12, input13, input11)

    else:
        sys.exit(0)
sys.exit(0)

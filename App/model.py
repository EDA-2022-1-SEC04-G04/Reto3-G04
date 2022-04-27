"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from sys import dont_write_bytecode
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los jugadores
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'players': None,
                'dateIndex': None}
          

    analyzer['players'] = lt.newList('ARRAY_LIST', compareIds)
    analyzer['index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    #analyzer['clubName'] = lt.newList('SINGLE_LINKED', compareClubNames""")
    return analyzer

# Funciones para agregar informacion al catalogo
def addPlayer(analyzer, player):
    """
    """
    lt.addLast(analyzer['players'], player)
    updateIndex(analyzer['index'], player)
    return analyzer


def updateIndex(map, player):
    """
    Se toma el sofifa_id y se busca si ya existe en el arbol
    dicho id.  Si es asi, se adiciona a su lista de jugadores
    y se actualiza el indice de tipos de jugadores.

    Si no se encuentra creado un nodo para ese id en el arbol
    se crea y se actualiza el indice de tipos de jugadores
    """
    
    playerid = player['sofifa_id']
    entry = om.get(map, int(playerid))
    if entry is None:
        datentry = newDataEntry(player)
        om.put(map, int(playerid), datentry)
    else:
        datentry = me.getValue(entry)
    addIndex(datentry, player)
    return map


def addIndex(datentry, player):
    """
    Actualiza un indice de tipo de jugadores.  Este indice tiene una lista
    de jugadores y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los jugadores de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstclubs']
    lt.addLast(lst, player)
    offenseIndex = datentry['offenseIndex']
    offentry = m.get(offenseIndex, player['club_name'])
    if (offentry is None):
        entry = newOffenseEntry(player['club_name'], player)
        lt.addLast(entry['lstoffenses'], player)
        m.put(offenseIndex, player['club_name'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], player)
    return datentry


def newDataEntry(player):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'offenseIndex': None, 'lstclubs': None}
    entry['offenseIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses)
    entry['lstclubs'] = lt.newList('SINGLE_LINKED', compareDatesJoined)
    return entry


def newOffenseEntry(offensegrp, player):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = lt.newList('SINGLE_LINKED', compareOffenses)
    return ofentry

# Funciones para creacion de datos

# Funciones de consulta
def playersSize(analyzer):
    """
    Número de jugadpres
    """
    return lt.size(analyzer['players'])

def clubsSize(analyzer):
    return lt.size(analyzer['clubName'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['index'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['index'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['index'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['index'])

def newPlayer(id, name, clubName, dateClubJoined, age, dob, shortName, overall,
                nationality, valueEUR, wageEUR, releaseEUR, validUntil, position, clubPos,
                tags, traits):
    player = {'name': '', 'sofifa_id': '', 'club_name': '' , 'club_joined': '', 'age':'', 
        'dob':'','short_name':'','overall':'','nationality_name':'','value_eur':'',
        'wage_eur':'','release_clause_eur':'','club_contract_valid_until':'','player_position':'','club_position':'',
        'player_tags':'','player_traits':''}

    player['sofifa_id']= id
    player['name']= name
    player['club_name']= clubName
    player['club_joined']= dateClubJoined
    player['age'] = age
    player['dob'] = dob
    player['short_name'] = shortName
    player['overall'] = overall
    player['nationality_name'] = nationality
    player['value_eur'] = valueEUR
    player['wage_eur'] = wageEUR
    player['release_clause_eur'] = releaseEUR
    player['club_contract_valid_until'] = validUntil
    player['player_position'] = position
    player['club_position'] = clubPos
    player['player_tags'] = tags
    player['player_traits'] = traits
    
    return player

def getPlayersByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['index'], initialDate, finalDate)
    totclubs = 0
    for lstdate in lt.iterator(lst):
        totclubs += lt.size(lstdate['lstclubs'])
    return totclubs


def getPlayersByRangeCode(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    crimedate = om.get(analyzer['index'], initialDate)
    if crimedate['key'] is not None:
        offensemap = me.getValue(crimedate)['offenseIndex']
        numoffenses = m.get(offensemap, offensecode)
        if numoffenses is not None:
            return m.size(me.getValue(numoffenses)['lstoffenses'])
    return 0

def getPlayersByClubName(analyzer, nameOfClub):
    
    """
    Retorna los 5 jugadores más recientemente vinculados al club
    """

    players = analyzer['players']
    listSize = lt.size(players)
    returnedList = lt.newList()
    counter = 1

    nombreClub = str(nameOfClub)
    for counter in range(1, listSize):
        ele1 = lt.getElement(players, counter)
        #print('\nNombre del club: ' + ele1['club_name'])
        #lt.addLast(returnedList, ele1)
        
        if str(ele1['club_name']) == nombreClub:
            print('\nExitoso!!!!!!!!')
            eleAdd = lt.getElement(players, counter)
            lt.addLast(returnedList, eleAdd)
        else:
            print('\nNo se cumple el if')   
       

    #sa.sort(returnedList, compareDatesJoined)
   
    return returnedList

def getLastFiveAdquisitions(listClub):

    listSize = lt.size(listClub)
    lastFivePlayers = lt.newList()
    for i in range(listSize-4, listSize+1):
        player = lt.getElement(listClub, i)
        lt.addFirst(lastFivePlayers, player)
    
    return lastFivePlayers


# Funciones utilizadas para comparar elementos dentro de una lista
def compareIds(id1, id2):
    """
    Compara dos jugadores
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDatesJoined(player1, player2):
    return (int(str(player1['club_joined'][0:4])) < int(str(player2['club_joined'][0:4])))

def compareDates(date1, date2):
    
    if (date1 == date2):
        return 0
    else:
        return -1

def compareClubNames(clubName, club):
    if (clubName == club['club_name']):
        return 0
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos tipos de jugadores
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1
# Funciones de ordenamiento

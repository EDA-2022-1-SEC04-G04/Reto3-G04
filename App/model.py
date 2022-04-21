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
                'dateIndex': None
                }

    analyzer['players'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['index'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
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
    entry['lstclubs'] = lt.newList('SINGLE_LINKED', compareDates)
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
    Número de crimenes
    """
    return lt.size(analyzer['players'])


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


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
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

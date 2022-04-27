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
 """

import config as cf
from App import model
import model
import csv
import datetime


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer
    
# Funciones para la carga de datos

def loadData(analyzer, playersfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    playersfile = cf.data_dir + playersfile
    input_file = csv.DictReader(open(playersfile, encoding="utf-8"),
                                delimiter=",")
    for player in input_file:
        model.addPlayer(analyzer, player)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def playerSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.playersSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def getPlayersByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getPlayersByRange(analyzer, initialDate.date(),
                                  finalDate.date())


def getPlayersByRangeCode(analyzer, initialDate,
                         offensecode):
    """
    Retorna el total de crimenes de un tipo especifico en una
    fecha determinada
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    return model.getPlayersByRangeCode(analyzer, initialDate.date(),
                                      offensecode)

def getPlayersByClubName(analyzer, nameOfClub):

    return model.getPlayersByClubName(analyzer, nameOfClub)

def getLastFiveAdquisitions(listClub):

    return model.getLastFiveAdquisitions(listClub)
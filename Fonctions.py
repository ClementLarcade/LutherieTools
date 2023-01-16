import numpy as np
import json
from codecs import open
from functools import wraps
from os import mkdir
from copy import copy

from Classes import Matrices



""""
Ester : calculer la matrice U depuis ESPRIT
puis en fonction d'une variable de choix d'algo d'estimation 
appeler ESTER depuis ESPRIT en fournissant U

retourner J en sortie de ESPRIT

de manière générale : appeler l'algo d'estimation depuis ESPRIT
""" 

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
            
        return cache[key]

    return wrapper 

def export(matrices: Matrices, exportfolder: str) -> None:

    mkdir("exports/" + exportfolder)
    exportJson(matrices.F, "exports/" + exportfolder + "/F.json")
    exportJson(matrices.BdBSeuil, "exports/" + exportfolder + "/B.json")
    exportJson(matrices.Ksi, "exports/" + exportfolder + "/Ksi.json")
    exportJson(matrices.J, "exports/" + exportfolder + "/J.json")
    exportJson(matrices.T, "exports/" + exportfolder + "/T.json")

    
    return

def exportJson(mat: np.ndarray, file_path: str) -> None:
    """
    Pour exporter les matrices résultats sous forme de fichier .json

    Args:
        mat (np.ndarray): La matrice à exporter
        file_path (str): Le chemin où exporter
    """    
    matList = mat.tolist()# nested lists with same data, indices
    
    json.dump(matList, 
            open(file_path, 'w', encoding='utf-8'), 
            separators=(',', ':'), 
            sort_keys=True, 
            indent=4) ### this saves the array in .json format
    
    return 

def seuil(inputarray: np.ndarray, seuil: float) -> np.ndarray:
    
    outpoutarray: np.ndarray = copy(inputarray)    
    
    for (i,j), x in np.ndenumerate(inputarray):
        if x < seuil:
            outpoutarray[i,j] = -200
        else:
            outpoutarray[i,j] = x
            
    return outpoutarray
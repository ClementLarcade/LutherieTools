import numpy as np
import json
from codecs import open
from functools import wraps
from os import mkdir

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

    """
    pour matrices.F, si f == NaN : f = -1000
    pour matrices.BdBSeuil, si b == NaN : b = nanmin(dBSeuil) et f = -1000
    pour matrices.Ksi, si ksi == Nan : ksi = 0 
    """

    deNaNination(matrices)

    matricesDict: dict = {
        "F" : matrices.F.tolist(),
        "B" : matrices.BdBSeuil.tolist(),
        "Ksi" : matrices.Ksi.tolist(),
        "T" : matrices.T.tolist()
    }

    filePath = "exports/" + exportfolder + "/matrices.json"
    
    mkdir("exports/" + exportfolder)

    json.dump(matricesDict, 
            open(filePath, 'w', encoding='utf-8'), 
            separators=(',', ':'), 
            sort_keys=True, 
            indent=4) ### this saves the array in .json format


    # exportJson(matrices.F, "exports/" + exportfolder + "/F.json")
    # exportJson(matrices.BdBSeuil, "exports/" + exportfolder + "/B.json")
    # exportJson(matrices.Ksi, "exports/" + exportfolder + "/Ksi.json")
    # exportJson(matrices.J, "exports/" + exportfolder + "/J.json")
    # exportJson(matrices.T, "exports/" + exportfolder + "/T.json")

    
    return


def deNaNination(matrices: Matrices):

    for index, frequence in np.ndenumerate(matrices.F):

        if frequence is np.NaN: 
            matrices.F = -1000

        if matrices.BdBSeuil[index] is np.NaN: 
            matrices.dBSeuil[index] = np.nanmin(matrices.dBSeuil)
            matrices.F[index] = -1000
            
        if matrices.Ksi[index] is np.NaN:            
            matrices.Ksi[index] = 0
        
        matrices.Ksi[:, 0] = np.zeros_like(matrices.Ksi[:,0])
            
    return


def exportJson(mat: np.ndarray, file_path: str) -> None:
   
    matList = mat.tolist()# nested lists with same data, indices
    
    json.dump(matList, 
            open(file_path, 'w', encoding='utf-8'), 
            separators=(',', ':'), 
            sort_keys=True, 
            indent=4) ### this saves the array in .json format
    
    return 



def seuil(matrices: Matrices, seuil: float) -> np.ndarray:
    
    matrices.BdBSeuil = np.zeros_like(matrices.BdB)
    
    
    
    for (i,j), x in np.ndenumerate(matrices.BdB):
        if x < seuil:
            matrices.BdBSeuil[i,j] = -200
        else:
            matrices.BdBSeuil[i,j] = x
            
    
            
    return 
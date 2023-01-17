import numpy as np
import json
from codecs import open
from os import mkdir, path

from Classes import Matrices


""""
Ester : calculer la matrice U depuis ESPRIT
puis en fonction d'une variable de choix d'algo d'estimation 
appeler ESTER depuis ESPRIT en fournissant U

retourner J en sortie de ESPRIT

de manière générale : appeler l'algo d'estimation depuis ESPRIT
""" 

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
    exportdir: str= "exports/" + exportfolder

    if not path.isdir(exportdir):
        mkdir(exportdir)

    print(filePath)
    json.dump(matricesDict, 
            open(filePath, 'w', encoding='utf-8'), 
            separators=(',', ':'), 
            sort_keys=True, 
            indent=4) ### this saves the array in .json format

    return


def deNaNination(matrices: Matrices):

    for index, frequence in np.ndenumerate(matrices.F):

        if matrices.BdBSeuil[index] == -200: 
            matrices.F[index] = -1000
            
        if matrices.Ksi[index] is np.NaN:            
            matrices.Ksi[index] = 0
        
        matrices.Ksi[:, 0] = np.zeros_like(matrices.Ksi[:,0])
            
    return


def seuil(matrices: Matrices, seuil: float) -> np.ndarray:
    
    matrices.BdBSeuil = np.zeros_like(matrices.BdB)
    
    for (i,j), x in np.ndenumerate(matrices.BdB):
        if x < seuil:
            matrices.BdBSeuil[i,j] = -200
        else:
            matrices.BdBSeuil[i,j] = x
            
    return 
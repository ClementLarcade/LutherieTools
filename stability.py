import numpy as np
from copy import copy

def stability(inMatrix: np.ndarray, numcolstoverify: int, tolerance: float) -> np.ndarray:
    
    modesValides = []
    (numrows, numcols) = inMatrix.shape
    outMatrix = copy(inMatrix)

    for (row, col), mode in np.ndenumerate(inMatrix):

        if mode in modesValides: 
            continue 

        elif ((numcols - col) > numcolstoverify and 
            isValid(mode, inMatrix[:, (col+1):numcolstoverify], tolerance)):

            modesValides.append(mode)
            
        else:
            outMatrix[row, col] = -1000


    return outMatrix


def isValid(value: float, colstoverify: np.ndarray, tolerance: float) -> bool:

    numcols: int = colstoverify.shape[1]
    numofvalidcols: int = 0

    for col in range(numcols):

        if isInInterval(value, colstoverify[:, col], tolerance):
            numofvalidcols += 1

    return numofvalidcols == numcols

    
def isInInterval(value: float, vector: np.ndarray, tolerance: float) -> bool:

    result: bool = False

    for _, vectorelem in np.ndenumerate(vector):
        if (value >= vectorelem - tolerance and 
            value <= vectorelem + tolerance):

            result = True

    return result
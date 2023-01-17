import numpy as np

class Params:

    def __init__(self) -> None:
        self.samplerate: int = 0
        self.horizon: float = 0.
        self.overlap: float = 0.
        self.nbPoles: int = 0
        self.exportfolder: str = ""


class Matrices:

    def __init__(self) -> None:
        self.F: np.ndarray = np.array([])        
        self.FStable: np.ndarray = np.array([])        

        self.B: np.ndarray = np.array([])
        self.BdB: np.ndarray = np.array([])
        self.BdBSeuil: np.ndarray = np.array([])

        self.Ksi: np.ndarray = np.array([])
        self.J: np.ndarray = np.array([])  
        self.T: np.ndarray = np.array([])  





        


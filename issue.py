from dataclasses import dataclass

@dataclass
class Issue:
    numero: int = 0
    resume: str = ""
    statut: str = None
    version_ciblee: str = None
#    date_creation: str = None
    categorie_MOA: str = None
    valeur_metier: int = None
    charge: int = None
    priorite_MOA: str =None
    groupe: str = None

    def update(self, issue):
        for k in self.__dict__:
            newValue = issue.__dict__.get(k,None)
            if newValue is None:
                continue
            self.__dict__[k] = newValue
"""
    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        print(value)
        self._numero = int(value)
"""
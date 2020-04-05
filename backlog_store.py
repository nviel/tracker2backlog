import ezodf
from issue import Issue
import shutil

# correspondance entre les champs de la classe Issue et les colonnes de ods.
COL_POS = {
    "priorite_MOA" :0,
    "charge" : 1,
    "valeur_metier" : 2,
    "numero" : 3,
    "categorie_MOA" :4,
    "statut" :5,
    "version_ciblee" :6,
    "resume" :7,
    "groupe" : 8
    }

def loadBackLog(odsFilePath):
    ods = ezodf.opendoc(odsFilePath)

    sheet = ods.sheets[0]
    print(sheet.ncols(), sheet.nrows())

    backlog = []
    # lecture des données
    # La première ligne ne contient que les noms des colonnes et n'est pas lue.
    for row_idx in range(1, sheet.nrows()):
        values = [sheet[row_idx, col].value for col in range(len(COL_POS))]
        if all(v is None for v in values):
            # si cette ligne ne contient pas de valeur on ne la prend pas
            continue
        params = {}
        issue = Issue()
        for k in issue.__dict__.keys():
            if k == "numero":
                # convert from float
                issue.__dict__[k] = int(values[COL_POS[k]])
            else:
                issue.__dict__[k] = values[COL_POS[k]]
        backlog.append(issue)
        #print(backlog[-1])
    return backlog


def saveBackLog(backlog, destFilePath, TemplateFilePath = 'template.ods'):
    # TODO: créer le nouveau fichier en copiant le template ou créer un document vide si le template n'existe pas.
    # TODO: Ouvrir le nouveau fichier et y copier le backlog
    shutil.copyfile(TemplateFilePath, destFilePath)
    ods = ezodf.opendoc(destFilePath)

    sheet = ods.sheets[0]
    sheet.insert_rows(1, len(backlog))
    for (row_idx, issue) in enumerate(backlog, 1):
        for k in issue.__dict__.keys():
            if issue.__dict__[k] is not None:
                sheet[row_idx, COL_POS[k]].set_value(issue.__dict__[k])

    ods.save()

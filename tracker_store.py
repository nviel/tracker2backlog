from issue import Issue
import csv

COL_POS = {
    "numero" : 0,
    "resume" :1,
    "statut" :2,
    "version_ciblee" :3
    }

def loadTrackerIssues(filePath):
    """les données du tracker sont stockées dans un dict parce que c'est plus pratique pour les recherches"""
    issues = {}
    with open(filePath,"r", encoding='utf8') as trackFile:
        r = csv.reader(trackFile, delimiter=",", quotechar='"')
        # Rq: le reader ne détecte pas bien la fin de ligne en \r\n et laisse le \r dans la dernière valeur  la ligne...
        # supprimer la première ligne.
        next(r)
        for row in r:
            issue = Issue()
            for k in issue.__dict__.keys():
                if k in COL_POS:
                    if k == 'numero':
                        issue.__dict__[k] = int(row[COL_POS[k]])
                    else:
                        issue.__dict__[k] = row[COL_POS[k]]
            issues[int(row[COL_POS["numero"]])] = issue

    return issues
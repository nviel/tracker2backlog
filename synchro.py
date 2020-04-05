"""
En entrée:
- le fichier csv issu de mantis
- le fichier ods issu de libreoffice calc avec les chiffrage et priorisation.
En sortie:
- le fichier ods mis à jour des nouveautées de mantis et conservant les saisies faites dans calc

TODO: que faire des tickets ajoutés?
Pour le moment ils sont ajouté à la fin mais:
- ils pourraient être ajouté dans un onglet "non priorisé
- lorsqu'ils ont une version ils devraient être positionnés à la fin des tickets portant cette version.

Les tickets supprimés pourraient être placé dans un onglet "terminés"
"""


from issue import Issue
from backlog_store import loadBackLog, saveBackLog
from tracker_store import loadTrackerIssues

def updateBackLog(backLog, tracker):
    # Suppression des tickets du tracker dont le statut est fermé ou résolu.
    filteredTracker = {}
    for (k,v) in tracker.items():
        if v.statut in (SOLVED, CLOSED):
            continue
        filteredTracker[k] = v
    tracker = filteredTracker

    newBackLog = []
    for issue in backLog:
        if issue.numero not in tracker:
        # suppression des tickets fermés dans le backLog
            continue
        # mise à jour des tickets existants
        issue.update(tracker[issue.numero])
        newBackLog.append(issue)
        del tracker[issue.numero]

    # ajout dans le backLog des nouveaux tickets restant dans le tracker
    for issue in tracker.values():
        newBackLog.append(issue)

    return newBackLog

backLogPath = "start.ods"
newBackLogPath = "result.ods"
trackerExportPath = "E-scaleport.csv"
SOLVED = "résolu"
CLOSED = "fermé"

backLog = loadBackLog(backLogPath)
print(backLog[1])
tracker = loadTrackerIssues(trackerExportPath)
backLog = updateBackLog(backLog, tracker)

saveBackLog(backLog, newBackLogPath)

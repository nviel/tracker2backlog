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
import re

def versionOrderKey(versionName):
    if versionName.strip() == '':
        key = "ZZZZ"
    # version sous la forme 4.10
    # transformée en 004010000
    elif re.match(r"^\d+\.\d+$", versionName):
        (M,m) = versionName.split(".")
        key = f"{M:>03}{m:>03}{0:>03}"
    # version sous la forme 4.8.3
    # transformée en 004008003
    elif re.match(r"^\d+\.\d+\.\d+$", versionName):
        (M,m,p) = versionName.split(".")
        key = f"{M:>03}{m:>03}{p:>03}"
    # version sous la forme 2020
    # transformée en 9999999992020
    elif re.match(r"^\d+$", versionName):
        key = "999999999" + versionName
    # autre version ne contenant pas que des chiffres
    else:
        key = 'Z' + versionName
    print(f"[{key}]")
    return key


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

    # repositionnement des tickets mal positionnés par rapport à leur version.
    versions = {}
    # regroupement des tickets par version
    for issue in newBackLog:
        if issue.version_ciblee not in versions:
            versions[issue.version_ciblee] = []
        versions[issue.version_ciblee].append(issue)
    # tri des versions
    versionNames = versions.keys()
    versionNames = sorted(versionNames, key = versionOrderKey)
    print(versionNames)
    orderedBackLog = []
    for versionName in versionNames:
        orderedBackLog += versions[versionName]

    return orderedBackLog

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

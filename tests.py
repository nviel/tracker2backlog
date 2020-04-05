from issue import Issue
from synchro import updateBackLog
import unittest

class MiseAJour(unittest.TestCase):

    def setUp(self):
        pass

    def testUpdateBackLog(self):
        bl = []
        bl.append(Issue(1, "résumé 1", "nouveau", "catégorie 1", "v1.0", "2020-01-01", "catMOA1", 1, 1, "important"))
        bl.append(Issue(2, "résumé 2", "nouveau", "catégorie 2", "v2.0", "2020-01-02", "catMOA2", 2, 2, "bof bof"))
        bl.append(Issue(3, "résumé 3", "nouveau", "catégorie 3", "v3.0", "2020-01-03", "catMOA3", 3, 3, "critique"))
        bl.append(Issue(4, "résumé 4", "nouveau", "catégorie 4", "v4.0", "2020-01-04", "catMOA4", 4, 4, "trop cool!"))

        t = {}
        # aucun changement
        t[1] = Issue(1, "résumé 1", "nouveau", "catégorie 1", "v1.0", "2020-01-01", None, None, None, None) 
        # modification de chaque valeur
        t[2] = Issue(2, "résumé 2'", "nouveau", "catégorie 2'", "v2.0'", "2020-01-02'", None, None, None, None) 
        # t[3] n'existe plus car il a été supprimé dans le tracker
        # ticket résolu
        t[4] = Issue(4, "résumé 4'", "résolu", "catégorie 4'", "v4.0'", "2020-01-04'", None, None, None, None)
        # ticket fermé 
        t[5] = Issue(4, "résumé 5'", "fermé", "catégorie 5'", "v5.0'", "2020-01-05'", None, None, None, None) 
        # nouveau ticket
        t[6] = Issue(6, "résumé 6", "commentaire", "catégorie 6", "v6.0", "2020-01-06", None, None, None, None) 

        new_bl = updateBackLog(bl, t)

        self.assertEqual(new_bl[0], Issue(1, "résumé 1", "nouveau", "catégorie 1", "v1.0", "2020-01-01", "catMOA1", 1, 1, "important"))
        self.assertEqual(new_bl[1], Issue(2, "résumé 2'", "nouveau", "catégorie 2'", "v2.0'", "2020-01-02'", "catMOA2", 2, 2, "bof bof"))
        self.assertEqual(new_bl[2], Issue(6, "résumé 6", "commentaire", "catégorie 6", "v6.0", "2020-01-06", None, None, None, None))



if __name__ == "__main__":
    unittest.main() # run all tests
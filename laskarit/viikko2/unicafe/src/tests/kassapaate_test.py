import unittest
from kassapaate import Kassapaate

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_luotu_kassapaate_on_olemassa(self):
        self.assertNotEqual(self.kassapaate, None)

    def test_kassapaate_alussa_oikein(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)


    
    #     Huomaa, että luokka tallentaa rahamäärän sentteinä
    # Käteisosto toimii sekä edullisten että maukkaiden lounaiden osalta
    #     Jos maksu riittävä: kassassa oleva rahamäärä kasvaa lounaan hinnalla ja vaihtorahan suuruus on oikea
    #     Jos maksu on riittävä: myytyjen lounaiden määrä kasvaa
    #     Jos maksu ei ole riittävä: kassassa oleva rahamäärä ei muutu, kaikki rahat palautetaan vaihtorahana ja myytyjen lounaiden määrässä ei muutosta
    # seuraavissa testeissä tarvitaan myös Maksukorttia jonka oletetaan toimivan oikein
    # Korttiosto toimii sekä edullisten että maukkaiden lounaiden osalta
    #     Jos kortilla on tarpeeksi rahaa, veloitetaan summa kortilta ja palautetaan True
    #     Jos kortilla on tarpeeksi rahaa, myytyjen lounaiden määrä kasvaa
    #     Jos kortilla ei ole tarpeeksi rahaa, kortin rahamäärä ei muutu, myytyjen lounaiden määrä muuttumaton ja palautetaan False
    #     Kassassa oleva rahamäärä ei muutu kortilla ostettaessa
    # Kortille rahaa ladattaessa kortin saldo muuttuu ja kassassa oleva rahamäärä kasvaa ladatulla summalla

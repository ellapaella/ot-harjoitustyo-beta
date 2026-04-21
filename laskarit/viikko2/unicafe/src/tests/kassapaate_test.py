import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):

    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_luotu_kassapaate_on_olemassa(self):
        self.assertNotEqual(self.kassapaate, None)

    def test_kassapaate_alussa_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        
    def test_kassapaate_edullinen_lounas_toimii_oikein_kateisella_summa_riittava(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(1000)
        self.assertEqual(self.kassapaate.edulliset,1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1002.4)
        self.assertEqual(vaihtoraha, 760)

    def test_kassapaate_maukas_lounas_toimii_oikein_kateisella_summa_riittava(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(1000)
        self.assertEqual(self.kassapaate.maukkaat,1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1004.0)
        self.assertEqual(vaihtoraha, 600)

    def test_kassapaate_edullinen_lounas_toimii_oikein_kateisella_summa_ei_riittava(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000.0)
        self.assertEqual(vaihtoraha, 100)

    def test_kassapaate_maukas_lounas_toimii_oikein_kateisella_summa_ei_riittava(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000.0)
        self.assertEqual(vaihtoraha, 100)

    def test_kassapaate_edullinen_lounas_toimii_oikein_kortilla_summa_riittava(self):
        kortti = Maksukortti(1000)
        is_it_True = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassapaate.edulliset,1)
        self.assertEqual(kortti.saldo_euroina(),7.6)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000.0)
        self.assertEqual(is_it_True, True)
        
    def test_kassapaate_maukas_lounas_toimii_oikein_kortilla_summa_riittava(self):
        kortti = Maksukortti(1000)
        is_it_True = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.maukkaat,1)
        self.assertEqual(kortti.saldo_euroina(),6.0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000.0)
        self.assertEqual(is_it_True, True)

    def test_kassapaate_edullinen_lounas_toimii_oikein_kortilla_summa_ei_riittava(self):
        kortti = Maksukortti(100)
        is_it_True = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassapaate.edulliset,0)
        self.assertEqual(kortti.saldo_euroina(),1.0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000.0)
        self.assertEqual(is_it_True, False)
        
    def test_kassapaate_maukas_lounas_toimii_oikein_kortilla_summa_ei_riittava(self):
        kortti = Maksukortti(100)
        is_it_True = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.maukkaat,0)
        self.assertEqual(kortti.saldo_euroina(),1.0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000.0)
        self.assertEqual(is_it_True, False)

    def test_kortille_lataus_toimii_oikein(self):
        kortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(kortti,1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1010.0)
        self.assertEqual(kortti.saldo_euroina(),20.0)

    def test_negatiivisen_summan_lataus_kortille_ei_onnistu(self):
        kortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(kortti,-1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000.0)
        self.assertEqual(kortti.saldo_euroina(),10.0)

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

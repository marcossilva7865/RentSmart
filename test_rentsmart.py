import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
from rentsmart import *

class TestRentSmart(unittest.TestCase):
    def test_apartamentos(self):
        for q in (1, 2):
            for g in (False, True):
                for c in (False, True):
                    with self.subTest(q=q, g=g, c=c):
                        bruto = Decimal(700 + (200 if q == 2 else 0) + (300 if g else 0))
                        self.assertEqual(Apartamento(q,g,c).aluguel(), bruto * (Decimal('1') if c else Decimal('0.95')))
    def test_casas(self):
        for q,g,esperado in [(1,False,900),(2,False,1150),(1,True,1200),(2,True,1450)]:
            self.assertEqual(Casa(q,g).aluguel(), esperado)
    def test_estudios(self):
        for vagas,esperado in [(0,1200),(2,1450),(3,1510),(5,1630)]:
            self.assertEqual(Estudio(vagas).aluguel(), esperado)
    def test_parcelas_e_projecao(self):
        for n in range(1,6):
            contrato = Contrato(n)
            self.assertEqual(sum(contrato.parcelas()),2000)
            linhas = Orcamento(Apartamento(2,True,False),contrato).projecao()
            self.assertEqual(len(linhas),12)
            self.assertEqual(sum(r[3] for r in linhas),15680)
            self.assertEqual(sum(r[2]>0 for r in linhas),n)
        self.assertEqual(Contrato(3).parcelas(),[Decimal('666.67'),Decimal('666.67'),Decimal('666.66')])
    def test_invalidos(self):
        for criar in [lambda: Casa(0,False),lambda: Casa(3,True),lambda: Casa(1,'s'),lambda: Apartamento(1,True,'n'),lambda: Estudio(-1),lambda: Estudio(1),lambda: Estudio(2.5),lambda: Contrato(0),lambda: Contrato(6)]:
            with self.assertRaises(ValueError): criar()
    def test_csv(self):
        with tempfile.TemporaryDirectory() as pasta:
            destino=Path(pasta)/'teste.csv'
            Orcamento(Apartamento(2,True,False),Contrato(3)).exportar_csv(destino)
            with destino.open(encoding='utf-8-sig',newline='') as arquivo:
                linhas=list(csv.DictReader(arquivo,delimiter=';'))
            self.assertEqual(len(linhas),12)
            self.assertEqual(linhas[0]['total_mes'],'1806,67')
            self.assertEqual(linhas[2]['parcela_contrato'],'666,66')
            self.assertEqual(linhas[3]['parcela_contrato'],'0,00')
    @patch('builtins.print')
    def test_entradas(self,_):
        with patch('builtins.input',side_effect=['abc','0','3','2']):
            self.assertEqual(ler_inteiro('Quartos:',1,2),2)
        with patch('builtins.input',side_effect=['talvez',' NÃO ']):
            self.assertFalse(ler_sim_nao('Crianças?'))

if __name__ == '__main__':
    unittest.main()

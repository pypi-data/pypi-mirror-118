import unittest

from tax_calculator import main
from tax_calculator.IMoney import Euro


class MyTestCase(unittest.TestCase):

    def test_forfettario_agevolato(self):
        # see https://flextax.it/regime-forfettario-tassazione/
        result = main._main(["compute-forfettario", "--ricavi", "55000€", "--ateco", "85.32.09", "--contributi_previdenziali_anno_scorso", "4000€", "--aliquota_imposta_sostitutiva", "0.05"])
        self.assertEqual(result["specific"]["ricavi lordi"], Euro(55000))
        self.assertEqual(result["specific"]["ricavi netti"], Euro(42021.12))
        self.assertEqual(result["specific"]["tasse annuali da pagare"], Euro(12978.88))

    def test_forfettario_agevolato_no_ateco(self):
        # see https://flextax.it/regime-forfettario-tassazione/
        result = main._main(["compute-forfettario", "--ricavi", "55000€", "--coefficiente_di_redditivita", "0.78", "--contributi_previdenziali_anno_scorso", "4000€", "--aliquota_imposta_sostitutiva", "0.05"])
        self.assertEqual(result["specific"]["ricavi lordi"], Euro(55000))
        self.assertEqual(result["specific"]["ricavi netti"], Euro(42021.12))
        self.assertEqual(result["specific"]["tasse annuali da pagare"], Euro(12978.88))

    def test_forfettario_normale(self):
        # see https://flextax.it/regime-forfettario-tassazione/
        result = main._main(["compute-forfettario", "--ricavi", "55000€", "--ateco", "85.32.09", "--contributi_previdenziali_anno_scorso", "4000€", "--aliquota_imposta_sostitutiva", "0.15"])
        self.assertEqual(result["specific"]["ricavi lordi"], Euro(55000))
        self.assertEqual(result["specific"]["ricavi netti"], Euro(38131.12))
        self.assertEqual(result["specific"]["tasse annuali da pagare"], Euro(16868.88))

    def test_forfettario_normale_no_ateco(self):
        # see https://flextax.it/regime-forfettario-tassazione/
        result = main._main(["compute-forfettario", "--ricavi", "55000€", "--coefficiente_di_redditivita", "0.78", "--contributi_previdenziali_anno_scorso", "4000€", "--aliquota_imposta_sostitutiva", "0.15"])
        self.assertEqual(result["specific"]["ricavi lordi"], Euro(55000))
        self.assertEqual(result["specific"]["ricavi netti"], Euro(38131.12))
        self.assertEqual(result["specific"]["tasse annuali da pagare"], Euro(16868.88))

    def test_forfettario_agevolato_different_timeinterval(self):
        # see https://flextax.it/regime-forfettario-tassazione/
        result = main._main(["compute-forfettario", "--ricavi", "55000€", "--ateco", "85.32.09", "--start_date", "2021-03-01", "--end_date", "2021-08-28", "--contributi_previdenziali_anno_scorso", "4000€", "--aliquota_imposta_sostitutiva", "0.05"])
        self.assertEqual(result["specific"]["ricavi lordi"], Euro(55000))
        self.assertEqual(result["specific"]["ricavi lordi mensile"], Euro(9166.66667))
        self.assertEqual(result["specific"]["ricavi netti"], Euro(42021.12))
        self.assertEqual(result["specific"]["ricavi netti mensile"], Euro(7003.52))
        self.assertEqual(result["specific"]["tasse annuali da pagare"], Euro(12978.88))


if __name__ == '__main__':
    unittest.main()

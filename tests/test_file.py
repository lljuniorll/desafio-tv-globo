from unittest import TestCase
from controller import File


class TestFile(TestCase):

    def test_valide_filename_valid(self):
        filename = '20190219_000001.txt'
        result = File.valide_filename(filename)
        self.assertTrue(result, 'Deu erro!')

    def test_valide_filename_invalid(self):
        filename = 'nome_invalido.txt'
        result = File.valide_filename(filename)
        self.assertFalse(result, 'Deu erro!')

    def test_filename_date_and_sequence(self):
        filename = '20190219_000001.txt'
        filename_date = '20190219'
        filename_sequence = '000001'
        result = File.filename_date_and_sequence(filename)
        self.assertEqual(result['filename_date'], filename_date)
        self.assertEqual(result['filename_sequence'], filename_sequence)

    def test_extract_line_data(self):
        line = " P    16/12/2018 00:51:54;16 16/12/2018 01:38:24;03 K0021473                " \
               "         Media Event          SUP - (DES)ENCONTRO PERFEITO - S 00:00:20;00 Media        " \
               "                    00:46:29;15 Sequential               Duration                 A) SRV2_REDE    " \
               "                 20181215234                                                       Completed "
        line_data = {'start_time':'16/12/2018 00:51:54;16', 'end_time': '16/12/2018 01:38:24;03',
                     'title': 'SUP - (DES)ENCONTRO PERFEITO - S', 'duration': '00:46:29;15',
                     'reconcile_key': '20181215234'}
        result = File.extract_line_data(line)
        self.assertEqual(result, line_data)


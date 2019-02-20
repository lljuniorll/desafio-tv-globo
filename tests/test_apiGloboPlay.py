from unittest import TestCase
from controller import ApiGloboPlay


class TestApiGloboPlay(TestCase):
    def test_send(self):
        title = 'SUP - (DES)ENCONTRO PERFEITO - S'
        duration = '00:46:29;15'
        path = '20190219_000001.txt'
        result = ApiGloboPlay(title, duration, path).send()
        api_result = [True, False]
        self.assertIn(result, api_result, 'Deu erro!')

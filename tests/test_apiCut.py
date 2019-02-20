from unittest import TestCase
from controller import ApiCut


class TestApiCut(TestCase):
    def test_send(self):
        start_time = '16/12/2018 00:51:54;16'
        end_time = '16/12/2018 01:38:24;03'
        path = '12_1231425234134234.mp4'
        result = ApiCut().send(start_time, end_time, path)
        self.assertTrue(result, 'Deu erro!')

    def test_status(self):
        job_external_id = '516ea484-9b81-4712-9311-75def0ae8722'
        result = ApiCut().status(job_external_id)
        api_result = [True, False]
        self.assertIn(result, api_result, 'Deu erro!')

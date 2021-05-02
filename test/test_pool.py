import unittest
from random import random
import numpy as np
from test.base import BaseTestCase
from src.service.pool_service import calculate_quantile
from src.model.pool import Pool


def first_api_request(client, pool_id, pool_values):
    response = client.post('/api/1', json={
        "poolId": pool_id,
        "poolValues": pool_values
    })
    return response


def second_api_request(client, pool_id, percentile):
    response = client.post('/api/2', json={
        "poolId": pool_id,
        "percentile": percentile
    })
    return response


class TestPool(BaseTestCase):
    def test_first_api(self):
        """Test for the first api"""
        Pool.pools = dict()
        with self.app as c:
            data = first_api_request(c, pool_id=5, pool_values=[1, 2, 5]).get_json()
            self.assertEqual(data['message'], 'inserted')
            data = first_api_request(c, pool_id=3, pool_values=[3, 4]).get_json()
            self.assertEqual(data['message'], 'inserted')
            data = first_api_request(c, pool_id=3, pool_values=[3, 9]).get_json()
            self.assertEqual(data['message'], 'appended')
            data = first_api_request(c, pool_id=3, pool_values=[]).get_json()
            self.assertEqual(data['message'], 'invalid input')
            data = first_api_request(c, pool_id='1', pool_values=[1]).get_json()
            self.assertEqual(data['message'], 'invalid input')
            data = first_api_request(c, pool_id=1, pool_values='[1]').get_json()
            self.assertEqual(data['message'], 'invalid input')
            response = c.post('/api/1', json='')
            data = response.get_json()
            self.assertEqual(data['message'], 'invalid input')

    def test_second_api(self):
        """Test for the second api"""
        Pool.pools = dict()
        pool_id = 2
        pool_values = [1, 3, 4, 3, 8, 9, 10]
        percentile = 99
        with self.app as c:
            first_api_request(c, pool_id, pool_values)
            data = second_api_request(c, pool_id, percentile).get_json()
            self.assertTrue(-0.001 < data['calculatedQuantile'] - np.quantile(pool_values, percentile / 100) < 0.001)
            self.assertEqual(data['totalCount'], 7)

            first_api_request(c, pool_id=3, pool_values=[3])
            data = second_api_request(c, pool_id=3, percentile=percentile).get_json()
            self.assertTrue(-0.001 < data['calculatedQuantile'] - np.quantile([3], percentile / 100) < 0.001)

            first_api_request(c, pool_id, pool_values)
            data = second_api_request(c, pool_id, percentile=0).get_json()
            self.assertTrue(-0.001 < data['calculatedQuantile'] - np.quantile(pool_values, 0) < 0.001)

            first_api_request(c, pool_id, pool_values)
            data = second_api_request(c, pool_id, percentile=100).get_json()
            self.assertTrue(-0.001 < data['calculatedQuantile'] - np.quantile(pool_values, 1) < 0.001)

            response = second_api_request(c, pool_id=-99999, percentile=99)
            data = response.get_json()
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['message'], 'pool not found')

            response = second_api_request(c, pool_id=2, percentile=101)
            data = response.get_json()
            self.assertEqual(data['message'], 'invalid input')

            response = second_api_request(c, pool_id='2', percentile=20)
            data = response.get_json()
            self.assertEqual(data['message'], 'invalid input')

            response = second_api_request(c, pool_id=2, percentile='101')
            data = response.get_json()
            self.assertEqual(data['message'], 'invalid input')

            response = c.post('/api/2', json='')
            data = response.get_json()
            self.assertEqual(data['message'], 'invalid input')

    def test_quantile(self):
        """Test for the quantile calculation function based on comparing with quantile function of numpy library"""
        arr = np.random.rand(1000).tolist()
        q = random()
        quantile = calculate_quantile(arr, q)
        self.assertTrue(-0.001 < quantile - np.quantile(arr, q), 0.001)


if __name__ == "__main__":
    unittest.main()

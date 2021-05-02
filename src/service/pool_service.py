import numbers
from ..model.pool import Pool


def save_pool(data):
    pool_id = data['poolId']
    pool_values = data['poolValues']
    pool = Pool(pool_id, pool_values)
    if pool_id in Pool.pools:
        pool_tmp = Pool.pools[pool_id].get_values()
        pool_tmp.extend(pool_values)
        Pool.pools[pool_id].set_values(pool_tmp)
        return {'message': 'appended'}
    else:
        Pool.pools[pool_id] = pool
        return {'message': 'inserted'}


def calculate_quantile(arr, q=0.5):
    arr.sort()
    n = len(arr)
    if n == 1:
        return arr[0]
    if q == 0:
        return min(arr)
    if q == 1:
        return max(arr)
    indices = q * (n - 1)
    indices_below = int(indices)
    indices_above = int(indices) + 1
    weight_below = indices_above - indices
    weight_above = indices - indices_below
    return arr[indices_below] * weight_below + arr[indices_above] * weight_above


def validate_first_api(request):
    if not isinstance(request.json, dict):
        return False
    try:
        data = request.json
        pool_id = data['poolId']
        pool_values = data['poolValues']
        assert len(pool_values) >= 1
    except (KeyError, AssertionError, TypeError):
        return False
    return all((isinstance(pool_id, int), isinstance(pool_values, list)))


def validate_second_api(request):
    if not isinstance(request.json, dict):
        return False
    try:
        data = request.json
        pool_id = data['poolId']
        percentile = data['percentile']
        assert 0 <= percentile <= 100
    except (KeyError, AssertionError, TypeError):
        return False
    return all((isinstance(pool_id, int), isinstance(percentile, numbers.Number)))

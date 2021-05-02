from flask import request
from . import app
from ..service.pool_service import calculate_quantile, save_pool, validate_first_api, validate_second_api
from ..model.pool import Pool


@app.route('/api/1', methods=['POST'])
def first_api():
    if not validate_first_api(request):
        return {'message': 'invalid input'}, 400
    data = request.json
    return save_pool(data)


@app.route('/api/2', methods=['POST'])
def second_api():
    if not validate_second_api(request):
        return {'message': 'invalid input'}, 400
    body = request.json
    pool_id = body['poolId']
    percentile = body['percentile']
    if pool_id in Pool.pools:
        pool_values = Pool.pools[pool_id].get_values()
        quantile = calculate_quantile(pool_values, percentile / 100)
    else:
        return {'message': 'pool not found'}, 404
    return {
        "calculatedQuantile": quantile,
        "totalCount": len(pool_values)
    }

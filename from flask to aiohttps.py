from aiohttp import web
from datetime import datetime
import json

app = web.Application()

advertisements = {}
ad_id_counter = 1


async def create_ad(request):
    global ad_id_counter
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid JSON'}, status=400)

    if not all(key in data for key in ['title', 'description', 'owner']):
        return web.json_response({'error': 'Missing required fields'}, status=400)

    ad = {
        'id': ad_id_counter,
        'title': data['title'],
        'description': data['description'],
        'created_at': datetime.now().isoformat(),
        'owner': data['owner']
    }

    advertisements[ad_id_counter] = ad
    ad_id_counter += 1

    return web.json_response(ad, status=201)


async def get_ad(request):
    ad_id = int(request.match_info['ad_id'])
    ad = advertisements.get(ad_id)
    if not ad:
        return web.json_response({'error': 'Advertisement not found'}, status=404)
    return web.json_response(ad)


async def delete_ad(request):
    ad_id = int(request.match_info['ad_id'])
    if ad_id not in advertisements:
        return web.json_response({'error': 'Advertisement not found'}, status=404)

    del advertisements[ad_id]
    return web.json_response({'message': 'Advertisement deleted successfully'})


async def update_ad(request):
    ad_id = int(request.match_info['ad_id'])
    if ad_id not in advertisements:
        return web.json_response({'error': 'Advertisement not found'}, status=404)

    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid JSON'}, status=400)

    if not data:
        return web.json_response({'error': 'No data provided'}, status=400)

    ad = advertisements[ad_id]
    if 'title' in data:
        ad['title'] = data['title']
    if 'description' in data:
        ad['description'] = data['description']
    if 'owner' in data:
        ad['owner'] = data['owner']

    return web.json_response(ad)


app.router.add_post('/ads', create_ad)
app.router.add_get('/ads/{ad_id}', get_ad)
app.router.add_delete('/ads/{ad_id}', delete_ad)
app.router.add_put('/ads/{ad_id}', update_ad)

if __name__ == '__main__':
    web.run_app(app)
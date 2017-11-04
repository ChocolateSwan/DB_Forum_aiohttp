from aiohttp import web


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    # return web.Response(text=text)
    data = {'some': 'data'}
    return web.json_response(data, status=300)
# async def index(request):
#     return web.Response(text='Hello Aiohttp!')
#
#
# def setup_routes(app):
#     app.router.add_get('/', index)

app = web.Application()
# setup_routes(app)

app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)
web.run_app(app, host='127.0.0.1', port=8888)
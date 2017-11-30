from aiohttp.web import json_response, View

async def post(self):
    pool = self.request.app['pool']
    async with pool.acquire() as connection:
        async with connection.transaction():
from aiohttp.web import json_response, View


class ForumCreate (View):
    async def post(self):
        pool = self.request.app['pool']
        async with pool.acquire() as connection:
            async with connection.transaction():
                data = await  self.request.json()
                result_user = await connection.fetchrow(
                    ''' select id, nickname from "User" where nickname = $1''',
                    data.get('user',' ')
                )
                if result_user is None:
                    return json_response({'message': 'Cant find user' },
                                         status=404)
                result_user = dict(result_user)
                result_forum = await connection.fetchrow(
                    '''INSERT INTO forum (slug, title, "user", user_id) VALUES
                ($1, $2, $3, $4)
                ON CONFLICT DO NOTHING
                RETURNING posts, slug, threads, title, "user"''',
                    data.get('slug',' '),
                    data.get('title', ' '),
                    result_user.get('nickname', ' '),
                    result_user.get('id', 0)
                )
                if result_forum is not None:
                    return json_response(dict(result_forum),
                                         status=201)
                result_forum = await connection.fetchrow(
                    ''' select posts, slug, threads, title, "user" from forum where slug = $1''',
                    data.get('slug',' ')
                )
                print(result_forum)
                return json_response(dict(result_forum),
                                     status=409)


class ForumDetails (View):
    async def get(self):
        pool = self.request.app['pool']
        async with pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    '''select posts, slug, threads, title, "user" from forum where slug = $1''',
                                                   self.request.match_info['slug'])
                status = 404 if result is None else 200
                return json_response({'message': 'cant find forum'} if status == 404 else dict(result),
                                     status=status)
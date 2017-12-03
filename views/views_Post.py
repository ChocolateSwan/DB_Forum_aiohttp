from aiohttp.web import json_response, View
class PostCreate (View):
    async def post(self):
        pool = self.request.app['pool']
        async with pool.acquire() as connection:
            async with connection.transaction():
                slug_or_id = self.request.match_info['slug_or_id']
                data = await  self.request.json()
                try:
                    thread_id = int(slug_or_id)
                    result_thread = await connection.fetchrow('''
                                    SELECT forum_id, forum
                                    FROM thread
                                    WHERE id = $1
                                    ''', thread_id)
                    if not result_thread:
                        return json_response({'message': 'no thread'},
                                             status=404)
                    result_thread = dict(result_thread)
                    forum_id = result_thread.get('forum_id')
                    forum_slug = result_thread.get('forum')
                except ValueError:
                    result_thread = await connection.fetchrow('''
                                                        SELECT id, forum_id, forum
                                                        FROM thread
                                                        WHERE slug = $1::citext
                                                        ''', slug_or_id)
                    if not result_thread:
                        return json_response({'message': 'no thread'},
                                             status=404)
                    result_thread = dict(result_thread)
                    thread_id = result_thread.get('id')
                    forum_id = result_thread.get('forum_id')
                    forum_slug = result_thread.get('forum')

                await connection.fetchall('''
                    INSERT INTO "Post" (author_id, author, forum_id, forum, created, message, root_parent, parent, path, thread_id)
                    SELECT 
                      u.id,
                      u.nickname,
                      $1,
                      $2::citext,
                      t.message,
                      case when t.pid = 0 then t.id else p.path[1] end,
                      case when t.pid = 0 then 0 else 
                
                ''')

                # result_user = await connection.fetchrow('''
                #                                         SELECT id, nickname
                #                                         FROM "User"
                #                                         WHERE nickname = $1::citext
                #                                         ''', data.get('nickname'))
                # if not result_user:
                #     return json_response({'message': 'no user'},
                #                          status=404)
                # result_user = dict(result_user)
                # user_id = result_user.get('id')
                #user_nickname = result_user.get('nickname')

                return json_response({1:1}, status=200)
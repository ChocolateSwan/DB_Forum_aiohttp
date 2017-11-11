from aiohttp.web import json_response, View
import json
from dateutil.tz import tzutc
from datetime import datetime
from pytz import timezone

from queryes.query_Thread import create_thread

UTC = tzutc()
def serialize_date(dt):

    if dt.tzinfo:
        dt = dt.astimezone(UTC).replace(tzinfo=None)
    return dt.isoformat() + 'Z'


# TODO +1 в форум
class ThreadCreate (View):
    async def post(self):
        pool = self.request.app['pool']
        async with pool.acquire() as connection:
            async with connection.transaction():
                data = await  self.request.json()
                # TODO добавить default в гет чтоб исключение не бросало
                result_user = await connection.fetchrow(
                    ''' select id, nickname from "User" where nickname = $1''',
                    data.get('author',' ')
                )
                if result_user is None:
                    return json_response({'message': 'Cant find user' },
                                         status=404)
                result_forum = await connection.fetchrow(
                    ''' select id, slug from forum where slug = $1''',
                    self.request.match_info['slug']
                )
                if result_forum is None:
                    return json_response({'message': 'Cant find forum' },
                                         status=404)

                result_user = dict(result_user)
                result_forum = dict(result_forum)
                created = data.get('created')
                if created:
                    t = datetime.strptime(''.join(created.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S.%f%z')
                    t.astimezone(UTC)
                else:
                    t = datetime.now(UTC)

                result_thread = await connection.fetchrow(create_thread,
                    result_user.get('id', 0),
                    result_user.get('nickname', ' '),
                    result_forum.get('id', 0),
                    result_forum.get('slug', ' '),
                    data.get('message', ' '),
                    data.get('slug', None),
                    data.get('title', ' '),
                    t,
                )

                result_thread = dict(result_thread)
                result_thread['created'] = result_thread['created'].isoformat()

                status = 201 if result_thread['bool'] else 409
                result_thread.pop('bool', False)
                return json_response(result_thread,
                                     status=status)

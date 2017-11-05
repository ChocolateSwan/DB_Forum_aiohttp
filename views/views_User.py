from aiohttp.web import json_response, View

from queryes.query_User import create_user, get_user, update_user, up_u, up_u_2


class Test(View):
    async def get(self):
        data = {'some': 'data1'}
        return json_response(data, status=400)

class Test_db(View):
    async  def get(self):
        pool = self.request.app['pool']
        # Take a connection from the pool.
        async with pool.acquire() as connection:
            # Open a transaction.
            async with connection.transaction():
                # Run the query passing the request argument.
                result = await connection.fetch('''SELECT * FROM "User" where nickname = $1 ''',"silva.mtdeemjJx10Pj1")
                return json_response({'row':dict(result[0])}, status=400)


class UserCreate (View):
    async def post(self):
        pool = self.request.app['pool']
        async with pool.acquire() as connection:
            async with connection.transaction():
                data = await  self.request.json()
                # TODO добавить default в гет чтоб исключение не бросало
                result = await connection.fetch(create_user,
                                                data.get('about'),
                                                data.get('email'),
                                                data.get('fullname'),
                                                self.request.match_info['nickname'])
                result = list(map(lambda x: dict(x), result))
                status = 201 if result[0]['bool'] else 409
                for res in result:
                    res.pop('bool', False)
                return json_response(result if status == 409 else result[0],
                                     status=status)


class UserProfile (View):
    async def get(self):
        pool = self.request.app['pool']
        async with pool.acquire() as connection:
            async with connection.transaction():
                # TODO добавить default в гет чтоб исключение не бросало
                result = await connection.fetchrow(get_user,
                                                   self.request.match_info['nickname'])
                status = 404 if result is None else 200
                return json_response({'message': 'cant find user'} if status == 404 else dict(result),
                                     status=status)

    async def post(self):
        pool = self.request.app['pool']
        async with pool.acquire() as connection:
            async with connection.transaction():
                # TODO добавить default в гет чтоб исключение не бросало
                data = await  self.request.json()
                req_update_user = ' '
                for key in data:
                    req_update_user += key + " = '" + str(data[key]) + "', "
                req_update_user = req_update_user[:req_update_user.rfind(',')]
                print (req_update_user)
                update_u = update_user.format(req_update_user, "'"+self.request.match_info['nickname']+"'", "'"+data.get('email',' ') + "'")
                update_u = up_u.format( "'"+data.get('email',' ') + "'" if data.get('email','') else ''
                    # "'"+data.get('email',' ') + "'"
                                        ) + update_u + up_u_2
                print (update_u)
                result = await connection.fetchrow(update_u)
                print (result)
                result = dict(result)
                # {'message': 'cant find user'}
                status = 200
                if result['bool'] == True:
                    status = 200
                else:
                    status = 409



                return json_response(result,
                                     status=status)


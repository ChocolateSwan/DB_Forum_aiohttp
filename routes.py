from views import *


# Первый элемент — http метод, далее расположен url,
# третьим в кортеже идёт объект handler,
# и напоследок — имя route, чтобы удобно было его вызывать в коде.
routes = [
    ('GET', '/', Test_db, 'main'),
    ('POST', '/user/{nickname}/create', UserCreate, 'create_user'),
    ('*', '/user/{nickname}/profile', UserProfile, 'profile_user'),
    # ('*',   '/log', Login,   'signout'),
]
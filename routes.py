from views.views_User import *
from views.views_Forum import *


# Первый элемент — http метод, далее расположен url,
# третьим в кортеже идёт объект handler,
# и напоследок — имя route, чтобы удобно было его вызывать в коде.
routes = [
    ('POST', '/user/{nickname}/create', UserCreate, 'create_user'),
    ('*', '/user/{nickname}/profile', UserProfile, 'profile_user'),
    ('POST', '/forum/create', ForumCreate, 'create_forum'),
    ('GET', '/forum/{slug}/details', ForumDetails, 'details_forum'),

]
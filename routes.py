from views.views_User import *
from views.views_Forum import *
from views.views_Thread import *

# Первый элемент — http метод, далее расположен url,
# третьим в кортеже идёт объект handler,
# и напоследок — имя route, чтобы удобно было его вызывать в коде.
routes = [
    ('POST', '/api/user/{nickname}/create', UserCreate, 'create_user'),
    ('*', '/api/user/{nickname}/profile', UserProfile, 'profile_user'),
    ('POST', '/api/forum/create', ForumCreate, 'create_forum'),
    ('GET', '/api/forum/{slug}/details', ForumDetails, 'details_forum'),
    ('POST', '/api/forum/{slug}/create', ThreadCreate, 'create_thread'),
]
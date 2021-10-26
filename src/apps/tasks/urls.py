from django.urls import path, include

from .views.transitions import (
    TransitionListApi,
)
from .views.tasks import (
    TaskListApi,
    TaskCreateApi,
    TaskUpdateApi
)

from .views.check_items import (
    CheckItemListApi,
    CheckItemCreateApi,
    CheckItemUpdateApi,
    CheckItemDeleteApi,
)

app_name = "admin_users"

transition_urlpatterns = [
    path('', TransitionListApi.as_view(), name='list'),
]

check_item_urlpatterns = [
    path('create/', CheckItemCreateApi.as_view(), name='create'),
    path('<int:item_id>/update/', CheckItemUpdateApi.as_view(), name='update'),
    path('<int:item_id>/delete/', CheckItemDeleteApi.as_view(), name='delete'),
    path('', CheckItemListApi.as_view(), name='list'),
]

task_urlpatterns = [
    path('create/', TaskCreateApi.as_view(), name='create'),
    path('<int:task_id>/update/', TaskUpdateApi.as_view(), name='update'),
    path('<int:task_id>/transitions/', include((transition_urlpatterns, 'transitions'))),
    path('<int:task_id>/check-items/', include((check_item_urlpatterns, 'check-items'))),
    path('', TaskListApi.as_view(), name='list'),
]

urlpatterns = [
    path('', include((task_urlpatterns, 'tasks')))
]

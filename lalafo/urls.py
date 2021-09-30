
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import LalafoViewSet, CommentViewSet, RatingViewSet, FavouritesListView

router = SimpleRouter()
router.register('lalafo', LalafoViewSet, 'lalafo')
router.register('comments', CommentViewSet, 'comments')
router.register('ratings', RatingViewSet, 'ratings')

urlpatterns = [
    path('', include(router.urls)),
    path('favourites_list/', FavouritesListView.as_view())
]


# urlpatterns = [
#     path('lalafo/', LalafoViewSet.as_view(
#         {'get': 'list',
#          'post': 'create'}
#     )),
#     path('lalafo/<int:pk>/', LalafoViewSet.as_view(
#         {'get': 'retrieve',
#          'put': 'update',
#          'patch': 'partial_update',
#          'delete': 'destroy'}
#     )),
# ]

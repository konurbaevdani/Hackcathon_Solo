from django_filters import rest_framework as rest_filters
from rest_framework import viewsets, mixins, filters
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.viewsets import GenericViewSet
from lalafo.models import Lalafo, Comment, Like, Favourite, Rating
from lalafo.permissions import IsAuthor, IsAuthorOrIsAdmin
from lalafo.serializers import (LalafoListSerializer,
                                LalafoDetailSerializer,
                                CreateLalafoSerializer,
                                CommentSerializer, RatingSerializer, FavouriteLalafoSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


class LalafoFilter(rest_filters.FilterSet):
    created_at = rest_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Lalafo
        fields = ('category', 'title', 'price', 'id')


class LalafoViewSet(viewsets.ModelViewSet):
    queryset = Lalafo.objects.all()
    serializer_class = CreateLalafoSerializer
    permission_classes = [IsAuthorOrIsAdmin]
    filter_backends = [rest_filters.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_class = LalafoFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return LalafoListSerializer
        elif self.action == 'retrieve':
            return LalafoDetailSerializer
        return CreateLalafoSerializer

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, user=user)
            like.is_liked = not like.is_liked
            if like.is_liked:
                like.save()
            else:
                like.delete()
            message = 'нравится' if like.is_liked else 'ненравится'
        except Like.DoesNotExist:
            Like.objects.create(post=post, user=user, is_liked=True)
            message = 'нравится'
        return Response(message, status=200)

    @action(['POST'], detail=True)
    def favourite(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            favourite = Favourite.objects.get(post=post, user=user)
            favourite.is_favourite = not favourite.is_favourite
            if favourite.is_favourite:
                favourite.save()
            else:
                favourite.delete()
            message = 'добавлено в избранные' if favourite.is_favourite else 'удалено из избранных'
        except Favourite.DoesNotExist:
            Favourite.objects.create(post=post, user=user, is_favourite=True)
            message = 'добавлено в избранные'
        return Response(message, status=200)

    def get_permission(self):
        if self.action == 'create' or self.action == 'like' or self.action == 'favourite':
            return [IsAuthenticated()]
        return [IsAuthorOrIsAdmin()]


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]


class LalafoDetailView(RetrieveAPIView):
    queryset = Lalafo.objects.all()
    serializer_class = LalafoListSerializer


class CreateLalafoView(CreateAPIView):
    queryset = Lalafo.objects.all()
    serializer_class = LalafoListSerializer


class UpdateLalafoView(UpdateAPIView):
    queryset = Lalafo.objects.all()
    serializer_class = LalafoListSerializer


class DeleteLalafoView(DestroyAPIView):
    queryset = Lalafo.objects.all()
    serializer_class = LalafoListSerializer


class RatingViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]


class FavouritesListView(ListAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteLalafoSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_fields = ['user', ]






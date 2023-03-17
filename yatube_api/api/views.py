from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated,
                                        )
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (CommentSerializer,
                          FollowSerializer,
                          GroupSerializer,
                          PostSerializer
                          )

from posts.models import Follow, Group, Post


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnlyPermission]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        if not self.request.user:
            raise ValidationError(
                'Только зарегистрированные пользователи '
                'могут отправлять сообщения.'
            )
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        if not request.user:
            return Response(
                {'detail': 'Зарегистрируйтесь или войдите на сайт.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not request.user:
            return Response(
                {'detail': 'Зарегистрируйтесь или войдите на сайт.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().list(request, *args, **kwargs)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet
                    ):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        if not self.request.user:
            raise ValidationError(
                'Только зарегистрированные пользователи '
                'могут отправлять сообщения.'
            )
        serializer.save(author=self.request.user)

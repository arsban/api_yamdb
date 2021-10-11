from Yamdb.models import User, Title, Comment, Review
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from Yamdb.models import User

from .permissions import IsAdmin, IsOwnerAdminModeratorOrReadOnly
from .serializers import (ConfirmationCodeSerializer, EmailSerializer,
                          UserSerializer, ReviewSerializer, CommentSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['get', 'post',
                         'patch', 'delete']
    search_fields = ['username']
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )


class EmailRegistrationView(views.APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def mail_send(email, user):
        send_mail(
            subject='YaMDB Confirmation Code',
            message=f'Hello! \n\nYour confirmation: '
                    f'{user.confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        serializer.save(email=email)
        user = get_object_or_404(User, email=email)
        self.mail_send(email, user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccessTokenView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        username = serializer.validated_data['username']
        try:
            user = get_object_or_404(User, username=username)
        except User.DoesNotExist:
            return Response({
                'email':
                    'Not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.confirmation_code != confirmation_code:
            return Response({
                'confirmation_code':
                    f'Invalid confirmation code for email {user.email}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.get_token(user), status=status.HTTP_200_OK)

    @staticmethod
    def get_token(user):
        return {
            'token': str(AccessToken.for_user(user))
        }


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer = ReviewSerializer(data=request.data)
        if Review.objects.filter(author=self.request.user, title=title).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, title_id=title.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=self.kwargs.get('id'),
                                   title__id=self.kwargs.get('title_id'))
        if self.request.user != review.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        if self.request.user == review.author:
            return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        return Comment.objects.filter(review=review)

    def create(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=self.kwargs('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, review_id=review.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'),
                                    review__id=self.kwargs.get('review_id'))
        if self.request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data,
                                       partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

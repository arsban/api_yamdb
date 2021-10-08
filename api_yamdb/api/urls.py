from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import GenreViewSet, CategoryViewSet, TitleViewSet, EmailRegistrationView,  AccessTokenView

router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)


urlpatterns = [
    path('v1/auth/email/', EmailRegistrationView.as_view()),
    path('v1/auth/token/', AccessTokenView.as_view()),
    path('v1/', include(router_v1.urls))
]

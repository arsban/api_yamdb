from django.urls import path, include

from .views import (GenreViewSet, CategoryViewSet, TitleViewSet,
                    AccessTokenView, EmailRegistrationView)

from rest_framework.routers import SimpleRouter


router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)


urlpatterns = [
    path('v1/auth/signup/', EmailRegistrationView.as_view()),
    path('v1/auth/token/', AccessTokenView.as_view()),
    path('v1/', include(router_v1.urls))
]

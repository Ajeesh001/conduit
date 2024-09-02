from django.urls import path
from api import views

urlpatterns = [
    path('signup', views.signup_view, name='signup'),
    path('signin', views.signin_view, name='signin'),
    path('addarticle', views.add_article, name='addarticle'),
    path('logout', views.logout_view, name='logout'),
    path('userarticles', views.user_articles_view, name='userarticles'),
    path('globalfeed', views.global_feed, name='globalfeed'),
    # path('check_token/', views.check_token, name='check_token'),
]
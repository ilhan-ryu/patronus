from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^explore$',
        view=views.ExplorerUsers.as_view(),
        name='explore_users'
    ),
    url(
        regex=r'^(?P<user_id>[0-9]+)/follow/$',
        view=views.FollowUsers.as_view(),
        name='follow_user'
    ),
    url(
        regex=r'^(?P<user_id>[0-9]+)/unfollow/$',
        view=views.UnFollowUsers.as_view(),
        name='unfollow_user'
    ),
    url(
        regex=r'search/$',
        view=views.Search.as_view(),
        name='search_user'
    ),
    url(
        regex=r'^(?P<username>\w+)/$',
        view=views.UserProfile.as_view(),
        name='user_profile'
    ),
    url(
        regex=r'^(?P<username>\w+)/followers/$',
        view=views.UserFollowing.as_view(),
        name='user_followers'
    ),
    url(
        regex=r'^(?P<username>\w+)/following/$',
        view=views.UserFollowing.as_view(),
        name='user_following'
    ),
    url(
        regex=r'^(?P<username>\w+)/password/$',
        view=views.ChangePassword.as_view(),
        name='change_password'
    ),
    url(
        regex=r'^login/facebook/$',
        view=views.FacebookLogin.as_view(),
        name='fb_login')
]

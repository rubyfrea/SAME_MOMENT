from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from samemoment import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^create-post$', views.add_post),
    url(r'^delete-post/(?P<post_id>\d+)$', views.delete_post),
    url(r'^login$', auth_views.login, {'template_name':'samemoment/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login),
    url(r'^register$', views.register),
    url(r'^view-profile/(?P<post_user>.+)$', views.view_profile),
]

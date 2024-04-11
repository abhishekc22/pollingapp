from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("signing/", views.signing, name="signing"),
    path("pollingpage/", views.creation_polling, name="pollingpage"),
    path("creation_polling/", views.create_poll, name="create_poll"),
    path("add-choices/<int:poll_id>/", views.add_choices, name="add_choices"),
    path("poll_list/", views.poll_list, name="poll_list"),
    path("polls/<int:poll_id>/vote/", views.vote, name="vote"),
    path("logout/", views.logout_view, name="logout"),
]

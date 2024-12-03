from django.urls import path, include

from accounts.views import RegisterWorker, WorkerListView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", RegisterWorker.as_view(), name="register"),
    path("workers/", WorkerListView.as_view(), name="workers-list"),
]

app_name = "accounts"
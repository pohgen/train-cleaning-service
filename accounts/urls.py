from django.urls import path, include

from accounts.views import RegisterWorker, WorkerListView, WorkerDetailView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", RegisterWorker.as_view(), name="register"),
    path("workers/", WorkerListView.as_view(), name="workers-list"),
path(
        "workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"
    ),
]

app_name = "accounts"
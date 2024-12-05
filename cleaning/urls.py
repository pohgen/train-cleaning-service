from django.urls import path

from cleaning.views import (
    index,
    TrainListView,
    stamp_date_start,
    stamp_date_end,
    TrainCreateView,
    TrainUpdateView,
    TrainDeleteView,
    approval_create_view,
    TrainDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("trains/", TrainListView.as_view(), name="trains-list"),
    path("trains/<int:pk>/start-time/", stamp_date_start, name="clean-time-start"),
    path("trains/<int:pk>/end-time/", stamp_date_end, name="clean-time-end"),
    path("trains/create/", TrainCreateView.as_view(), name="create-train"),
    path("trains/<int:pk>/update/", TrainUpdateView.as_view(), name="update-train"),
    path("trains/<int:pk>/delete/", TrainDeleteView.as_view(), name="delete-train"),
    path("trains/<int:pk>/detail/", TrainDetailView.as_view(), name="detail-train"),
    path(
        "trains/<int:pk>/approval-create/", approval_create_view, name="approval-create"
    ),
]


app_name = "cleaning"

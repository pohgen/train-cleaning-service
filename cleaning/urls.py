from django.urls import path

from cleaning.views import (
    index,
    TrainListView,
    stamp_date_start,
    stamp_date_end,
)

urlpatterns = [
    path("", index, name="index"),
    path("trains/", TrainListView.as_view(), name="trains-list"),
    path("trains/<int:pk>/start_time/", stamp_date_start, name="clean-time-start"),
    path("trains/<int:pk>/end_time/", stamp_date_end, name="clean-time-end"),
]





app_name = "cleaning"


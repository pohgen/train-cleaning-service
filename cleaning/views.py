from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import generic

from cleaning.models import Train

def index(request):

    cleaned_trains = Train.objects.filter(
        Q(status=Train.Status.COMPLETED) | Q(status=Train.Status.APPROVED)
    ).values_list("name", flat=True)

    uncleaned_trains = Train.objects.filter(
        Q(status=Train.Status.AWAITS) | Q(status=Train.Status.IN_PROGRESS)
    ).values_list("name", flat=True)

    rejected_trains = Train.objects.filter(
        status=Train.Status.CANCELED
    ).values_list('name', flat=True)

    context = {
        "cleaned_trains": cleaned_trains,
        "uncleaned_trains": uncleaned_trains,
        "rejected_trains": rejected_trains
    }
    return render(request, "cleaning/index.html", context=context)


class TrainListView(LoginRequiredMixin, generic.ListView):
    model = Train
    context_object_name = "trains_list"
    template_name = "cleaning/trains_list.html"


def stamp_date_start(request, pk):
    train = Train.objects.get(id=pk)
    train.start_time = now()
    train.save()
    return HttpResponseRedirect(reverse_lazy("cleaning:trains-list"))

def stamp_date_end(request, pk):
    train = Train.objects.get(id=pk)
    train.end_time = now()
    train.save()
    return HttpResponseRedirect(reverse_lazy("cleaning:trains-list"))

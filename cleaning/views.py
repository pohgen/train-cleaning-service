from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import generic

from cleaning.forms import TrainCreateForm, ApprovalForm, TrainSearchForm
from cleaning.models import Train


def index(request):

    cleaned_trains = Train.objects.filter(
        Q(status=Train.Status.COMPLETED) | Q(status=Train.Status.APPROVED)
    ).values_list("name", flat=True)

    uncleaned_trains = Train.objects.filter(
        Q(status=Train.Status.AWAITS) | Q(status=Train.Status.IN_PROGRESS)
    ).values_list("name", flat=True)

    rejected_trains = Train.objects.filter(status=Train.Status.CANCELED).values_list(
        "name", flat=True
    )

    context = {
        "cleaned_trains": cleaned_trains,
        "uncleaned_trains": uncleaned_trains,
        "rejected_trains": rejected_trains,
    }
    return render(request, "cleaning/index.html", context=context)


class TrainListView(LoginRequiredMixin, generic.ListView):
    model = Train
    context_object_name = "trains_list"
    template_name = "cleaning/trains_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TrainListView, self).get_context_data(**kwargs)
        search_name = self.request.GET.get("name", "")
        context["search_form"] = TrainSearchForm(initial={"name": search_name})
        return context

    def get_queryset(self):
        queryset = Train.objects.prefetch_related("workers")
        search_name = self.request.GET.get("name")
        if search_name:
            return queryset.filter(name__icontains=search_name)
        return queryset


def stamp_date_start(request, pk):
    train = Train.objects.get(id=pk)
    train.start_time = now()
    train.status = Train.Status.IN_PROGRESS
    train.save()
    return HttpResponseRedirect(reverse_lazy("cleaning:trains-list"))


def stamp_date_end(request, pk):
    train = Train.objects.get(id=pk)
    train.end_time = now()
    train.status = Train.Status.COMPLETED
    train.save()
    return HttpResponseRedirect(reverse_lazy("cleaning:trains-list"))


class TrainCreateView(LoginRequiredMixin, generic.CreateView):
    model = Train
    form_class = TrainCreateForm
    success_url = reverse_lazy("cleaning:trains-list")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["workers"].queryset = form.fields["workers"].queryset.exclude(
            Q(username="admin") | Q(role="auditor")
        )
        return form


class TrainUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Train
    form_class = TrainCreateForm
    success_url = reverse_lazy("cleaning:trains-list")


class TrainDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Train
    template_name = "cleaning/confirm_delete_train.html"
    success_url = reverse_lazy("cleaning:trains-list")


class TrainDetailView(LoginRequiredMixin, generic.DetailView):
    model = Train
    queryset = Train.objects.all().prefetch_related("approval__worker")


def approval_create_view(request, pk):
    train = get_object_or_404(Train, pk=pk)

    if train.approval:
        return redirect("cleaning:trains-list")

    if request.method == "POST":
        form = ApprovalForm(request.POST)
        if form.is_valid():
            approval = form.save(commit=False)
            approval.save()
            train.approval = approval
            train.save()
            if approval.status:
                train.status = Train.Status.APPROVED
            else:
                train.status = Train.Status.CANCELED
            train.save()
            return redirect("cleaning:trains-list")
    else:
        form = ApprovalForm(initial={"train": train, "worker": request.user})
    return render(
        request, "cleaning/approval_form.html", {"form": form, "train": train}
    )

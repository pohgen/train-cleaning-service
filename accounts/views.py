from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView

from accounts.forms import CustomUserCreationForm
from accounts.models import Worker
from cleaning.models import Train


class RegisterWorker(FormView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("cleaning:index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    context_object_name = "workers_list"
    template_name = "accounts/workers_list.html"

    def get_queryset(self):
        return super().get_queryset().exclude(is_superuser=True)


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("trains")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()

        if worker.role == Worker.Role.AUDITOR:
            trains_to_approve = Train.objects.filter(
                approval__isnull=True,
                status=Train.Status.COMPLETED,
                end_time__isnull=False
            )
            context['trains_to_approve'] = trains_to_approve

        return context
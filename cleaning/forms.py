from django import forms

from accounts.models import Worker
from cleaning.models import Train, Approval


class TrainCreateForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Train
        fields = ("name", "cleaning_type", "workers")


class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = ("worker", "status", "comments")


class TrainSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search train by name"
            }
        ))
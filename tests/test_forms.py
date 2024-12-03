from django.test import TestCase
from accounts.models import Worker
from cleaning.models import Train, Approval
from cleaning.forms import TrainCreateForm, ApprovalForm, TrainSearchForm


class TrainCreateFormTest(TestCase):
    def setUp(self):
        self.worker1 = Worker.objects.create(username="worker1")
        self.worker2 = Worker.objects.create(username="worker2")

    def test_train_create_form_valid_data(self):
        form_data = {
            'name': '78-003',
            'cleaning_type': 'SP1',
            'workers': [self.worker1.id, self.worker2.id],
        }
        form = TrainCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_train_create_form_invalid_data(self):
        form_data = {
            'cleaning_type': 'SP1',
        }
        form = TrainCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('workers', form.errors)


class ApprovalFormTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create(username="approver")

    def test_approval_form_valid_data(self):
        form_data = {
            'worker': self.worker.id,
            'status': True,
            'comments': 'Approved train',
        }
        form = ApprovalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_approval_form_default_behavior(self):
        form_data = {
            'worker': self.worker.id,
            'status': False,
        }
        form = ApprovalForm(data=form_data)
        self.assertTrue(form.is_valid())
        result = form.cleaned_data.get('comments')
        self.assertEqual(result, '')


class TrainSearchFormTest(TestCase):
    def test_train_search_form_valid_data(self):
        form_data = {'name': '78-003'}
        form = TrainSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_train_search_form_empty_input(self):
        form_data = {'name': ''}
        form = TrainSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

from django.test import TestCase
from django.urls import reverse

from accounts.models import Worker
from cleaning.models import Train


class IndexViewTest(TestCase):
    def setUp(self):
        Train.objects.create(name="Train1", status=Train.Status.AWAITS)
        Train.objects.create(name="Train2", status=Train.Status.COMPLETED)
        Train.objects.create(name="Train3", status=Train.Status.CANCELED)

    def test_index_view_context(self):
        response = self.client.get(reverse("cleaning:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Train2", response.context["cleaned_trains"])
        self.assertIn("Train1", response.context["uncleaned_trains"])
        self.assertIn("Train3", response.context["rejected_trains"])


class StampDateViewTest(TestCase):
    def setUp(self):
        self.train = Train.objects.create(name="Train1", status=Train.Status.AWAITS)

    def test_stamp_date_start(self):
        self.client.get(reverse("cleaning:clean-time-start", args=[self.train.pk]))
        self.train.refresh_from_db()
        self.assertEqual(self.train.status, Train.Status.IN_PROGRESS)
        self.assertIsNotNone(self.train.start_time)

    def test_stamp_date_end(self):
        self.train.status = Train.Status.IN_PROGRESS
        self.train.save()
        self.client.get(reverse("cleaning:clean-time-end", args=[self.train.pk]))
        self.train.refresh_from_db()
        self.assertEqual(self.train.status, Train.Status.COMPLETED)
        self.assertIsNotNone(self.train.end_time)


class ApprovalCreateViewTest(TestCase):
    def setUp(self):
        self.train = Train.objects.create(name="Train1", status=Train.Status.COMPLETED)
        self.worker = Worker.objects.create(username="worker1")

    def test_approval_create_view(self):
        form_data = {
            "worker": self.worker.pk,
            "status": True,
            "comments": "Approved",
        }
        self.client.post(
            reverse("cleaning:approval-create", args=[self.train.pk]), data=form_data
        )
        self.train.refresh_from_db()
        self.assertEqual(self.train.status, Train.Status.APPROVED)
        self.assertIsNotNone(self.train.approval)

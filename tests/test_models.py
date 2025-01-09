import time

from django.test import TestCase
from django.utils.timezone import now

from cleaning.models import Train, Approval
from accounts.models import Worker


class TrainModelTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create(username="testworker")

        self.approval = Approval.objects.create(
            worker=self.worker, status=True, comments="Test approval"
        )

        self.train = Train.objects.create(
            name="78-002",
            cleaning_type="SP1",
            status=Train.Status.AWAITS,
            approval=self.approval,
        )
        self.train.workers.add(self.worker)

    def test_train_string_representation(self):
        self.assertEqual(str(self.train), "78-002")

    def test_default_status(self):
        self.assertEqual(self.train.status, Train.Status.AWAITS)

    def test_train_status_changes_based_on_approval(self):
        self.assertEqual(self.train.status, Train.Status.AWAITS)

        if self.approval.status:
            self.train.status = Train.Status.APPROVED
        else:
            self.train.status = Train.Status.CANCELED

        self.train.save()
        self.assertEqual(self.train.status, Train.Status.APPROVED)

    def test_train_with_multiple_workers(self):
        worker2 = Worker.objects.create(username="worker2")
        self.train.workers.add(worker2)

        self.assertEqual(self.train.workers.count(), 2)

    def test_train_start_end_time_logic(self):
        self.train.start_time = now()
        self.train.save()
        self.assertIsNotNone(self.train.start_time)
        time.sleep(0.1)
        self.train.end_time = now()
        self.train.save()
        self.assertIsNotNone(self.train.end_time)

        self.assertLess(self.train.start_time, self.train.end_time)


class ApprovalModelTest(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create(username="approver", role="auditor")
        self.approval = Approval.objects.create(
            worker=self.worker, status=True, comments="Initial approval"
        )

    def test_approval_string_representation(self):
        self.assertEqual(str(self.approval), "True")

    def test_approval_time_is_set_on_creation(self):
        self.assertIsNotNone(self.approval.time)

    def test_approval_comments_nullable(self):
        approval_no_comment = Approval.objects.create(worker=self.worker, status=False)
        self.assertIsNone(approval_no_comment.comments)

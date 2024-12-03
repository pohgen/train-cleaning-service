from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Worker
from cleaning.models import Train, Approval


class WorkerAdminTest(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.client.login(username="admin", password="adminpass")
        self.worker = Worker.objects.create(username="worker1", role="cleaner")

    def test_worker_admin_list_display(self):
        url = reverse("admin:accounts_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.worker.username)
        self.assertContains(response, self.worker.role)

    def test_worker_admin_search(self):
        url = reverse("admin:accounts_worker_changelist")
        response = self.client.get(url + "?q=worker1")
        self.assertContains(response, self.worker.username)
        self.assertNotContains(response, "nonexistentuser")

    def test_worker_admin_add_role_field(self):
        url = reverse("admin:accounts_worker_add")
        response = self.client.get(url)
        self.assertContains(response, 'name="role"')

    def test_worker_admin_add_info_fields(self):
        url = reverse("admin:accounts_worker_add")
        response = self.client.get(url)
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')


class TrainAdminTest(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.client.login(username="admin", password="adminpass")
        self.train = Train.objects.create(name="78-002", cleaning_type="SP2", status="completed")

    def test_train_admin_list_display(self):
        url = reverse("admin:cleaning_train_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.train.name)
        self.assertContains(response, self.train.cleaning_type)
        self.assertContains(response, self.train.status)

    def test_train_admin_filter(self):
        url = reverse("admin:cleaning_train_changelist")
        response = self.client.get(url + "?name=78-002")
        self.assertContains(response, self.train.name)

    def test_train_admin_search(self):
        url = reverse("admin:cleaning_train_changelist")
        response = self.client.get(url + "?q=78-002")
        self.assertContains(response, self.train.name)

    def test_train_admin_ordering(self):
        url = reverse("admin:cleaning_train_changelist")
        response = self.client.get(url)
        trains = response.context_data['cl'].result_list
        self.assertEqual(trains[0], self.train)


class ApprovalAdminTest(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.client.login(username="admin", password="adminpass")
        self.train = Train.objects.create(name="78-002", cleaning_type="SP2", status="completed")
        self.approval = Approval.objects.create(worker=self.superuser, status=True)
        self.train.approval = self.approval

    def test_approval_admin_display(self):
        url = reverse("admin:cleaning_approval_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.approval.status)

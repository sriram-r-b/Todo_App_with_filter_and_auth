from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Task

class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_task_creation(self):
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task description',
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.status, Task.Status.Todo)
        self.assertEqual(task.user, self.user)

    def test_task_status_update(self):
        task = Task.objects.create(
            user=self.user,
            title='Task to be updated',
        )
        task.status = Task.Status.Done
        task.save()
        self.assertEqual(task.status, Task.Status.Done)

    def test_task_ordering(self):
        task1 = Task.objects.create(user=self.user, title='Task 1')
        task2 = Task.objects.create(user=self.user, title='Task 2')
        tasks = Task.objects.all()
        self.assertEqual(list(tasks), [task1, task2])

    def tearDown(self):
        self.user.delete()
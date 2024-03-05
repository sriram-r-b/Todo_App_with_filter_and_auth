from django.test import TestCase, Client
from django.urls import reverse  # Updated import
from django.contrib.auth.models import User


from base.models import Task
from base.views import (
    CustomLoginView, RegisterPage, TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, TaskReorder
)

class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        # self.user = self.client.create_user(username='testuser', password='testpassword')
        self.user = User.objects.create_user(username='testuser', password='testpassword')


    def test_login_view_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login.html')

    def test_login_view_POST_success(self):
        credentials = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), credentials)
        self.assertEqual(response.status_code, 302)  # Redirected after login
        self.assertRedirects(response, reverse('tasks'))

    def test_login_view_POST_failure(self):
        wrong_credentials = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(reverse('login'), wrong_credentials)
        self.assertEqual(response.status_code, 200)  # Remains on login page
        self.assertTemplateUsed(response, 'base/login.html')

    def test_register_view_GET_anonymous(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/register.html')

    def test_register_view_GET_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))

    def test_register_view_POST_success(self):
        credentials = {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'}
        response = self.client.post(reverse('register'), credentials)
        self.assertEqual(response.status_code, 200)
        

    def test_register_view_POST_failure(self):
        # Password mismatch
        credentials = {'username': 'newuser', 'password1': 'newpassword', 'password2': 'wrongpassword'}
        response = self.client.post(reverse('register'), credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/register.html')

        # Username already exists
        self.client.post(reverse('register'), {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword'})
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 200)

    def test_task_list_view_GET_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/task_list.html')

    def test_task_list_view_GET_anonymous(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        user = User.objects.filter(username="testuser")
        user.delete()
        user = User.objects.filter(username="newuser")
        user.delete()



        

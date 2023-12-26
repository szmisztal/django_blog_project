from django.test import TestCase, SimpleTestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.utils import timezone
from .forms import EntryForm, LoginForm, RegisterForm
from .models import Entry
from . import views

class FormsTestCase(TestCase):

    def test_entry_form_valid_data(self):
        form = EntryForm(data = {"title": "Test Title", "text": "Test Text"})
        self.assertTrue(form.is_valid())

    def test_entry_form_invalid_data(self):
        form = EntryForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_login_form_valid_data(self):
        form = LoginForm(data = {"username": "testuser", "password": "testpassword"})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        form = LoginForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_register_form_valid_data(self):
        form = RegisterForm(data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "testpassword123",
            "password2": "testpassword123"
        })
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_data(self):
        form = RegisterForm(data = {})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class EntryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        testuser = User.objects.create_user(username = "testuser", password = "testpass")
        testuser.save()

        Entry.objects.create(
            title = "Test Entry",
            publication_date = timezone.now(),
            text = "This is a test entry text.",
            author = testuser
        )

    def test_title_content(self):
        entry = Entry.objects.get(id = 1)
        expected_object_name = f"{entry.title}"
        self.assertEqual(expected_object_name, "Test Entry")

    def test_publication_date(self):
        entry = Entry.objects.get(id = 1)
        expected_date = timezone.now().date()
        self.assertEqual(entry.publication_date, expected_date)

    def test_text_content(self):
        entry = Entry.objects.get(id = 1)
        expected_object_text = f"{entry.text}"
        self.assertEqual(expected_object_text, "This is a test entry text.")

    def test_author(self):
        entry = Entry.objects.get(id = 1)
        expected_author = f"{entry.author}"
        self.assertEqual(expected_author, "testuser")

    def test_max_length(self):
        entry = Entry.objects.get(id = 1)
        title_max_length = entry._meta.get_field("title").max_length
        text_max_length = entry._meta.get_field("text").max_length
        self.assertEqual(title_max_length, 50)
        self.assertEqual(text_max_length, 1000)


class TestUrls(SimpleTestCase):

    def test_homepage_url_resolves(self):
        url = reverse("homepage")
        self.assertEquals(resolve(url).func.view_class, views.HomepageView)

    def test_register_url_resolves(self):
        url = reverse("register")
        self.assertEquals(resolve(url).func, views.sign_up)

    def test_login_url_resolves(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func, views.sign_in)

    def test_logout_url_resolves(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func, views.sign_out)

    def test_entry_detail_url_resolves(self):
        url = reverse("entry_detail", args = [1])
        self.assertEquals(resolve(url).func.view_class, views.EntryDetailView)

    def test_entries_list_url_resolves(self):
        url = reverse("entries_list")
        self.assertEquals(resolve(url).func.view_class, views.EntryListView)

    def test_entry_create_url_resolves(self):
        url = reverse("entry_create")
        self.assertEquals(resolve(url).func.view_class, views.EntryCreateView)

    def test_entry_update_url_resolves(self):
        url = reverse("entry_update", args = [1])
        self.assertEquals(resolve(url).func.view_class, views.EntryUpdateView)

    def test_entry_delete_url_resolves(self):
        url = reverse("entry_delete", args = [1])
        self.assertEquals(resolve(url).func.view_class, views.EntryDeleteView)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.homepage_url = reverse("homepage")
        self.entry_detail_url = reverse("entry_detail", args = [1])
        self.user = User.objects.create_user(username = "testuser", password = "testpass")
        self.entry = Entry.objects.create(
            title = "Test Title",
            publication_date = "2023-12-25",
            text = "Test Text",
            author = self.user
        )

    def test_homepage_view(self):
        response = self.client.get(self.homepage_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage.html")

    def test_entry_detail_view(self):
        response = self.client.get(self.entry_detail_url)
        self.assertEquals(response.status_code, 302)
        self.client.login(username = "testuser", password = "testpass")
        response = self.client.get(self.entry_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "entry_detail.html")

    def test_entry_list_view(self):
        self.client.login(username = "testuser", password = "testpass")
        response = self.client.get(reverse("entries_list"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "entries_list.html")

    def test_entry_create_view(self):
        self.client.login(username = "testuser", password = "testpass")
        response = self.client.post(reverse("entry_create"), {
            "title": "New Test Title",
            "publication_date": "2023-12-26",
            "text": "New Test Text",
        })
        self.assertEquals(response.status_code, 302)

    def test_entry_update_view(self):
        self.client.login(username = "testuser", password = "testpass")
        response = self.client.post(reverse("entry_update", args = [self.entry.id]), {
            "title": "Updated Test Title",
            "publication_date": "2023-12-27",
            "text": "Updated Test Text",
        })
        self.assertEquals(response.status_code, 302)

    def test_entry_delete_view(self):
        self.client.login(username = "testuser", password = "testpass")
        response = self.client.post(reverse("entry_delete", args = [self.entry.id]))
        self.assertEquals(response.status_code, 302)
        entries_count = Entry.objects.filter(id = self.entry.id).count()
        self.assertEquals(entries_count, 0)


class AuthViewsTestCase(TestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.test_user = User.objects.create_user(username = "testuser", password = "testpass")

    def test_sign_up(self):
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "newtestpass",
            "password2": "newtestpass",
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_sign_in(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpass",
        })
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("homepage"))

    def test_sign_out(self):
        self.client.login(username = "testuser", password = "testpass")
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

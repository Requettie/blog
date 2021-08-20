from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="hotsauce"
        )
        self.post = Post.objects.create(
            title="A title",
            body="A body",
            author=self.user
        )

    def test_string_representation(self):
        post = Post(title="A sample title")
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", "A title")
        self.assertContains(f"{self.post.body}", "A body")
        self.assertTemplateUsed(f"{self.post.author}", "testuser")

    def test_post_list_view(self):
        response = self.client.get(reverse("home"))
        self.assert(response.status_code, 200)
        self.assertContains(response, "A body")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detail_view(self):
        response = self.client.get("/post/1/")
        not_found_response = self.client.get("/post/1000")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "A title")
        self.assertTemplateUsed(response, "post_detail.html")

    
    def test_get_absolute_url(self):
            self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_post_detail_view(self):
        response = self.client.post(reverse("post_new"),{
            "title":"New title",
            "body": "New body",
            "author": self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New title")
        self.assertEqual(Post.objects.last().body, "New body")

    def test_post_update_view(self):
        response = self.client.post(reverse("post_edit", args="1"),{
            "title":"Update title",
            "body": "Updated body",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Updated title")

    def test_post_delete_view(self):
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)

    
# Create your tests here.

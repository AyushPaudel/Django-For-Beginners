from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email ='test@mail.com',
            password='secret',
        )
        self.post = Post.objects.create(
            title='A good title',
            body ='Nice content',
            author = self.user,
        )

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Nice content')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertContains(response, 'Nice content')

        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'),
                                   {
                                       'title': 'New title',
                                       'body': 'New text',
                                       'author': self.user,

                                   })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New title")
        self.assertTemplateUsed(response, 'post_new.html')

    def text_post_update_view(self):
        response = self.client.post(reverse('post_edit', args=1),
        {
            "title":"Updated",
            "body": "updated body",

        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Updated")
        self.assertContains(response, "updated body")
        self.assertTemplateUsed(response, 'post_edit.html')

    def text_post_delete_view(self):
        response = self.client.get(
            reverse('post_delete', args=1))
        self.assertEqual(response.status_code, 200)





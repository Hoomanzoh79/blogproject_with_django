from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from django.shortcuts import reverse


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Hooman')
        cls.post1 = Post.objects.create(
            title='post1',
            text='This is post1',
            author=cls.user,
            status=Post.STATUS_CHOICES[0][0]
        )
        cls.post2 = Post.objects.create(
            title='post2',
            text='This is a draft post',
            author=cls.user,
            status=Post.STATUS_CHOICES[1][0],
        )

    def test_posts_list_view_by_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_posts_list_view_by_name(self):
        response = self.client.get(reverse('posts_list'))

    def test_str_post_equals_title(self):
        self.assertEqual(str(self.post1), self.post1.title)

    def test_post_title(self):
        self.assertEqual(self.post1.title, 'post1')

    def test_draft_post_not_showed(self):
        response = self.client.get(reverse('posts_list'))
        self.assertNotContains(response, self.post2.title)
        self.assertContains(response, self.post1.title)

    def test_post_detail_by_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_title_on_post_detail(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_404_if_id_not_found(self):
        response = self.client.get(reverse('post_detail', args=[1000]))
        self.assertEqual(response.status_code, 404)

    def test_post_create(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'Some title',
            'text': 'A random text',
            'author': self.user.id,
            'status': 'pub',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Some title')
        self.assertEqual(Post.objects.last().text, 'A random text')

    def test_post_update(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'post2 edited',
            'text': 'Some random text',
            'author': self.user.id,
            'status': 'pub'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'post2 edited')
        self.assertEqual(Post.objects.last().text, 'Some random text')

    def test_post_delete(self):
        response = self.client.post(reverse('post_delete', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)

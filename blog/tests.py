import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Post


class PostMethodTests(TestCase):

    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(pub_date=time)
        self.assertEqual(future_post.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_post = Post(pub_date=time)
        self.assertEqual(old_post.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for posts whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_post = Post(pub_date=time)
        self.assertEqual(recent_post.was_published_recently(), True)


def create_post(title, days):
    """
    Creates a posts with the given `title` published the given
    number of `days` offset to now (negative for posts published
    in the past, positive for posts that have yet to be published).
    """
    author = 'aaa'
    author_email = 'example@example.com'
    summary = 'summary of the post'
    content = 'main body of the post'
    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(title=title, author=author, author_email=author_email, summary=summary,
                               content=content, pub_date=time)


class PostViewTests(TestCase):

    def test_index_view_with_no_posts(self):
        """
        If no posts exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_index_view_with_a_past_post(self):
        """
        Posts with a pub_date in the past should be displayed on the
        index page.
        """
        create_post(title="Past post.", days=-30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post.>']
        )

    def test_index_view_with_a_future_post(self):
        """
        Posts with a pub_date in the future should not be displayed on
        the index page.
        """
        create_post(title="Future post.", days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, "No posts are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_post_list'], [])

    def test_index_view_with_future_post_and_past_post(self):
        """
        Even if both past and future posts exist, only past posts
        should be displayed.
        """
        create_post(title="Past post.", days=-30)
        create_post(title="Future post.", days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post.>']
        )

    def test_index_view_with_two_past_post(self):
        """
        The posts index page may display multiple posts.
        """
        create_post(title="Past post 1.", days=-30)
        create_post(title="Past post 2.", days=-5)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(
            response.context['latest_post_list'],
            ['<Post: Past post 2.>', '<Post: Past post 1.>']
        )


class PostIndexDetailTests(TestCase):

    def test_detail_view_with_a_future_post(self):
        """
        The detail view of a post with a pub_date in the future should
        return a 404 not found.
        """
        future_post = create_post(title='Future Post.', days=5)
        response = self.client.get(reverse('blog:detail', args=(future_post.id, future_post.slug)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_post(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_post = create_post(title='Past Post.', days=-5)
        response = self.client.get(reverse('blog:detail', args=(past_post.id, past_post.slug)))
        self.assertContains(response, past_post.title, status_code=200)
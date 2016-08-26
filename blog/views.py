import random
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import RequestContext
from django.views.generic import MonthArchiveView, YearArchiveView, ListView
from django.utils import timezone

from .forms import CommentForm
from .models import Post, Comment

# Create your views here.

class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'
    paginate_by = 5

    def get_queryset(self):
        """
        Return the last published questions (not including those set to be
        published in the future).
        """
        return Post.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


def detail(request, post_id, slug):
    posts = Post.objects.filter(pub_date__lte=timezone.now())
    post = get_object_or_404(posts, pk=post_id, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(request.path)
    return render(request, 'blog/detail.html',
                  {
                      'post': post,
                      'form': form,
                  })


class PostMonthArchiveView(MonthArchiveView):
    template_name = 'blog/archive.html'
    context_object_name = 'monthly_post_list'
    queryset = Post.objects.all()
    date_field = "pub_date"
    allow_future = True


class ArticleYearArchiveView(YearArchiveView):
    template_name = 'blog/article_month_archive.html'
    queryset = Post.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True


# #####################################

def hello(request):
    rand = random.randrange(0, 100)
    return HttpResponse(str(rand))


# def index(request):
#     latest_post_list = Post.objects.order_by('-pub_date')[:5]
#     context = {'latest_post_list': latest_post_list}
#     return render(request, 'blog/blog_index.html', context)
#
# def detail(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     return render(request, 'blog/blog_detail.html', {'post': post})

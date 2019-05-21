from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        # 表单被提交,request.POST中包含表单数据
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #验证表单数据
            cd = form.cleaned_data
            #发送邮件……
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title,post_url,cd['name'],cd['comment'])
            send_mail(subject, message, 'xzd19990526@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
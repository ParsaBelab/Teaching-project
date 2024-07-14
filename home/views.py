from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.http import JsonResponse
from home.forms import CommentForm
from posts.models import Post, Category, Comment
from django.core.paginator import Paginator


class HomeView(View):
    def get(self, request):
        post_list = Post.objects.all()
        paginator = Paginator(post_list, 1)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        categories = Category.objects.all()
        recent_posts = Post.objects.all()[:3]
        return render(request, 'home/index.html',
                      {'posts': posts, 'categories': categories, 'recent_posts': recent_posts})


class PostDetailView(View):
    form_class = CommentForm
    template_name = 'home/post-detail.html'
    post_instance = None

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:register')
        elif not request.user.is_premium:
            messages.error(request, 'برای دسترسی به این صفحه لطفا اشتراک تهیه نمایید', 'error')
            return redirect('Home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id, slug):
        form = self.form_class()
        post = self.post_instance
        rposts = post.get_related_posts_by_category()
        categories = Category.objects.all()
        comments = Comment.objects.filter(post=post, is_reply=False)
        return render(request, self.template_name, {'post': post, 'rposts': rposts, 'comments': comments, 'form': form , 'categories':categories})

    def post(self, request, post_id, slug):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.post_instance
            comment.author = request.user
            comment.save()
        return redirect('Home:post-detail', self.post_instance.id, self.post_instance.slug)


class AddReplyView(View):
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:register')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, slug, post_id, comment_id):
        form = self.form_class(request.POST)
        comment = get_object_or_404(Comment, pk=comment_id)
        post = get_object_or_404(Post, pk=post_id, slug=slug)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.parent = comment
            reply.is_reply = True
            reply.author = request.user
            reply.save()
        return redirect('Home:post-detail', post.id, post.slug)


class ToggleFavoriteView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post in request.user.favorites.all():
            request.user.favorites.remove(post)
            action = 'unliked'
        else:
            request.user.favorites.add(post)
            action = 'liked'
        return JsonResponse({'action': action})

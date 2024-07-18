from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Category


class CategoryListView(View):
    template_name = 'posts/categories.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})


class CategoryDetailView(View):
    template_name = 'posts/category.html'

    def get(self, request, cat_id):
        category = get_object_or_404(Category, id=cat_id)
        post_list = category.posts.all()
        paginator = Paginator(post_list, 1)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        return render(request, self.template_name, {'posts': posts, 'category': category})

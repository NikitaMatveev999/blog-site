from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from .forms import PostForm, SignUpForm
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from rest_framework import generics
from .serializers import PostSerializer


class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def favourite_list(request):
    user = request.user
    favourite_posts = user.favourite.all()
    context = {'favourite_posts': favourite_posts}
    return render(request, 'posts/favourite.html', context)


def add_like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('detail', args=[str(pk)]))


def add_favourite_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(reverse('detail', args=[str(pk)]))


class SearchResultsView(ListView):
    model = Post
    template_name = "posts/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        find_posts = Post.objects.filter(
            Q(body__icontains=query) | Q(title__icontains=query)
        )
        return find_posts


class HomeView(ListView):
    paginate_by = 3
    model = Post
    template_name = 'posts/index.html'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        context = super(HomeView, self).get_context_data()
        context['categories'] = categories
        return context


def category_view(request, cat_id):
    posts = Post.objects.filter(category_id=cat_id)
    categories = Category.objects.all()
    return render(request, 'posts/categories.html', {'posts': posts,
                                                     'categories': categories})


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        categories = Category.objects.all()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        favourite_post = False
        if stuff.favourite.filter(id=self.request.user.id).exists():
            favourite_post = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        context['favourite'] = favourite_post
        context['categories'] = categories
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/add_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy('home')


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/update_post.html'
    fields = ['body']


class RegistrationView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/registration.html'
    success_url = 'login'

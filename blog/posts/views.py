from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from .forms import PostForm, SignUpForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from rest_framework import generics
from .serializers import PostSerializer


class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class FavouriteListView(ListView):
    model = Post
    template_name = 'posts/favourite.html'
    context_object_name = 'favourite_posts'

    def get_queryset(self):
        return self.request.user.favourite.all()


class AddLikeView(View):
    def post(self, request, pk):
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('detail', args=[str(pk)]))


class AddFavouriteView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
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


class CategoryView(ListView):
    paginate_by = 3
    model = Post
    template_name = 'posts/categories.html'
    context_object_name = 'posts'

    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        return Post.objects.filter(category_id=cat_id)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        categories = Category.objects.all()
        liked = stuff.likes.filter(id=self.request.user.id).exists()
        favourite_post = stuff.favourite.filter(id=self.request.user.id).exists()
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

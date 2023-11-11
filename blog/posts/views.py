from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category, Comment
from .forms import PostForm, SignUpForm, CommentForm
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
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super(RegistrationView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        try:
            new_user = authenticate(username=username, password=password)
            if new_user is not None:
                login(self.request, new_user)
            else:
                messages.error(self.request, 'Ошибка регистрации. Попробуйте еще раз.')
                return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, 'Ошибка регистрации. Попробуйте еще раз.')
        return valid


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if 'parent_id' in self.request.GET:
            parent_id = self.request.GET['parent_id']
            form.instance.parent = get_object_or_404(Comment, pk=parent_id)
        else:
            form.instance.parent = None
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})

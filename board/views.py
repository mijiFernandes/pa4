from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from board.models import Post

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin
from django.conf import settings


#--- ListView
class PostLV(ListView):
    model = Post
    template_name = 'board/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2


#--- DetailView
class PostDV(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'content']
    initial = {'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('board:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'board/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'content']
    success_url = reverse_lazy('board:index')


class PostDeleteView(OwnerOnlyMixin, DetailView):
    model = Post
    success_url = reverse_lazy('board:index')


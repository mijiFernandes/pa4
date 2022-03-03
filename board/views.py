from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from board.froms import CommentForm
from board.models import Post, Comment

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]

        form = CommentForm()
        post = get_object_or_404(Post, slug=slug)
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(slug=self.kwargs['slug'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=request.user, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            try:
                points = settings.POINTS_SETTINGS['CREATE_ARTICLE']
            except KeyError:
                points = 0
            request.user.modify_points(points)
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


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


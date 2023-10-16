from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm
from django.utils.text import slugify


class HomeView(View):
    template_name = "home/index.html"

    def get(self, request):
        posts = Post.objects.all()

        context = {"posts": posts}
        return render(request, self.template_name, context)

    def post(self, request):
        return render(request, self.template_name)


class PostDetailView(View):
    template_name = "home/post_detail.html"

    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)

        context = {"post": post}

        return render(request, self.template_name, context)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)

        if post.user.id == request.user.id:
            post.delete()

            messages.success(request, "Post delete successfully.", "success")

        else:
            messages.error(request, "You can't delete this post.", "danger")

        return redirect("home:home")


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = "home/update.html"

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance

        if not post.user.id == request.user.id:
            messages.error(request, "You can't update this post", "danger")
            return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)

        context = {"form": form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.save()

            messages.success(
                request, "The post has been updated successfully.", "success"
            )

            return redirect("home:post-detail", new_post.id, new_post.slug)

        context = {"form": form}
        return render(request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = "home/create.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.user = request.user
            new_post.save()

            messages.success(
                request, "The new post has been created successfully.", "success"
            )

            return redirect("home:post-detail", new_post.id, new_post.slug)

from django.shortcuts import render
from django.views.generic import ListView
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.views import View
from .forms import CommentForm
from django.urls import reverse
from django.core.paginator import Paginator

# Create your views here.


class PostListView(ListView):
    template_name = "blog/blogs.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"
    paginate_by = 6  # Number of posts per page

    def get_context_data(self, **kwargs):
        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))

        context = super().get_context_data(**kwargs)
        context["number"] = len_cart
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj
    

class PostDetails(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))

        context = {
            "post": post,
            "number": len_cart,
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)
        print(comment_form.is_valid())
        if comment_form.is_valid():
            
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        else:
            print(comment_form.errors)
        
        len_cart = 0
        if self.request.session.get("cart_clothes") is not None:
            len_cart = len(self.request.session.get("cart_clothes"))
       
        context = {
            "post": post,
            "number": len_cart,
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }
        return render(request, "blog/post-detail.html", context)

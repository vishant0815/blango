from django.shortcuts import render
from django.utils import timezone
from blog.models import Post
from django.shortcuts import redirect
from blog.forms import CommentForm
import logging


logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
  posts = (
    Post.objects.filter(published_at__lte=timezone.now())
    .select_related("author")
    .defer("created_at", "modified_at")
  )
  logger.debug("Got %d posts", len(posts))
  return render(request, "blog/index.html", {"posts": posts})
  
def post_detail(request, slug):
  if request.user.is_active:
    if request.method == "POST":
      comment_form = CommentForm(request.POST)

      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.content_object = post
        comment.creator = request.user
        comment.save()
        return redirect(request.path_info)
    else:
        comment_form = CommentForm()
  else:
      comment_form = None
  return render(
      request, "blog/post-detail.html", {"post": post, "comment_form": comment_form}
    )

def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])

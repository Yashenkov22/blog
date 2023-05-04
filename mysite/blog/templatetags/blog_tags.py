from django import template
from blog.models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_post(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_post': latest_posts}

@register.simple_tag
def get_most_comment_posts(count=5):
    return Post.published.annotate(total_comment=Count('comments')).order_by('-total_comment')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
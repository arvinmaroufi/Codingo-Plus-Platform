from django.urls import path, include
from .router import BlogRouter, MainCategoryRouter, SubCategoryRouter, TagRouter, CommentReplyRouter


app_name = 'Blogs'


blog_router = BlogRouter()
main_category_router = MainCategoryRouter()
sub_category_router = SubCategoryRouter()
tag_router = TagRouter()
comment_reply_router = CommentReplyRouter()

urlpatterns = [
    path('blogs/', include(blog_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
    path('tags/', include(tag_router.get_urls())),
    path('replies/', include(comment_reply_router.get_urls())),
]

from django.urls import path, include
from .router import MainCategoryRouter, SubCategoryRouter, TagRouter, BookRouter, CommentReplyRouter


app_name = 'Books'


main_category_router = MainCategoryRouter()
sub_category_router = SubCategoryRouter()
tag_router = TagRouter()
book_router = BookRouter()
comment_reply_router = CommentReplyRouter()


urlpatterns = [
    path('main-categories/', include(main_category_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
    path('tags/', include(tag_router.get_urls())),
    path('books/', include(book_router.get_urls())),
    path('replies/', include(comment_reply_router.get_urls())),
]

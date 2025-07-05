from django.urls import path, include
from .router import MainCategoryRouter, SubCategoryRouter, TagRouter, PodcastRouter, CommentReplyRouter


app_name = 'Podcasts'
main_category_router = MainCategoryRouter()
sub_category_router = SubCategoryRouter()
tag_router = TagRouter()
podcast_router = PodcastRouter()
comment_reply_router = CommentReplyRouter()


urlpatterns = [
    path('main-categories/', include(main_category_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
    path('tags/', include(tag_router.get_urls())),
    path('podcasts/', include(podcast_router.get_urls())),
    path('replies/', include(comment_reply_router.get_urls())),
]

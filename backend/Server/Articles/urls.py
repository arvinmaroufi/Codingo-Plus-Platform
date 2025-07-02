from django.urls import path, include
from .router import MainCategoryRouter, SubCategoryRouter, TagRouter, AuthorRouter, ArticleContentRouter


app_name = 'Articles'


main_category_router = MainCategoryRouter()
sub_category_router = SubCategoryRouter()
tag_router = TagRouter()
author_router = AuthorRouter()
article_content_router = ArticleContentRouter()


urlpatterns = [
    path('main-categories/', include(main_category_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
    path('tags/', include(tag_router.get_urls())),
    path('authors/', include(author_router.get_urls())),
    path('article-contents/', include(article_content_router.get_urls())),
]

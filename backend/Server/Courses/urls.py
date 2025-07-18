from django.urls import path, include
from . import routers, views


app_name = "Courses"


main_category_router = routers.MainCategoryRouter()
sub_category_router = routers.SubCategoryRouter()
tags_router = routers.SubCategoryRouter()
course_router = routers.CourseRouter()
course_faqs_router = routers.CourseFaqRouter()
course_contents_router = routers.CourseContentRouter()
course_chapters_router = routers.CourseChapterRouter()
course_sessions_router = routers.CourseSessionRouter()
comments_router = routers.CommentsRouter()
comment_replays_router = routers.CommentsReplayRouter()


urlpatterns = [
    path('main-categories/', include(main_category_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
    path('tags/', include(tags_router.get_urls())),
    path('courses/', include(course_router.get_urls())),
    path('course-faqs/', include(course_faqs_router.get_urls())),
    path('course-contents/', include(course_contents_router.get_urls())),
    path('course-sessions/', include(course_sessions_router.get_urls())),
    path('course-chapters/', include(course_chapters_router.get_urls())),
    path('comments/', include(comments_router.get_urls())),
    path('comment-replays/', include(comment_replays_router.get_urls())),
    path('categories/', views.CategoriesList.as_view())
]

from django.urls import path, include
from . import routers



app_name = "Courses"


main_category_router = routers.MainCategoryRouter()
sub_category_router = routers.SubCategoryRouter()
tags_router = routers.SubCategoryRouter()
course_router = routers.CourseRouter()
course_faqs_router = routers.CourseFaqRouter()
course_contents_router = routers.CourseContentRouter()


urlpatterns = [
    path('main-categories/', include(main_category_router.get_urls())),
    path('sub-categories/', include(sub_category_router.get_urls())),
    path('tags/', include(tags_router.get_urls())),
    path('courses/', include(course_router.get_urls())),
    path('course-faqs/', include(course_faqs_router.get_urls())),
    path('course-contents/', include(course_contents_router.get_urls())),
]

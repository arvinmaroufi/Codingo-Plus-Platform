import django_filters
from django_filters import rest_framework as filters
from .models import Course
from .models import SubCategory, MainCategory


class CourseFilter(filters.FilterSet):
    level_status = filters.ChoiceFilter(field_name="level_status", choices=Course.Level.choices)
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    sub_category = filters.ModelChoiceFilter(field_name="category", queryset=SubCategory.objects.all())
    main_category = filters.ModelChoiceFilter(field_name="category__parent", queryset=MainCategory.objects.all())
    payment_status = filters.ChoiceFilter(field_name="payment_status", choices=Course.Payment.choices)
    course_status= filters.ChoiceFilter(field_name="status", choices=Course.Status.choices)

    class Meta:
        model  = Course
        # Meta.fields is optional when you declare custom filters,
        # but you could list them here for clarity:
        fields = [
            "level_status", "min_price", "max_price",
            "payment_status", "course_status",
            "sub_category", "main_category",
        ]

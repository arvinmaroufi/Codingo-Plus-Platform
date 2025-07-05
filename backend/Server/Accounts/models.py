from django.db import models





class UserCourseEnrollment(models.Model):
    course = models.ForeignKey(
        'Courses.Course',
        on_delete=models.CASCADE,
        related_name="user_activated_course"
    )

    user = models.ForeignKey(
        'Users.User',
        on_delete=models.CASCADE,
        related_name="user_activated_course"
    )

    is_active = models.BooleanField(default=False)

    purchased_on = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User course enrollment"
        verbose_name_plural = "Users courses enrollments"
    
    def __str__(self):
        return f"{self.user.username} puchased the {self.course.title}."
    
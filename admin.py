from django.contrib import admin
from .models import Course, CourseMaterial, Enrollment, Quiz

# admin.site.register(Course)
admin.site.register(CourseMaterial)
admin.site.register(Enrollment)
# admin.site.register(Quiz)
class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    inlines = [QuizInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("course", "question", "correct_option", "marks")
    search_fields = ("question",)
    list_filter = ("course",)




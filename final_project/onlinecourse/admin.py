from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


class LessonsInline(admin.StackedInline):
    model = Lesson
    extra = 5


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonsInline, QuestionInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)

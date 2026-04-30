from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission


def index(request):
    courses = Course.objects.all()
    return render(request, "onlinecourse/index.html", {"courses": courses})


def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    if user.is_authenticated:
        enrollment, created = Enrollment.objects.get_or_create(user=user, course=course)
        return HttpResponseRedirect(reverse("onlinecourse:detail", args=(course.id,)))
    return HttpResponseRedirect(reverse("onlinecourse:index"))


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = get_object_or_404(Enrollment, user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    selected_ids = request.POST.getlist("choice")
    selected_choices = Choice.objects.filter(id__in=selected_ids)
    submission.choices.set(selected_choices)
    submission.save()
    return HttpResponseRedirect(
        reverse("onlinecourse:show_exam_result", args=(course.id, submission.id))
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = submission.choices.values_list("id", flat=True)
    total_score = 0
    for question in course.question_set.all():
        if question.is_get_score(selected_ids):
            total_score += question.grade
    return render(request, "onlinecourse/exam_result.html", {
        "course": course,
        "submission": submission,
        "selected_ids": selected_ids,
        "total_score": total_score,
    })

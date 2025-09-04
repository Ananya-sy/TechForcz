from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse

from .models import Course, CourseMaterial, Enrollment, Quiz, Certificate ,EnrollmentRequest
from .forms import UploadMaterialForm , EnrollmentRequestForm


# -------------------------
# Public Pages
# -------------------------
def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def home(request):
    courses = Course.objects.all()[:3]   # get only 2 courses
    return render(request, 'home.html', {'courses': courses})



# -------------------------
# Courses
# -------------------------
def course_list(request):
    query = request.GET.get("q")
    if query:
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()
    return render(request, 'course_list.html', {"courses": courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = CourseMaterial.objects.filter(course=course)  # show files
    return render(request, 'course_detail.html', {"course": course, "materials": materials})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect("dashboard")


@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, "dashboard.html", {"enrollments": enrollments})


# -------------------------
# Quiz
# -------------------------
@login_required
def take_quiz(request, course_id):
    quiz = get_object_or_404(Quiz, course_id=course_id)
    return render(request, 'quiz.html', {"quiz": quiz})


# -------------------------
# Certificates
# -------------------------
@login_required
def certificate_view(request, course_id):
    certificate = get_object_or_404(Certificate, course_id=course_id, user=request.user)
    return render(request, 'certificate.html', {"certificate": certificate})


@login_required
def certificate_pdf(request, course_id):
    return HttpResponse("PDF download will be here.")


# -------------------------
# Upload Content (PDFs, Videos, etc.)
# -------------------------
@login_required
def upload_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = UploadMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course  # attach course automatically
            material.save()
            return redirect("course_detail", course_id=course.id)
    else:
        form = UploadMaterialForm()

    return render(request, "upload_content.html", {"form": form, "course": course})


# -------------------------
# Checkout / Payment
# -------------------------
@login_required
def checkout(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "checkout.html", {"course": course})


@login_required
def buy_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        payment_successful = True  # Replace with real payment gateway logic
        if payment_successful:
            return redirect('payment_success', course_id=course.id)
        else:
            return render(request, 'payment_failed.html', {'course': course})

    return redirect('checkout', course_id=course.id)


@login_required
def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user

    Enrollment.objects.get_or_create(student=student, course=course, defaults={"progress": 0.0})
    return redirect("dashboard")


# -------------------------
# Auth
# -------------------------
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def register_view(request):
    return render(request, "register.html")


def certificate_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "certificate.html", {
        "user": request.user,
        "course": course,
    })

def enroll_now(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        form = EnrollmentRequestForm(request.POST)
        if form.is_valid():
            enrollment_request = form.save(commit=False)
            enrollment_request.course = course
            enrollment_request.save()
            return render(request, 'thank_you.html')  # Create this template for the thank you message
    else:
        form = EnrollmentRequestForm()
    return render(request, 'enroll_now.html', {'form': form, 'course': course})
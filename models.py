from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('cloud', 'Cloud'),
            ('ai', 'AI/ML'),
            ('networking', 'Networking'),
            ('security', 'Security'),
            ('programming', 'Programming'),
        ],
        default='programming'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # <--- Add this
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="materials/")  # PDF or MP4
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)  # % based on quiz score

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1)  # e.g., 'a', 'b', 'c', 'd'
    marks = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.course.title} - {self.question[:50]}"
    
class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")  # Pending/Success/Failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.status})"
    
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    issued_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.user.username} - {self.course.title}"
    
class EnrollmentRequest(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Enrollment Request for {self.name} - {self.course.title}"
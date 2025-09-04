from django.urls import path
from . import views
# from .views import enroll_now  

urlpatterns = [
    path('', views.home, name='home'),                             # Landing page
    path('courses/', views.course_list, name='course_list'),       # List + search/filter
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/', views.course_list, name='courses_list'),

    # Enquiry/Enroll
    # path('enroll/<int:course_id>/', views.enrollment_request, name='enrollment_request'),
     path('enroll_now/<int:course_id>/', views.enroll_now, name='enroll_now'),


    # Dashboard + Quiz
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quiz/<int:course_id>/', views.take_quiz, name='take_quiz'),

    # Upload content (admin/teacher)
    path('upload/<int:course_id>/', views.upload_content, name='upload_content'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("register/", views.register_view, name="register"),

    # Certificate
    path("certificate/<int:course_id>/", views.certificate_view, name="certificate"),
    path('certificate/<int:course_id>/pdf/', views.certificate_pdf, name='certificate_pdf'),

    # Static Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

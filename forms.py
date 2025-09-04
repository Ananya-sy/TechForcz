from django import forms
from .models import CourseMaterial, EnrollmentRequest

class UploadMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'file']  # ✅ removed 'course', we handle in view
        
class EnrollmentRequestForm(forms.ModelForm):
    class Meta:
        model = EnrollmentRequest
        fields = ['name', 'phone', 'email']
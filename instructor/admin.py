from django.contrib import admin
from .models import *


class CreateAssessmentAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'marks')
    
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj and obj.question_type == 'MCQ':
            return ['question_text', 'question_type', 'marks', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        elif obj and obj.question_type == 'SUB':
            return ['question_text', 'question_type', 'marks', 'answer_text']
        return fields
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.question_type == 'MCQ':
            self.exclude = ('answer_text',)
        elif obj and obj.question_type == 'SUB':
            self.exclude = ('option_a', 'option_b', 'option_c', 'option_d', 'correct_option')
        else:
            self.exclude = ()
        return form

admin.site.register(CreateAssessment, CreateAssessmentAdmin)


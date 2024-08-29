from django.contrib import admin
from .models import *


class CreateAssessementAdmin(admin.ModelAdmin):
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

admin.site.register(CreateAssessment, CreateAssessementAdmin)

class MarkAssessmentAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'student_id', 'marks_obtained')
    list_filter = ('assessment__question_type',)
    search_fields = ('student_id', 'assessment__question_text')
    ordering = ('assessment', 'student_id')
    
    fieldsets = (
        (None, {
            'fields': ('assessment', 'student_id', 'student_answer', 'marks_obtained', 'feedback')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        # Marks should only be editable for subjective questions
        if obj and obj.assessment.question_type == 'MCQ':
            return ['marks_obtained']
        return []

admin.site.register(MarkAssessment, MarkAssessmentAdmin)

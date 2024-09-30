from typing import Any
from django import forms
from courses.models import Completion, CompletionFile

class CompletionForm(forms.ModelForm):
    class Meta:
        model = Completion
        fields = ["task", "text"]

    def save(self, commit: bool = ...) -> Any:
        instance =  super().save(commit)

        for file in self.files:
            CompletionFile.objects.create(file=file, completion=instance)

        return instance
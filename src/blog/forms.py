from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "content", "parent"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Optional display name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "required": True}),
            "content": forms.Textarea(attrs={"rows": 5, "placeholder": "Write your comment..."}),
            "parent": forms.HiddenInput(),
        }

    def clean_content(self):
        value = self.cleaned_data["content"].strip()
        if not value:
            raise forms.ValidationError("Comment content cannot be empty.")
        return value

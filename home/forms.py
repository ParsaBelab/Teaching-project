from django import forms
from django.utils.translation import gettext_lazy as _
from posts.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': _('Your Comment')}

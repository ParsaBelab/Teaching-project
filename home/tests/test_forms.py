from django.test import TestCase
from home.forms import CommentForm


class CommentFormTest(TestCase):
    def test_comment_form_valid_data(self):
        form = CommentForm(data={'body': 'This is a test comment'})
        self.assertTrue(form.is_valid())

    def test_comment_form_empty_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('body', form.errors)

    def test_comment_form_label(self):
        form = CommentForm()
        self.assertEqual(form.fields['body'].label, 'Your Comment')

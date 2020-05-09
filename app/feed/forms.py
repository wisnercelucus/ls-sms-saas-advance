from django import forms
from .models import Post
from ckeditor.widgets import CKEditorWidget


class PostModelForm(forms.ModelForm):
	content = forms.CharField(label='', widget=CKEditorWidget(attrs={"placeholder": "Say something", "class": "form-control"}))
	#content = forms.CharField(label='', 
	#            widget=forms.Textarea(
	#                    attrs={"placeholder": "Say something", "class": "form-control"}
	#                ))

	#image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
	class Meta:
		model = Post
		fields = [
		'content',
		"image",
		]


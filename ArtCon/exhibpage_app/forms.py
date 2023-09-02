from django import forms
from .models import Review
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget
from django.utils.safestring import mark_safe


class ReviewForm(forms.ModelForm):
    contents = SummernoteTextField()
    scores = (
        ("0", "☆☆☆☆☆"),
        ("1", "★☆☆☆☆"),
        ("2", "★★☆☆☆"),
        ("3", "★★★☆☆"),
        ("4", "★★★★☆"),
        ("5", "★★★★★"),
    )
    rank = forms.ChoiceField(label="평점", widget=forms.Select(), choices=scores)

    field_order = ["rank", "contents"]

    class Meta:
        model = Review
        fields = ["rank", "contents"]
        # fields = '__all__'
        exclude = (
            "P_id",
            "username",
        )

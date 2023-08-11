from django import forms
from .models import Post, Comment
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget


class BoardWriteForm(forms.ModelForm):
    postname = forms.CharField(
        label="글 제목",
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "placeholder": "제목",
                "class": "form-control mt-1",
                "id": "id_postname",
                "name": "postname",
            }
        ),
        required=True,
    )

    contents = SummernoteTextField()

    genres = ("정극", "정극"), ("코미디", "코미디")
    locations = ("서울", "서울"), ("경상남도", "경상남도")

    tag1 = forms.CharField(label="배우")
    tag2 = forms.ChoiceField(label="장르", widget=forms.Select(), choices=genres)
    tag3 = forms.ChoiceField(label="지역", widget=forms.Select(), choices=locations)

    field_order = ["postname", "tag1", "tag2", "tag3", "contents"]

    class Meta:
        model = Post
        fields = ["postname", "contents", "tag1", "tag2", "tag3"]
        widgets = {
            "contents": forms.Textarea(
                attrs={"class": "form-control mt-1", "id": "id_contents"}
            )
        }

    def clean(self):
        cleaned_data = super().clean()

        postname = cleaned_data.get("postname", "")
        contents = cleaned_data.get("contents", "")
        tag1 = cleaned_data.get("tag1", "")
        tag2 = cleaned_data.get("tag2", "정극")
        tag3 = cleaned_data.get("tag3", "서울")

        if postname == "":
            self.add_error("postname", "글 제목을 입력하세요.")
        elif contents == "":
            self.add_error("contents", "글 내용을 입력하세요.")
        else:
            self.postname = postname
            self.contents = contents
            self.tag1 = tag1
            self.tag2 = tag2
            self.tag3 = tag3


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["contents"]
        # fields = '__all__'
        exclude = (
            "postname",
            "username",
        )

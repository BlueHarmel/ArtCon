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

    options = ("test1", "test1"), ("test2", "test2")

    board_name = forms.ChoiceField(
        label="게시판 선택", widget=forms.Select(), choices=options
    )

    field_order = ["postname", "board_name" "contents"]

    class Meta:
        model = Post
        fields = ["postname", "contents", "board_name"]
        widgets = {
            "contents": forms.Textarea(
                attrs={"class": "form-control mt-1", "id": "id_contents"}
            )
        }

    def clean(self):
        cleaned_data = super().clean()

        postname = cleaned_data.get("postname", "")
        contents = cleaned_data.get("contents", "")
        board_name = cleaned_data.get("board_name", "test1")

        if postname == "":
            self.add_error("postname", "글 제목을 입력하세요.")
        elif contents == "":
            self.add_error("contents", "글 내용을 입력하세요.")
        else:
            self.postname = postname
            self.contents = contents
            self.board_name = board_name


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["contents"]
        # fields = '__all__'
        exclude = (
            "postname",
            "username",
        )

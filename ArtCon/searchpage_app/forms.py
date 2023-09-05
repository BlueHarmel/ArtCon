from django import forms


class CustomCheckboxInput(forms.widgets.CheckboxInput):
    template_name = "custom_checkbox_input.html"


class SearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "(옵션) 전시회 키워드 검색",
            }
        ),
    )
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control form-control-lg my-4",
                "data-placeholder": "날짜 선택",
            }
        ),
    )
    category = forms.MultipleChoiceField(
        choices=[
            ("뮤지컬", "뮤지컬"),
            ("서양음악(클래식)", "서양음악(클래식)"),
            ("복합", "복합"),
            ("무용", "무용"),
            ("대중음악", "대중음악"),
            ("연극", "연극"),
            ("한국음악(국악)", "한국음악(국악)"),
            ("서커스/마술", "서커스/마술"),
            ("대중무용", "대중무용"),
            ("발레", "발레"),
            # 나머지 장르들도 추가
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-check-input", "name": "category"}
        ),
    )

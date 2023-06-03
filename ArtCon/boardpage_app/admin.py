from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Post)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ("contents",)
    list_display = (
        "postname",
        "contents",
        "username",
        "board_name",
        "hits",
        "date",
        "update_dttm",
    )
    list_display_links = list_display

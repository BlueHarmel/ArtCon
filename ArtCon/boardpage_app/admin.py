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
        "tag1",
        "tag2",
        "tag3",
        "hits",
        "date",
        "update_dttm",
    )
    list_display_links = list_display

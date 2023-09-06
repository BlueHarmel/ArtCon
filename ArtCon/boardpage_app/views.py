from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardWriteForm, CommentForm
from .models import Post, Comment
from authpage_app.models import User
from django.views.decorators.http import require_GET, require_POST
from datetime import date, datetime, timedelta


# Create your views here.
def board(request):
    login_session = request.session.get("login_session", "")
    context = {"login_session": login_session}

    tag1_filter = request.GET.get("tag1")
    tag2_filter = request.GET.get("tag2")
    tag3_filter = request.GET.get("tag3")

    posts = Post.objects.all()

    if tag1_filter:
        posts = posts.filter(tag1=tag1_filter)
    if tag2_filter:
        posts = posts.filter(tag2=tag2_filter)
    if tag3_filter:
        posts = posts.filter(tag3=tag3_filter)

    context["posts"] = posts

    return render(request, "boardpage_app/board.html", context)


def write(request):
    login_session = request.session.get("login_session", "")
    context = {"login_session": login_session}

    if request.method == "GET":
        write_form = BoardWriteForm()
        context["forms"] = write_form
        return render(request, "boardpage_app/write.html", context)

    elif request.method == "POST":
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            user_name = request.user
            username = User.objects.filter(username=user_name)[0]
            board = Post(
                postname=write_form.postname,
                contents=write_form.contents,
                username=username,
                tag1=write_form.tag1,
                tag2=write_form.tag2,
                tag3=write_form.tag3,
            )
            board.save()
            return redirect("/board")
        else:
            context["forms"] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context["error"] = value
            return render(request, "boardpage_app/write.html", context)


def board_single(request, pk):
    login_session = request.session.get("login_session", "")
    context = {"login_session": login_session}

    board = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(postname=board)

    context["board"] = board
    context["comments"] = comments

    if board.username.id == login_session:
        context["writer"] = True
    else:
        context["writer"] = False

    response = render(request, "boardpage_app/board_single.html", context)

    # 조회수 기능
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get("hitboard", "_")

    if f"_{pk}_" not in cookie_value:
        cookie_value += f"{pk}_"
        response.set_cookie(
            "hitboard", value=cookie_value, max_age=max_age, httponly=True
        )
        board.hits += 1
        board.save()
    return response


def board_delete(request, pk):
    login_session = request.session.get("user", "")
    board = get_object_or_404(Post, id=pk)
    if board.username.id == login_session:
        board.delete()
        return redirect("/board")
    else:
        return redirect(f"/board/{pk}/")


def board_modify(request, pk):
    login_session = request.session.get("user", "")
    context = {"login_session": login_session}

    board = get_object_or_404(Post, id=pk)
    context["board"] = board

    if board.username.id != login_session:
        return redirect(f"/board/{pk}/")

    if request.method == "GET":
        write_form = BoardWriteForm(instance=board)
        context["forms"] = write_form
        return render(request, "boardpage_app/modify.html", context)

    elif request.method == "POST":
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            board.postname = write_form.postname
            board.contents = write_form.contents
            board.tag1 = write_form.tag1
            board.tag2 = write_form.tag2
            board.tag3 = write_form.tag3

            board.save()
            return redirect("/board")
        else:
            context["forms"] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context["error"] = value
            return render(request, "boardpage_app/modify.html", context)


@require_POST
def likes(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Post, id=pk)

        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect(f"/board/{pk}/")
    return redirect("authpage_app:login")


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.postname = article
            comment.username = request.user
            comment.save()
        else:
            print(comment_form.errors)
        return redirect("board:board_single", pk)
    return redirect("authpage_app:login")


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.username:
            comment.delete()
    return redirect("board:board_single", article_pk)


@require_POST
def comment_likes(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_pk)

        if comment.like_users.filter(pk=request.user.pk).exists():
            comment.like_users.remove(request.user)
        else:
            comment.like_users.add(request.user)
        return redirect(f"/board/{article_pk}/")
    return redirect("authpage_app:login")

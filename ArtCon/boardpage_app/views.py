from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardWriteForm
from .models import Post
from authpage_app.models import User


# Create your views here.
def board(request):
    login_session = request.session.get("login_session", "")
    context = {"login_session": login_session}

    test1_boards = Post.objects.filter(board_name="test1")
    test2_boards = Post.objects.filter(board_name="test2")

    context["test1_boards"] = test1_boards
    context["test2_boards"] = test2_boards

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
                board_name=write_form.board_name,
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

    context["board"] = board

    return render(request, "boardpage_app/board_single.html", context)

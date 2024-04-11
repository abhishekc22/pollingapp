from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import *
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponseBadRequest
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def signup(request):
    return render(request, "signup.html")


def signing(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("signup")

        user = User.objects.create_user(username=username, password=password)
        user.save()

        messages.success(request, "Account created successfully. You can now login.")
        return redirect("login")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("poll_list")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")


@login_required
def creation_polling(request):
    return render(request, "question.html")


@login_required
def create_poll(request):
    if request.method == "POST":
        question = request.POST.get("question")
        deadline = request.POST.get("deadline")
        if deadline:
            poll = Poll.objects.create(question=question, deadline=deadline)
        else:
            poll = Poll.objects.create(question=question)

        return redirect("add_choices", poll_id=poll.id)

    return render(request, "question.html")


@login_required
def add_choices(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if request.method == "POST":
        choice_text = request.POST.get("choice_text")
        Choice.objects.create(poll=poll, text=choice_text)
    choices = Choice.objects.filter(poll=poll)
    return render(request, "choices.html", {"poll": poll, "choices": choices})


@login_required
def poll_list(request):
    polls = Poll.objects.annotate(total_votes=Count("choice__vote")).all()
    for poll in polls:
        total_votes = poll.total_votes
        for choice in poll.choice_set.all():
            choice_percentage = 0
            if total_votes > 0:
                choice_percentage = round(
                    (choice.vote_set.count() / total_votes) * 100, 2
                )
            choice.percentage = choice_percentage
    paginator = Paginator(polls, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "dashboard.html", {"page_obj": page_obj})


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if poll.deadline and poll.deadline <= timezone.now():
        return HttpResponseBadRequest("Voting has ended for this poll.")

    if request.method == "POST":
        choice_id = request.POST.get("choice")
        choice = get_object_or_404(Choice, pk=choice_id)
        existing_vote = Vote.objects.filter(choice__poll=poll, user=request.user)
        if existing_vote.exists():
            return HttpResponseBadRequest("You have already voted for this poll.")
        new_vote = Vote(choice=choice, user=request.user)
        new_vote.save()

        Vote.objects.filter(choice__poll=poll, user=request.user).exclude(
            pk=new_vote.pk
        ).delete()

        poll.has_voted = True
        poll.save()

        return JsonResponse({"success": True})

    return HttpResponse("Method not allowed", status=405)


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

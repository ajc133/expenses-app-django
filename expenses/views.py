from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.db.models import F, Q, Sum
from django.forms import ValidationError
from django.http import (
    HttpRequest,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import (
    require_http_methods,
    require_safe,
)

from .forms import ExpenseForm
from .models import Expense, User


@login_required
@require_http_methods(["HEAD", "GET", "POST"])
def submit_expense(request: HttpRequest):
    default_group = request.user.groups.first()
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.submitter = request.user
            expense.save()
            return redirect("group_expenses", expense.group.id)

    # FIXME: What if a user is in two groups
    form = ExpenseForm(initial={"payer": request.user, "group": default_group})

    return render(request, "expense_submit.html", {"form": form})


@login_required
def groups(request: HttpRequest):
    groups = request.user.groups.all().values("id", "name")
    if len(groups) == 1:
        return redirect("group_expenses", groups[0]["id"])
    context = {"title": "Groups", "details_url": "group_expenses", "objects": groups}
    return render(request, "basic_list.html", context)


@login_required
def group_expenses(request: HttpRequest, group_id: int):
    group = get_object_or_404(Group, pk=group_id)
    search_string = request.GET.get("search")

    # Compute total expenses and per-person share
    total_cost = group.expenses.aggregate(total=Sum("cost"))["total"] or 0
    member_count = group.user_set.count()
    per_person_share = total_cost / member_count if member_count > 0 else 0

    # Compute how much each user paid
    group_debts = (
        User.objects.filter(groups=group)
        .annotate(paid=Sum("expenses_paid__cost", filter=Q(expenses_paid__group=group)))
        .annotate(owes=per_person_share - F("paid"))
        .filter(owes__gt=0)
    )

    group_expenses = group.expenses.select_related("payer").all()
    if search_string:
        group_expenses = group_expenses.filter(item__icontains=search_string)
    context = {
        "group_id": group.id,
        "expenses": group_expenses,
        "debts": group_debts.values("first_name", "owes"),
        "group": group,
    }

    return render(request, "group_expenses.html", context)


@require_safe
@login_required
def expense_details(request: HttpRequest, expense_id):
    expense = Expense.objects.select_related("payer", "submitter").get(id=expense_id)
    context = {"expense": expense}
    return render(request, "expense_details.html", context)


@require_http_methods(["HEAD", "GET", "POST"])
@login_required
def expense_edit(request: HttpRequest, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.submitter = request.user
            expense.save()

            return redirect("expense_edit", expense.id)
    form = ExpenseForm(instance=expense)

    return render(request, "expense_edit.html", {"form": form})


@require_http_methods(["HEAD", "GET", "POST"])
@login_required
def expense_delete(request: HttpRequest, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if request.method == "POST":
        group_id = expense.group.id
        expense.delete()
        return redirect("group_expenses", group_id)
    return render(request, "expense_delete.html", {"expense": expense})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("expense_submit")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

from datetime import datetime, timezone

from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http.request import QueryDict
from django.urls import reverse
from django.views.decorators.http import (
    require_http_methods,
    require_safe,
)
from django.contrib.auth.decorators import login_required
from .models import Expense, User


@login_required
def groups(request: HttpRequest):
    groups = Group.objects.all().values("id", "name")

    template = loader.get_template("list.html")
    return HttpResponse(template.render(context, request))


@require_http_methods(["HEAD", "GET", "POST"])
@login_required
def expenses(request: HttpRequest):
    context = RequestContext(request)
    submitter = get_object_or_404(User, pk=request.user.id)
    if request.method == "POST":
        form = request.POST
        item = form.get("item")
        cost = form.get("cost")
        receipt_photo = request.FILES.get("receipt-photo")
        payer_id = form.get("user-id")
        if item is None or cost is None:
            return HttpResponseBadRequest()
        payer = get_object_or_404(User, pk=payer_id)

        Expense(
            payer=payer,
            item=item,
            cost=cost,
            submitter=submitter,
            receipt_photo=receipt_photo,
        ).save()
        return HttpResponseRedirect(reverse("expenses"))

    expenses = Expense.objects.select_related("payer").order_by("-created_at").all()

    users = list(User.objects.exclude(username="admin").exclude(pk=submitter.id).all())
    # We always want submitter to be the first dropdown option
    users.insert(0, submitter)

    total_cost = Expense.objects.aggregate(Sum("cost"))["cost__sum"] or 0
    num_users = len(users)
    debts = []
    for user in users:
        amount_spent = sum([e.cost for e in user.expenses_paid.all()])
        if amount_spent < total_cost / num_users:
            owes = "{:.2f}".format(total_cost / num_users - amount_spent)
            debts.append((user.first_name, owes))

    template = loader.get_template("all_expenses.html")
    context = context.flatten() | {"expenses": expenses, "users": users, "debts": debts}

    return HttpResponse(template.render(context, request))


@require_safe
@login_required
def expense_details(request: HttpRequest, expense_id):
    # TODO: One db query
    expense = Expense.objects.get(id=expense_id)
    payer = User.objects.get(id=expense.payer.id)
    submitter_name = User.objects.get(id=expense.submitter.id)
    template = loader.get_template("expense_details.html")
    context = {"expense": expense, "payer": payer, "submitter": submitter_name}
    return HttpResponse(template.render(context, request))


def update_expense(
    request: HttpRequest, expense_id: int, form: QueryDict
) -> HttpResponse:
    submitter = get_object_or_404(User, pk=request.user.id)
    item = form.get("item")
    cost = form.get("cost")
    payer_id = form.get("user-id")
    receipt_photo = request.FILES.get("receipt-photo")
    if item is None or cost is None:
        return HttpResponseBadRequest()

    # The save() method handles image upload properly, and update()
    # does not. That's why I changed this block to call save().
    existing = Expense.objects.get(id=expense_id)
    existing.item = item
    existing.cost = cost
    existing.payer = User.objects.get(id=payer_id)
    existing.submitter = submitter
    if receipt_photo:
        existing.receipt_photo = receipt_photo
    existing.save()
    return HttpResponseRedirect(
        reverse("expense_details", kwargs={"expense_id": expense_id})
    )


@require_http_methods(["HEAD", "GET", "POST"])
@login_required
def expense_edit(request: HttpRequest, expense_id):
    if request.method == "POST":
        return update_expense(request, expense_id, request.POST)

    # TODO: One db query
    expense = Expense.objects.get(id=expense_id)
    payer = User.objects.get(id=expense.payer.id)

    users = list(User.objects.exclude(username="admin").exclude(id=payer.id).all())
    # We always want original payer to be the first dropdown option
    users.insert(0, payer)

    template = loader.get_template("expense_edit.html")
    context = {"expense": expense, "users": users}
    return HttpResponse(template.render(context, request))


@require_http_methods(["POST"])
@login_required
def expense_delete(request: HttpRequest, expense_id):
    Expense.objects.get(pk=expense_id).delete()
    return HttpResponseRedirect(reverse("expenses"))


@require_safe
@login_required
def users(request: HttpRequest):
    users = User.objects.exclude(username="admin").all()
    template = loader.get_template("all_users.html")
    context = {"users": users.values()}
    return HttpResponse(template.render(context, request))


@require_safe
@login_required
def user_details(request: HttpRequest, user_id):
    user = User.objects.get(id=user_id)
    user_expenses = user.expenses_paid.order_by("-created_at").all()
    template = loader.get_template("user_details.html")
    context = {"user": user, "expenses": user_expenses}
    return HttpResponse(template.render(context, request))


@require_safe
@login_required
def testing(request: HttpRequest):
    expenses = Expense.objects.all().values()
    template = loader.get_template("testing.html")
    context = {"expenses": expenses}
    return HttpResponse(template.render(context, request))

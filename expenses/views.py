from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.views.decorators.http import (
    require_http_methods,
    require_safe,
)
from django.contrib.auth.decorators import login_required
from .models import Expense, User


@require_http_methods(["HEAD", "GET", "POST"])
@login_required
def expenses(request: HttpRequest):
    context = RequestContext(request)
    submitter = get_object_or_404(User, pk=request.user.id)
    if request.method == "POST":
        form = request.POST
        item = form.get("item")
        cost = form.get("cost")
        payer_id = form.get("user-id")
        if item is None or cost is None:
            return HttpResponseBadRequest()
        payer = get_object_or_404(User, pk=payer_id)

        Expense(payer=payer, item=item, cost=cost, submitter=submitter).save()

    expenses = Expense.objects.select_related("payer").all()
    users = list(User.objects.exclude(username="admin").exclude(pk=submitter.id).all())
    users.insert(0, submitter)

    total_cost = Expense.objects.aggregate(Sum("cost"))["cost__sum"]
    print(total_cost)
    # TODO: DB query
    for user in users:
        setattr(
            user,
            "owes",
            (total_cost / 2) - sum([e.cost for e in user.expense_set.all()]),
        )

    template = loader.get_template("all_expenses.html")
    context = context.flatten() | {
        "expenses": expenses,
        "users": users,
    }

    return HttpResponse(template.render(context, request))


@require_safe
@login_required
def expense_details(request: HttpRequest, id):
    # TODO: One db query
    expense = Expense.objects.get(id=id)
    payer = User.objects.get(id=expense.payer.id)
    submitter_name = User.objects.get(id=expense.submitter.id)
    template = loader.get_template("expense_details.html")
    context = {"expense": expense, "payer": payer, "submitter": submitter_name}
    return HttpResponse(template.render(context, request))


@require_safe
@login_required
def users(request: HttpRequest):
    users = User.objects.exclude(username="admin").all()
    template = loader.get_template("all_users.html")
    context = {"users": users.values()}
    return HttpResponse(template.render(context, request))


@require_safe
@login_required
def user_details(request: HttpRequest, id):
    # TODO: One db query
    user = User.objects.get(id=id)
    user_expenses = user.expense_set.all().values()
    template = loader.get_template("user_details.html")
    context = {"user": user, "expenses": user_expenses}
    return HttpResponse(template.render(context, request))


@require_safe
@login_required
def main(request: HttpRequest):
    # FIXME: Template doesn't show user logged in
    template = loader.get_template("main.html")
    context = RequestContext(request)
    return HttpResponse(template.render(context.flatten()))


@require_safe
@login_required
def testing(request: HttpRequest):
    expenses = Expense.objects.all().values()
    template = loader.get_template("testing.html")
    context = {"expenses": expenses}
    return HttpResponse(template.render(context, request))

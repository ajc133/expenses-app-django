from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.template import loader
from django.views.decorators.http import require_http_methods, require_safe
from .models import Expense, User


@require_http_methods(["GET", "POST"])
def expenses(request: HttpRequest):
    if request.method == "POST":
        form = request.POST
        item = form.get("item")
        cost = form.get("cost")
        user_name = form.get("userName")
        if not Expense.create_expense(item, cost, user_name):
            return HttpResponseNotFound(b"User does not exist")

    expenses = Expense.objects.all().values()
    for expense in expenses:
        user_name = User.objects.get(id=expense["user_id"])
        expense["user_name"] = user_name
    template = loader.get_template("all_expenses.html")
    context = {"expenses": expenses}
    return HttpResponse(template.render(context, request))


@require_safe
def details(request: HttpRequest, id):
    expense = Expense.objects.get(id=id)
    user_name = User.objects.get(id=expense.user.id)
    template = loader.get_template("details.html")
    context = {"expense": expense, "user_name": user_name}
    return HttpResponse(template.render(context, request))


@require_safe
def main(request: HttpRequest):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())


def testing(request: HttpRequest):
    expenses = Expense.objects.all().values()
    users = User.objects.all().values()
    template = loader.get_template("testing.html")
    context = {"expenses": expenses, "users": users}
    return HttpResponse(template.render(context, request))

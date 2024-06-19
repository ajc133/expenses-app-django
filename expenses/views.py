from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.views.decorators.http import require_http_methods, require_safe
from .models import Expense, User

@require_http_methods(["GET", "POST"])
def expenses(request: HttpRequest):
    if request.method == "POST":
        form = request.POST
        item = form.get("item")
        cost = form.get("cost")
        userName = form.get("userName")
        user = User.objects.get(name=userName)
        Expense(user=user,item=item,cost=cost).save()

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
    template = loader.get_template("details.html")
    context = {"expense": expense}
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

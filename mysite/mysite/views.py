from django.http import JsonResponse
from django.shortcuts import redirect, render


def index(request):
    return render(request, "index.html")


def reset(request):
    if request.method == "POST":
        confirm = request.POST.get('confirm')

        if confirm != "confirm":
            return JsonResponse({"success": False})

        # seed()
        return redirect("/")
    else:
        return render(request, "reset.html")

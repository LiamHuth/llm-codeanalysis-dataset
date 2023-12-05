#
#

def detail(request, document_id):
    if request.user.is_authenticated:
        document = Document.objects.get(pk=document_id)
        context = {
            "title": document.title,
            "content": document.content
        }
        return render(request, "users/detail.html", context)
    else:
        return redirect(reverse("login"))

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
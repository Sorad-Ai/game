from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import tbl_proj
from django.db.models import Q
from django.http import StreamingHttpResponse
from .hands import gen
from django.http import JsonResponse

# for search suggestions
def get_suggestions(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        suggestions = (tbl_proj.objects.filter(keyword__icontains=query)
                                      .order_by('-view')  # Sort by 'view' column in descending order
                                      .values_list('keyword', flat=True)
                                      .distinct())
        return JsonResponse(list(suggestions), safe=False)
    return JsonResponse([], safe=False)


def app(request):
    return render(request)

def main(request):
    cards = tbl_proj.objects.all().order_by('-view')
    return render(request, 'cards.html', {'cards': cards})

# search
def search_projects(request):
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        projects = tbl_proj.objects.filter(
            Q(name__icontains=query) |
            Q(desc__icontains=query) |
            Q(keyword__icontains=query)
        )  # Filter by name, desc, or keyword
    else:
        projects = tbl_proj.objects.all()  # Display all if no query
    return render(request, 'search_results.html', {'projects': projects})


def appp(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        if project_id:
            print("Received project_id:", project_id)  # Debugging line
            try:
                project = tbl_proj.objects.get(id=project_id)
                # for update view
                project.view += 1
                project.save()

                # For redirection to app
                url_to_redirect = project.link
                return render(request, 'app/'+url_to_redirect)
            
            except tbl_proj.DoesNotExist:
                print("Project not found with ID:", project_id)  # Debugging line
                return redirect('/')  # Handle the error appropriately
        else:
            print("Project ID not provided.")  # Debugging line
            return redirect('/')  # Handle the error appropriately
    else:
        return redirect('/')
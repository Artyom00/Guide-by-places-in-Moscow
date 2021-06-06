from django.shortcuts import redirect


def redirect_categories_list(request):
    return redirect('rubrics_list', permanent=True)


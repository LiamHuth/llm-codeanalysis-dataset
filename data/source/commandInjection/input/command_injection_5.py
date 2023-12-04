# author: Liam Huth
# December 2023

from django.shortcuts import render
from django.http import HttpResponse
import sys
import io

def execute_python_code(code):
    backup = sys.stdout
    sys.stdout = io.StringIO()

    try:
        exec(code)
        output = sys.stdout.getvalue()
    except Exception as e:
        output = str(e)
    finally:
        sys.stdout.close()
        sys.stdout = backup

    return output

def home(request):
    output = ''
    if request.method == 'POST':
        code = request.POST.get('code')
        output = execute_python_code(code)

    return render(request, 'interpreter/home.html', {'output': output})

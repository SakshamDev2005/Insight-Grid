
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from .models import read_csv_file
from.models import generate_plot as gp
import pandas as pd
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.utils import timezone


var1 = "https://github.com/SakshamDev2005"
var2 = "https://www.instagram.com/hii_saksham/"
var3 = "https://www.linkedin.com/in/saksham2005/"

def home(request):
    return render(request, 'core/home.html',{'Github':var1,'Instagram':var2,'Linkedin':var3})

def about(request):
    return render(request, 'core/about.html',{'Github':var1,'Instagram':var2,'Linkedin':var3})

def contact(request):
    return render(request, 'core/contact.html',{'Github':var1,'Instagram':var2,'Linkedin':var3})

def upload_csv(request):
    return render(request, 'core/csv_file.html')

def terms(request):
    return render(request, 'core/terms.html',{'Github':var1,'Instagram':var2,'Linkedin':var3})

def privacy(request):
    return render(request, 'core/privacy.html',{'Github':var1,'Instagram':var2,'Linkedin':var3})


def home(request):

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        file_name = uploaded_file.name if uploaded_file else "CSV file"

        # Clear previous plot image to ensure it doesn't persist across requests
        request.session.pop('plot_image', None)

        if uploaded_file and uploaded_file.name.endswith('.csv'):
            try:
                table_data, file_name = read_csv_file(uploaded_file)

                # Only store small part in session (or nothing if it's huge)
                request.session['table_data'] = table_data # optional limit
                request.session['file_name'] = file_name

                return redirect('upload_csv')
            
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error: {str(e)}')
                return redirect('home')
        else:
            from django.contrib import messages
            messages.error(request, 'Please upload a valid CSV file.')
            return redirect('home')

    return render(request, 'core/home.html')

def upload_csv(request):

    table_data = request.session.get('table_data')
    file_name = request.session.get('file_name')
    plot_image = request.session.get('plot_image')

    if not table_data:
        from django.contrib import messages
        messages.error(request, 'No data found. Please upload again.')
        return redirect('home')
    
    try:
        table_data = pd.DataFrame(table_data['data'], columns=table_data['columns'])
        html_table = table_data.to_html(classes='table table-striped', index=False)
        return render(request, 'core/upload_csv.html', {'table_data': html_table, 
                                                        'file_name': file_name, 
                                                        'plot_image': plot_image,
                                                        'Github':var1,'Instagram':var2,'Linkedin':var3})

    except Exception as e:
        from django.contrib import messages
        messages.error(request, f'Error: {str(e)}')
        return redirect('home')

def generate_plot(request):
    if request.method == 'POST':
        x_axis = request.POST.get('x_axis').strip()
        y_axis = request.POST.get('y_axis').strip()
        plot_type = request.POST.get('graph_type')

        if not x_axis or not y_axis or not plot_type:
            from django.contrib import messages
            messages.error(request, 'Please select x-axis, y-axis, and plot type.')
            request.session.pop('plot_image', None)
            return redirect('upload_csv')
        
        try:
            table_data = request.session.get('table_data')
            if not table_data:
                from django.contrib import messages
                messages.error(request, 'No data found. Please upload again.')
                return redirect('home')

            table_data = pd.DataFrame(table_data['data'], columns=table_data['columns'])
           
            plot_image = gp(table_data,plot_type, x_axis, y_axis)
            request.session['plot_image'] = plot_image

            return redirect('upload_csv')
        
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error: {str(e)}')
            return redirect('home')
        

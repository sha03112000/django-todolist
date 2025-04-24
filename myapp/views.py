from django.shortcuts import redirect, render
from . forms import AddProductForm
from django.contrib import messages

from myapp.models import Login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signUp(request):
    return render(request, 'signup.html')

def sigIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        return render(request, 'index.html', {'message': 'Login successful!'})
    return render(request, 'index.html')

def signUpAction(request):
    if request.method == 'POST':
        requestdata = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'email': request.POST.get('email'),
        }
        form = AddProductForm(data=requestdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sign up successful!')
            return redirect('signUp')   # Redirect to a success page or login page
        else:
            return render(request, 'signup.html', {'form': form})
    return render(request, 'signup.html')

# def update_product(request, pk):
#     product = Product.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = UpdateProductForm(request.POST, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('success')
#     else:
#         form = UpdateProductForm(instance=product)
#     return render(request, 'product_form.html', {'form': form})
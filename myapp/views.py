from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from . forms import AddListForm, AddUserForm
from django.contrib import messages
from django import forms
from .models import Login, Todo
from django.contrib.auth.hashers import check_password
from .decorators import login_required_decorator

class AuthenticationForm(forms.Form):
    
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        try:
            user = Login.objects.get(username=username)
        except Login.DoesNotExist:
            raise forms.ValidationError("Invalid username or password")

        if not check_password(password, user.password):
            raise forms.ValidationError("Invalid username or password")

        # Attach user object to the form for use in the view
        self.user = user
        return cleaned_data
    
    
    
# Create your views here.



def sigIn(request):
    return render(request, 'signIn.html')


def signInAction(request):
    if request.method == 'POST':
        userName = request.POST.get('username')
        passWord = request.POST.get('password')
        requestedData = {
            'username': userName,
            'password': passWord,
        }
        form = AuthenticationForm(data=requestedData)
        if form.is_valid():
            user = form.user
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'signIn.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'signIn.html' , {'form': form})


def signUp(request):
    return render(request, 'signup.html')

def signUpAction(request):
    if request.method == 'POST':
        requestdata = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
            'email': request.POST.get('email'),
        }
        form = AddUserForm(data=requestdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sign up successful!')
            return redirect('signIn')   # Redirect to a success page or login page
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = AddUserForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    request.session.flush()  # Clears all session data
    messages.success(request, "You have been logged out.")
    return redirect('sigIn')


@login_required_decorator  # Placeholder for the decorator
def index(request):
    data = Todo.objects.all().order_by('id') 
    return render(request, 'index.html', {'data': data})

@login_required_decorator
def addTodo(request):
    return render(request, 'todolist.html')


@login_required_decorator
def addTodoAction(request):
    if request.method == 'POST':
        form = AddListForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'data added sucessfully')
            return redirect('index')
        else:
            messages.error(request,'unable to add list')
            return render(request, 'todolist.html', {'form': form})
    else:
     form = AddListForm()
    return render(request, 'todolist.html', {'form': form})

@login_required_decorator
def updateAction(request):
    if request.method == 'POST':
        instance = Todo.objects.get(id=request.POST.get('taskId'))
        form = AddListForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data updated successfully')
            return redirect('index')
        else:
            messages.error(request, 'Unable to update list')
            data = Todo.objects.all().order_by('id') 
            return render(request, 'index.html', {'form': form, 'data': data})
    return redirect('index')  # fallback to index if not POST

    

@login_required_decorator
def delete(request, id):
    if request.method == 'POST':
        instance = get_object_or_404(Todo, id=id)
        print(instance)
        instance.delete()
        return JsonResponse({'message': 'Data deleted successfully'})
    return JsonResponse({'message': 'Invalid request'}, status=400)

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
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,CreateView,FormView,ListView,DetailView
# Create your views here.
from todoweb.forms import UserRegistrationForm,LoginForm,TodoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from api.models import Todos

from django.utils.decorators import method_decorator
from django.contrib import messages


def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"you must login")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper


class RegisterView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    model=User
    success_url=reverse_lazy("signin")



    # def get(self,request,*args,**kw):
    #     form=UserRegistrationForm()
    #     return render(request,"register.html",{"form":form})

    # def post(self,request,*args,**kw):
    #     form=UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         messages.success(request,"your account created successfully")
    #         return redirect("signin")
    #     else:
    #         messages.error(request,"registration failed")
    #         return render(request,"register.html",{"form":form})


class LoginView(FormView):

    template_name="login.html"
    form_class=LoginForm


    # def get(self,request,*args,**kw):
    #     form=LoginForm()
    #     return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                messages.error(request,"invalid credentials")
                print("invalid")
                return redirect("signin")

# class IndexView(View):
#     def get(self,request,*args,**kw):
#         return render(request,"index.html")

@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    template_name="index.html"

@method_decorator(signin_required,name="dispatch")
class TodoListView(ListView):
    template_name="todo-list.html"
    model=Todos
    context_object_name="todos"

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
    




    # def get(self,request,*args,**kw):
    #     qs=Todos.objects.filter(user=request.user)
    #     return render(request,"todo-list.html",{"object_list":qs})

@method_decorator(signin_required,name="dispatch")
class TodoCreateView(View):
    template_name="todo-add.html"
    form_class=TodoForm
    model=Todos
    success_url=reverse_lazy("todo-list")

    def form_valid(self,form):
        form.instance.user=self.request.user
        messages.success(self.request,"todo created")
        return super().form_valid(form)

    # def get(self,request,*args,**kw):
    #     form=TodoForm()
    #     return render(request,"todo-add.html",{"form":form})

    # def post(self,request,*args,**kw):
    #     form=TodoForm(request.POST)
    #     if form.is_valid():
    #         instance=form.save(commit=False)
    #         instance.user=request.user
    #         instance.save()

    #         messages.success(request,"todo created successfully")
    #         return redirect("todo-list")
    #     else:
    #         messages.error(request,"failed to create todo")
    #         return render(request,"todo-add.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class TodoDetailView(DetailView):
    template_name="todo-detail.html"
    model=Todos
    context_object_name="todo"
    pk_url_kwarg="id"
    
    # def get(self,request,*args,**kw):
    #     id=kw.get("id")
    #     qs=Todos.objects.get(id=id)
    #     return render(request,"todo-detail.html",{"todo":qs})

@signin_required
def todo_delete_view(request,*args,**kw):
    id=kw.get("id")
    Todos.objects.get(id=id).delete()
    messages.success(request,"todo has been deleted")
    return redirect("todo-list")

@signin_required
def sign_out_view(request,*args,**kw):
    logout(request)
    return redirect("signin") 

            




        


        
        
            
            











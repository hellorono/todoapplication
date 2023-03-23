from django.urls import path
from todoweb import views

urlpatterns = [
    path("register",views.RegisterView.as_view(),name="register"),
    path("login",views.LoginView.as_view(),name="signin"),
    path("index",views.IndexView.as_view(),name="home"),
    path("todos/all",views.TodoListView.as_view(),name="todo-list"),
    path("todos/add",views.TodoCreateView.as_view(),name="todo-add"),
    path("todos/<int:id>",views.TodoDetailView.as_view(),name="todo-detail"),
    path("todos/<int:id>/remove",views.todo_delete_view,name="todo-delete"),
    path("signout",views.sign_out_view,name="sign-out")
]


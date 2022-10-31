from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.models import Todos
from api.serializers import TodoSerializer,RegistrationSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

class TodosView(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        Todos.objects.get(id=id).delete()
        return Response(data="deleted")

    def update(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class TodoModelViews(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=TodoSerializer
    queryset=Todos.objects.all()

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    # def list(self, request, *args, **kwargs):
    #     qs=Todos.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer=TodoSerializer(data=request.data,context={"user":request.user})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def create(self,request,*args,**kw):
    #     serializer=TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)#get credential sending user
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    

    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False,user=self.request.user)
        serilaizer=TodoSerializer(qs,many=True)
        return Response(data=serilaizer.data)

    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True)
        serilaizer=TodoSerializer(qs,many=True)
        return Response(data=serilaizer.data)
#localhost:8000/api/v1/todos/2/mark_as_done/
    @action(methods=["post"],detail=True)  
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        object.status=True
        object.save()
        serilaizer=TodoSerializer(object,many=False)
        return Response(data=serilaizer.data)

#authentication and permissions

class UsersView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all() #import user

    # def create(self,request,*args,**kw):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)#make password (password hashing)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
    



        
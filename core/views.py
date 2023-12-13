from django.shortcuts import render
from .models import  Task
from .serializers import RegisterUserSerializer, TaskSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.authtoken.models import Token

# Create your views here.

def loginuser(request):
    return render(request, 'login.html')

def registeruser(request):
    return render(request, 'register.html')

def logoutuser(request):
    logout(request)
    return redirect('login')

class RegisterUserAPI(APIView):
    def post(self, request):
        serializers = RegisterUserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            print(serializers.data)
            return Response(serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginUserAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                    'token': token.key
                })
        else:
            return Response({
                "error":"username or password is incorrect"
            },status=status.HTTP_400_BAD_REQUEST)

@login_required
def home(request):
    return render(request,"index.html")

class TaskList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetails(APIView):
    def get(self, request, id):
        snippet = self.get_object(id)
        serializer = TaskSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, id):
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        task = Task.objects.get(id=id)
        task.delete()
        return Response(status=status.HTTP_200_OK)
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "Method not supported",
            "status": "Failed"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        

        if not username or not email or not password:
            return JsonResponse({
                "error": "Input fields should not be empty"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(email=email, username=username, password=password)
        user.save()
        
        send_mail(
            "Congratualations",
            "We are so happy to have you onboard.",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return JsonResponse({
            "message": f"User {username} registered successfully"
        }, status=status.HTTP_201_CREATED)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON in request body."
        }, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "Method not supported",
            "status": "Failed"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({
                "error": "Input fields should not be empty"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return JsonResponse({
                "access-token": str(refresh.access_token),
                "refresh-token": str(refresh)
            })
        else:
            return JsonResponse({
                "error": "Invalid username or password."
            }, status=status.HTTP_401_UNAUTHORIZED)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON in request body."
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def createBoard(request):
#     user=request.user
#     boardName= (json.loads(request.body))["bname"]
#     description=(json.loads(request.body))["desc"]
#     if boardName and description:
#         newBoard=Boards.objects.create(boardName=boardName,description=description,user=user)
#         return JsonResponse({
#             "boardId":newBoard.id,
#             "message":"board created sucessfully"
#         })
        
        
        
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def createBoard(request):
    try:
        if request.user=="":
            raise Exception("user is not signed in")
        else:
            user=request.user
            try:
                boardName= (json.loads(request.body))["bname"]
                description=(json.loads(request.body))["desc"]
                if boardName == "" or description =="":
                    raise Exception("Board name and des not provided check once")
                checkBoardname = Boards.objects.filter(boardName=boardName).exists()
                if checkBoardname == True:
                    raise Exception("Author alredy added to the database")
                else:
                    boardName= (json.loads(request.body))["bname"]
                    description=(json.loads(request.body))["desc"]
                    newBoard=Boards.objects.create(boardName=boardName,description=description,user=user)
                    return JsonResponse({
                        "boardId":newBoard.id,
                        "message":"board created sucessfully"
                    })
            except Exception as ex:
                return JsonResponse({
                    "massage":str(ex),
                    "status":"filed"
                },status = status.HTTP_409_CONFLICT)
    except Exception as ex:
        return JsonResponse({
            "massage":str(ex),
            "status":"filed"
        },status = status.HTTP_401_UNAUTHORIZED)






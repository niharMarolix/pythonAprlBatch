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
        email = data['email']
        username = data['username']
        password = data['password']
        

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
        username = data['username']
        password = data['password']

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
                
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def createBoard(request):
    try:
        user = request.user
        data = json.loads(request.body)
        boardName = data['boardName']
        description = data['description']

        if not boardName or not description:
            return JsonResponse({
                "error": "Board name and description are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        new_board = Board.objects.create(boardName=boardName, description=description, user=user)
        return JsonResponse({
            "boardId": new_board.id,
            "message": "Board created successfully"
        }, status=status.HTTP_201_CREATED)

    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON in request body."
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def createListTitle(request):
    try:
        user = request.user
        data = json.loads(request.body)
        listTitle = data['listTitle']
        cardId = data['cardId']

        card_instance = Card.objects.get(id=cardId)

        if not listTitle or not card_instance:
            return JsonResponse({
                "error": "List title and valid card ID are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        new_list = List.objects.create(listTitle=listTitle, card=card_instance)
        return JsonResponse({
            "listId": new_list.id,
            "message": "List title created successfully"
        }, status=status.HTTP_201_CREATED)

    except Card.DoesNotExist:
        return JsonResponse({
            "error": "Card does not exist."
        }, status=status.HTTP_404_NOT_FOUND)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON in request body."
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def createCard(request):
    try:
        user = request.user
        data = json.loads(request.body)
        cardTitle = data['cardTitle']
        cardDescription = data['cardDescription']
        boardId = data.get['boardId']

        board_instance = Board.objects.get(id=boardId)

        if not cardTitle or not board_instance:
            return JsonResponse({
                "error": "Card title and valid board ID are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        new_card = Card.objects.create(cardTitle=cardTitle, cardDescription=cardDescription, board=board_instance)
        return JsonResponse({
            "cardId": new_card.id,
            "message": "Card created successfully"
        }, status=status.HTTP_201_CREATED)

    except Board.DoesNotExist:
        return JsonResponse({
            "error": "Board does not exist."
        }, status=status.HTTP_404_NOT_FOUND)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON in request body."
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def createTask(request):
    try:
        user = request.user
        data = json.loads(request.body)
        list_id = data['list_id']
        to_do_task = data['toDoTasks']

        list_instance = List.objects.get(id=list_id)

        if not to_do_task or not list_instance:
            return JsonResponse({
                "error": "Task description and valid list ID are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        new_task = Task.objects.create(
            toDoTasks=to_do_task,
            list=list_instance
        )

        return JsonResponse({
            "taskId": new_task.id,
            "message": "Task created successfully"
        }, status=status.HTTP_201_CREATED)

    except List.DoesNotExist:
        return JsonResponse({
            "error": "List does not exist."
        }, status=status.HTTP_404_NOT_FOUND)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON in request body."
        }, status=status.HTTP_400_BAD_REQUEST)


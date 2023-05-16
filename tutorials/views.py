from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from tutorials.models import myTutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view

#Find all Tutorials, Post a Tutorial Works
@api_view(['GET','POST'])
def tutorial_list(request):
    if request.method == 'GET':
        tutorials = myTutorial.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Get/Put/Delete for a Single Tutorial
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # Find Single Tutorial with ID Works
    try: 
        tutorial = myTutorial.objects.get(pk=pk) 
    except myTutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        tutorial_serializer = TutorialSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
    #Put Request to Update a Tutorial Works
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    #Delete Single Tutorial Works
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
   
    
#Find all Tutorials with published = True Works 
@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = myTutorial.objects.filter(published=True)
    tutorials_serializer = TutorialSerializer(tutorials, many=True)
    return JsonResponse(tutorials_serializer.data, safe=False)

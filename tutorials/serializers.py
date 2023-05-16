from rest_framework import serializers 
from tutorials.models import myTutorial
 
 
class TutorialSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = myTutorial
        fields = ('id',
                  'title',
                  'description',
                  'published')
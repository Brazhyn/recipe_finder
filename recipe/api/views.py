from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from recipe.models import Recipe, Review
from .serializers import RecipeSerializer, ReviewSerializer 
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'slug'
    

class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return Review.objects.filter(recipe__slug=slug) 
    
    def perform_create(self, serializer):
        author = self.request.user
        slug = self.kwargs['slug']
        recipe = Recipe.objects.get(slug=slug)
        
        if Review.objects.filter(author=author, recipe=recipe).exists():
            raise ValidationError('You have already reviewed this movie!')
        
        if recipe.number_reviews == 0:
            recipe.avg_rating = serializer.validated_data['rating']
        else:
            recipe.avg_rating = (recipe.avg_rating + serializer.validated_data['rating']) / 2
            
        recipe.number_reviews += 1
        recipe.save()
        serializer.save(author=author, recipe=recipe)
        
        

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    
    




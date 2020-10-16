from django.urls import path

from . import game, review, category

urlpatterns = [
    path('category/', category.API1, name='categoryFirst'),
    path('category/<int:index1>', category.API2, name='categorySecond'),
    path('category/<int:index1>/game/', game.API1, name='gameFirst'),
    path('category/<int:index1>/game/<int:index2>', game.API2, name='gameSecond'),
    path('game/', game.API3, name='gameThird'),
    path('category/<int:index1>/game/<int:index2>/review', review.API1, name='reviewFirst'),
    path('category/<int:index1>/game/<int:index2>/review/<int:index3>', review.API2, name='reviewSecond'),
    
]
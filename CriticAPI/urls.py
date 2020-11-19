from django.urls import path

from . import game, review, category, user

urlpatterns = [
    path('user/', user.API1, name='userFirst'),
    path('user/<int:index1>', user.API2, name='userSecond'),
    path('category/', category.API1, name='categoryFirst'),
    path('category/<int:index1>', category.API2, name='categorySecond'),
    path('category/<int:index1>/game/', game.API1, name='gameFirst'),
    path('game/<int:index1>', game.API2, name='gameSecond'),
    path('game/', game.API3, name='gameThird'),
    path('game/<int:index1>/review', review.API1, name='reviewFirst'),
    path('game/<int:index1>/review/<int:index2>', review.API2, name='reviewSecond'),
    
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('profile/', views.profile, name='profile'),


    path('notes/', login_required(views.notes), name='notes'),
    path('delete_note/<int:id>',
         login_required(views.delete_note), name='delete_note'),
    path('notes_detail/<int:pk>',
         login_required(views.NotesDetailView.as_view()), name='notes_detail'),
    path('homework/', login_required(views.homework), name='homework'),
    path('update_homework/<int:id>',
         login_required(views.homework_update), name='homework_update'),
    path('delete_homework/<int:id>',
         login_required(views.homework_delete), name='homework_delete'),
    path('youtube/', views.youtube, name='youtube'),
    path('todo/', login_required(views.todo), name='todo'),
    path('update_todo/<int:id>',
         login_required(views.todo_update), name='todo_update'),
    path('delete_todo/<int:id>',
         login_required(views.todo_delete), name='todo_delete'),
    path('books/', views.books, name='books'),
    path('dictionary/', views.dictionary, name='dictionary'),
    path('wiki/', views.wiki, name='wiki'),
    path('conversion/', views.conversion, name='conversion'),
]

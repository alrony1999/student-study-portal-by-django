from django.http import HttpResponse
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib import messages
from .models import Notes
from .forms import *
from django.views.generic import DetailView
from youtubesearchpython import VideosSearch
import requests
import wikipedia


def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            Notes(user=request.user, title=form.cleaned_data.get('title'),
                  description=form.cleaned_data.get('description')).save()
            form = NotesForm()
            messages.success(
                request, f'Notes Added from {request.user.username} successfully')
            return HttpResponseRedirect('/notes/')
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {
        'notes': notes,
        'form': form,
    }
    return render(request, 'dashboard/notes.html', context)


def delete_note(request, id):
    Notes.objects.get(pk=id).delete()
    messages.success(request, 'Deleted successfully')
    return redirect("notes")


# def noteDetailView(request, id):
#     note = Notes.objects.get(pk=id)
#     return render(request, 'dashboard/notes_detail.html', {'note': note})


class NotesDetailView(DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = form.cleaned_data.get('is_finished')
                if finished:
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            Homework(
                user=request.user,
                subject=form.cleaned_data.get('subject'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                due=form.cleaned_data.get('due'),
                is_finished=finished
            ).save()
            messages.success(
                request, f'Homework Added from {request.user.username} successfully')
            return HttpResponseRedirect('/homework/')

    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'form': form,
        'homeworks': homeworks,
        'homework_done': homework_done
    }
    return render(request, 'dashboard/homework.html', context)


def homework_update(request, id):
    homework = Homework.objects.get(pk=id)
    if homework.is_finished:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    messages.success(
        request, f'Homework Updated Id {id} successfully')
    return redirect('homework')


def homework_delete(request, id):
    Homework.objects.get(pk=id).delete()
    messages.success(
        request, f'Homework Deleted successfully')
    return redirect('homework')


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
    else:
        form = DashboardForm()
        result_list = []
    context = {
        'form': form,
        'r': result_list
    }
    return render(request, 'dashboard/youtube.html', context)


def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = form.cleaned_data.get('is_finished')
                if finished:
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            Todo(
                user=request.user,
                title=form.cleaned_data.get('title'),
                is_finished=finished
            ).save()
            messages.success(
                request, f'Todo Added from {request.user.username} successfully')
            return HttpResponseRedirect('/todo/')

    else:
        form = TodoForm()

    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'form': form,
        'todos': todos,
        'todo_done': todo_done
    }
    return render(request, 'dashboard/todo.html', context)


def todo_update(request, id):
    todo = Todo.objects.get(pk=id)
    if todo.is_finished:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    messages.success(
        request, f'Todo Updated Id {id} successfully')
    return redirect('todo')


def todo_delete(request, id):
    Todo.objects.get(pk=id).delete()
    messages.success(
        request, f'Todo Deleted successfully')
    return redirect('todo')


def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        ans = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': ans['items'][i]['volumeInfo']['title'],
                'subtitle': ans['items'][i]['volumeInfo'].get('subtitle'),
                'description': ans['items'][i]['volumeInfo'].get('description'),
                'count': ans['items'][i]['volumeInfo'].get('pageCount'),
                'categories': ans['items'][i]['volumeInfo'].get('categories'),
                'rating': ans['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': ans['items'][i]['volumeInfo'].get('imageLinks')['thumbnail'],
                'preview': ans['items'][i]['volumeInfo'].get('previewLink')

            }
            result_list.append(result_dict)

        context = {
            'form': form,
            'r': result_list
        }
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        ans = r.json()
        phonetics = ans[0]['phonetics'][0]['text'],
        audio = ans[0]['phonetics'][0]['audio'],
        defination = ans[0]['meanings'][0]['definitions'][0]['definition'],
        synonyms = ans[0]['meanings'][0]['definitions'][0]['synonyms']
        context = {
            'form': form,
            'input': text,
            'phonetics': phonetics,
            'audio': audio,
            'defination': defination,
            'synonyms': synonyms
        }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form,
        }
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary,

        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'dashboard/wiki.html', context)


def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
            return render(request, 'dashboard/conversion.html', context)
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm(request.POST)
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
            return render(request, 'dashboard/conversion.html', context)
    else:
        form = ConversionForm()
    context = {
        'form': form,
        'input': False
    }
    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account Created for {username}.')
            return HttpResponseRedirect('/login/')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)


def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)

    if len(todos) == 0:
        todos_done = False
    else:
        todos_done = True

    if len(homeworks) == 0:
        homeworks_done = False
    else:
        homeworks_done = True

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'todos_done': todos_done,
        'homeworks_done': homeworks_done
    }
    return render(request, 'dashboard/profile.html', context)

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, Photos, User, Comment

from .forms import PhotoForm, UserForm, CommentForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class PhotoView(generic.ListView):
    template_name = 'polls/photos.html'
    context_object_name = 'latest_photo_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Photos.objects.filter(
            time__lte=timezone.now()
        ).order_by('-time')[:5]

class PhotoDetailView(generic.DetailView):
    model = Photos
    template_name = 'polls/photo_detail.html'

class PhotoAddView(generic.CreateView):
    model = Photos
    template_name = 'polls/photo_add.html'
    fields = ['title', 'image', 'text']


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def photo_upload(request):
    form = PhotoForm(request.POST, request.FILES)
    form2 = UserForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        if form2.is_valid():
            form2.save()
        return HttpResponseRedirect(reverse('polls:photo'))
    else:
        return render(request, 'polls/photos.html', {'form': form})

def photo_comment(request):
    if request.method == 'POST':
        photo_id = request.POST.get('photo_id')
        photo = get_object_or_404(Photos, pk=photo_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # comment.user = request.user
            comment.save()
            photo.comment_list.add(comment)
    return HttpResponseRedirect(reverse('polls:photo'))

def photo_likes(request):
    if request.method == 'POST':
        photo_id = request.POST.get('photo_id')
        photo = get_object_or_404(Photos, pk=photo_id)
        photo.likes += 1
        photo.save()
    return HttpResponseRedirect(reverse('polls:photo'))

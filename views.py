from django.shortcuts import render
from django.template import RequestContext,loader
from models import Question, Choice
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from mysite.views import check_login 
# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
@check_login
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = RequestContext(request,{'latest_question_list': latest_question_list})
    return HttpResponse(template.render(context))
@check_login
def detail(request,question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
            raise Http404("Question does not exist")
    return render(request,'polls/detail.html',{'question' : question})
@check_login
def results(request, question_id):
    question = get_object_or_404(Question,pk = question_id)
    return render(request,'polls/result.html',{'question' : question})
@check_login
def vote(request,question_id):
    p = get_object_or_404(Question,pk = question_id)
    try:
        selected_choice = p.choice_set.get(pk = request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question' : p,
            'error_message' : "You didn't select a choice.", 
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte = timezone.now()
            ).order_by("-pub_date")[:5]
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now())
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'
    
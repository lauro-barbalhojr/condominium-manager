from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


# Create your views here.
class IndexView(generic.ListView):
    template_name = "votacoes/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """Retornar as cinco últimas questões publicadas"""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "votacoes/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "votacoes/results.html"
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice =question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "votacoes/detail.html",
            {
                "question": question,
                "error_message": "Você não fez uma escolha"
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse("votacoes:resultados", args=(question.id,)))

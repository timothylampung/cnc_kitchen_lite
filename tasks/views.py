from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
from django.views import View

from tasks.forms import TaskSetForm
from tasks.models import TaskSet


class TaskListView(ListView):
    model = TaskSet
    template_name = 'tasks/tasks.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        task_set = TaskSet.objects.order_by('-timestamp')
        context = super().get_context_data(**kwargs)
        context['task_set'] = task_set
        context['task_count'] = task_set.count()
        return context


class TaskCreateView(CreateView):
    model = TaskSet
    template_name = 'tasks/tasks.html'
    form_class = TaskSetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recipe Create'
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return redirect(reverse("tasks:tasks-list"))


class TaskDeleteView(DeleteView):
    model = TaskSet
    success_url = '/recipes/'
    template_name = 'recipes/recipes.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(reverse("tasks:tasks-list"))

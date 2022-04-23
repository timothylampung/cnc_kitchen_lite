import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from recipe.forms import RecipeForm, StepForm
from recipe.models import Recipe, Step, SubStep
from posts.forms import PostForm
from tasks.forms import TaskSetForm

from recipe.step_forms import (HeaterForm, MixerForm, ValveForm, StepFormType, PickIngredientForm)

heater_form = HeaterForm()
mixer_form = MixerForm()
valve_form = ValveForm()
pickup_form = PickIngredientForm()


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipes.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        recipes = Recipe.objects.order_by('-timestamp')
        context = super().get_context_data(**kwargs)
        context['recipes'] = recipes
        context['recipes_count'] = recipes.count()
        task_set_form = TaskSetForm()
        context['task_set_form'] = task_set_form
        return context


class RecipeCreateView(CreateView):
    model = Recipe
    template_name = 'recipes/new-recipe/new-recipe.html'
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recipe Create'
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return redirect(reverse("recipes:recipes-detail", kwargs={
            'pk': form.instance.pk
        }))


class RecipeDetailView(DetailView, UpdateView):
    model = Recipe
    template_name = 'recipes/new-recipe/detail-recipe.html'
    form_class = RecipeForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = RecipeForm(instance=self.object, )
        pickup_step = Step(recipe=self.object, step_type=Step.PICKUP_STEP)
        wok_step = Step(recipe=self.object, step_type=Step.WOK_STEP)
        pickup_step_form = StepForm(instance=pickup_step)
        wok_step_form = StepForm(instance=wok_step)

        form.helper.form_action = f'/recipes/detail/{self.object.id}/'
        context = self.get_context_data(object=self.object)
        context['form'] = form
        context['wok_step_form'] = wok_step_form
        context['pickup_step_form'] = pickup_step_form
        context['recipe'] = self.object
        context['title'] = 'Recipe Detail'
        context['heater_form'] = heater_form
        context['mixer_form'] = mixer_form
        context['valve_form'] = valve_form
        context['pickup_form'] = pickup_form
        return self.render_to_response(context)

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.save()
        return redirect(reverse("recipes:recipes-detail", kwargs={
            'pk': form.instance.pk
        }))


class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = '/recipes/'
    template_name = 'recipes/recipes.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(reverse("recipes:recipes-list"))


class RecipeUpdateView(UpdateView):
    model = Recipe
    template_name = 'recipes/new-recipe/new-recipe.html'
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.save()
        return redirect(reverse("recipes-detail", kwargs={
            'pk': form.instance.pk
        }))


def step_add(request):
    print(request.POST)
    form = StepForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()

        print(form.errors)
        return redirect(reverse("recipes:recipes-detail", kwargs={
            'pk': request.POST['recipe']
        }))


def add_sub_step(request, step_id, recipe_id, form_type):
    print(request.POST)
    form = HeaterForm(request.POST or None)
    data = {}
    if request.method == "POST":
        if form_type == StepFormType.MIXER_FORM:
            form = MixerForm(request.POST or None)
        if form_type == StepFormType.VALVE_FORM:
            form = ValveForm(request.POST or None)
            print(data)
        if form_type == StepFormType.HEATER_FORM:
            form = HeaterForm(request.POST or None)
        if form_type == StepFormType.PICKUP_INGREDIENT:
            form = PickIngredientForm(request.POST or None)

        if form.is_valid():
            _f = dict()
            _f = form.data.copy()
            _d = _f.pop('csrfmiddlewaretoken')
            data = json.dumps(_f)
            sub_step = SubStep(step_id=step_id, name=form_type)
            sub_step.parameters = data
            sub_step.save()
            async_to_sync(get_channel_layer().group_send)(f'channel_1', {
                'type': 'channel_message',
                'message': 'Sub step saved!',
            })
        else:
            print(form.errors)
            async_to_sync(get_channel_layer().group_send)(f'channel_1', {
                'type': 'channel_message',
                'message': 'Some error occur while saving sub step',
            })

        return redirect(reverse("recipes:recipes-detail", kwargs={
            'pk': recipe_id
        }))

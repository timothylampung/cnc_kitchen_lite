from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from ingredients.forms import IngredientForm
from ingredients.models import Ingredient
from posts.forms import PostForm


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/ingredients.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        ingredients = Ingredient.objects.order_by('-timestamp')
        context = super().get_context_data(**kwargs)
        context['ingredients'] = ingredients
        context['ingredients_count'] = ingredients.count()
        return context


class IngredientCreateView(CreateView):
    model = Ingredient
    template_name = 'ingredients/new-ingredient/new-ingredient.html'
    form_class = IngredientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return redirect(reverse("ingredients:ingredients-detail", kwargs={
            'pk': form.instance.pk
        }))


class IngredientDetailView(DetailView, UpdateView):
    model = Ingredient
    template_name = 'ingredients/new-ingredient/new-ingredient.html'
    form_class = IngredientForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = IngredientForm(instance=self.object, )
        form.helper.form_action = f'/ingredients/update/{self.object.id}'
        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.save()
        return redirect(reverse("ingredients:ingredients-detail", kwargs={
            'pk': form.instance.pk
        }))


class IngredientDeleteView(DeleteView):
    model = Ingredient
    success_url = '/ingredients'
    template_name = 'post_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(reverse("ingredients:ingredients-list"))


class IngredientUpdateView(UpdateView):
    model = Ingredient
    template_name = 'ingredients/new-ingredient/new-ingredient.html'
    form_class = IngredientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.save()
        return redirect(reverse("ingredient-detail", kwargs={
            'pk': form.instance.pk
        }))

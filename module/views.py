from crispy_forms.layout import Layout, Div, Submit
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from module.forms import ModuleForm
from module.models import Module, ModuleController
from posts.forms import PostForm
from recipe.step_forms import PickIngredientForm, HeaterForm, MixerForm, ValveForm


class ModuleListView(ListView):
    model = Module
    template_name = 'modules/modules.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        modules = Module.objects.order_by('-timestamp')
        context = super().get_context_data(**kwargs)

        context['modules'] = modules
        context['modules_count'] = modules.count()
        return context


class ModuleCreateView(CreateView):
    model = Module
    template_name = 'modules/new-module/new-module.html'
    form_class = ModuleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Module Create'
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return redirect(reverse("modules:modules-detail", kwargs={
            'pk': form.instance.pk
        }))


class ModuleDetailView(DetailView, UpdateView):
    model = Module
    template_name = 'modules/new-module/new-module.html'
    form_class = ModuleForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ModuleForm(instance=self.object, )
        form.helper.form_action = f'/modules/detail/{self.object.id}/'
        context = self.get_context_data(object=self.object)
        module_forms = []
        controllers = ModuleController.objects.filter(module=self.object)
        for controller in controllers:
            if controller.controller_type == ModuleController.PICKUP_INGREDIENT:
                ingredient_form = PickIngredientForm()
                ingredient_form.helper.form_class = 'pick-ingredient-form'
                ingredient_form.helper.form_action = f'/tasks/send-remote-data/{controller.controller_type}/'
                ingredient_form.helper.add_input(
                    Submit('submit', 'ping', css_class='col-md-12 mt-2')
                )

                module_forms.append(
                    {
                        'form': ingredient_form,
                        'type': controller.controller_type,
                        'selector': 'pick-ingredient-form'
                    }
                )
            elif controller.controller_type == ModuleController.HEATER:
                heater_form = HeaterForm()
                heater_form.helper.form_class = 'heater-form'
                heater_form.helper.form_action = f'/tasks/send-remote-data/{controller.controller_type}/'
                heater_form.helper.add_input(
                    Submit('submit', 'ping', css_class='col-md-12 mt-2')
                )

                module_forms.append(
                    {
                        'form': heater_form,
                        'type': controller.controller_type,
                        'selector': 'heater-form'

                    }
                )
            elif controller.controller_type == ModuleController.MIXER:
                mixer_form = MixerForm()
                mixer_form.helper.form_class = 'mixer-form'
                mixer_form.helper.form_action = f'/tasks/send-remote-data/{controller.controller_type}/'
                mixer_form.helper.add_input(
                    Submit('submit', 'ping', css_class='col-md-12 mt-2')
                )
                module_forms.append(
                    {
                        'form': mixer_form,
                        'type': controller.controller_type,
                        'selector': 'mixer-form'
                    }
                )
            elif controller.controller_type == ModuleController.VALVE:
                valve_form = ValveForm()
                valve_form.helper.form_class = 'valve-form'
                valve_form.helper.form_action = f'/tasks/api/send-remote-data/{controller.controller_type}/'
                valve_form.helper.add_input(
                    Submit('submit', 'ping', css_class='col-md-12 mt-2')
                )
                module_forms.append(
                    {
                        'form': valve_form,
                        'type': controller.controller_type,
                        'selector': 'valve-form'
                    }
                )

        context['form'] = form
        context['controller_forms'] = module_forms
        context['title'] = 'Module Detail'
        return self.render_to_response(context)

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.save()
        return redirect(reverse("modules:modules-detail", kwargs={
            'pk': form.instance.pk
        }))


class ModuleDeleteView(DeleteView):
    model = Module
    success_url = '/modules'
    template_name = 'post_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(reverse("modules:modules-list"))


class ModuleUpdateView(UpdateView):
    model = Module
    template_name = 'modules/new-module/new-module.html'
    form_class = ModuleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.editor = self.request.user
        form.save()
        return redirect(reverse("modules-detail", kwargs={
            'pk': form.instance.pk
        }))

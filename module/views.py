from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from module.forms import ModuleForm
from module.models import Module
from posts.forms import PostForm


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
        context['form'] = form
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

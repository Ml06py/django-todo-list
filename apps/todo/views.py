from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, UpdateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

import uuid

from todo.models import task, project
from .forms import TodoForm, ProjectForm, ProjectTaskForm
from .mixins import UserTodoAccess, DeleteTodoMixin, UserProjectAccess, DeleteProjectMixin

# Codes for Todo stuff
class home_page(LoginRequiredMixin, ListView):
	'''
		This is the home page and a list of all the tasks
	'''
	template_name = 'base/home.html'
	paginate_by = 2

	def get_queryset(self):
		return  task.objects.filter(owner=self.request.user).order_by("time_to_start","done")

class updateTask(LoginRequiredMixin, UserTodoAccess, UpdateView):
	'''
		This is the page to update a task
	'''
	template_name = 'todo/task/updateTask.html'
	fields = ["name", "detail", "time_to_start", "token" ,"done"]
	success_url = reverse_lazy('todo:home')

	def get_object(self):
		return get_object_or_404(task, token=self.kwargs['token'])
	
class CreateTask(LoginRequiredMixin, FormView):
	'''
		This is the page to create a task
	'''
	template_name = 'todo/task/createTask.html'
	form_class = TodoForm
	success_url = 'todo:home'

	def form_valid(self,form):
		owner_form = form.save(commit=False)
		owner_form.owner = self.request.user
		owner_form.token = uuid.uuid4().hex.upper()[0:12]
		owner_form.save()
		return redirect('todo:home')

class DeleteTask(DeleteTodoMixin,DeleteView):
	'''
		This is the page to delete a task
	'''
	model = task
	success_url = reverse_lazy('todo:home')
	template_name = "todo/task/DeleteTask.html"

class SearchTask(ListView):
    model = task
    template_name = "base/search.html"

    def get_queryset(self):
        query = self.request.GET.get("nav_search")
        object_list =  task.objects.filter(Q(name__icontains=query))
        return object_list.filter(owner=self.request.user)

# Codes for Project stuff
class CreateProject(LoginRequiredMixin, FormView):
	'''
		This is the page to create a project
	'''
	template_name = "todo/project/createProject.html"
	form_class = ProjectForm

	def form_valid(self, form):
		form = form.save(commit= False)
		form.owner = self.request.user
		form.token = uuid.uuid4().hex.upper()[0:12]
		form.save()
		return redirect("todo:listProject")

class UpdateProject(LoginRequiredMixin, UserProjectAccess, UpdateView):
	'''
		This is the page to update a project
	'''
	template_name = 'todo/project/updateProject.html'
	fields = ["name", "detail", "deadline" ,"status", "token"]
	success_url = reverse_lazy('todo:listProject') 

	def get_object(self):
		return get_object_or_404(project, token=self.kwargs['token'])

class DeleteProject(LoginRequiredMixin, DeleteProjectMixin, DeleteView):
	'''
		This is the page to delete a project
	'''
	success_url = reverse_lazy('todo:listProject')
	template_name = "todo/project/DeleteProject.html"
	
	def get_object(self):
		object = get_object_or_404(project, token=self.kwargs['token'])
		object.task.all().delete()
		return object


class listProject(LoginRequiredMixin, ListView):
	'''
		This is the page to list all the projects
	'''

	template_name = 'todo/project/listProject.html'
	paginate_by = 2

	def get_queryset(self):
		return  project.objects.filter(owner=self.request.user).order_by("status")


class ListProjectTask(LoginRequiredMixin, ListView):
	'''
		This is the page to list all the tasks of a project
	'''
	template_name = 'todo/project/listProjectTask.html'
	def get_queryset(self):
		project_token = self.kwargs["token"]
		return task.objects.filter(project__token= project_token).order_by("time_to_start","done")


class CreateProjectTask(LoginRequiredMixin, FormView):
	'''
		This is the page to create a task in a project
	'''
	template_name = 'todo/project/createProjectTask.html'
	form_class = ProjectTaskForm

	def form_valid(self, form):
		form = form.save(commit= False)
		project_model = project.objects.filter(token=self.kwargs['token']).first()
		form.owner = self.request.user
		form.token = uuid.uuid4().hex.upper()[0:12]
		form.save()
		project_model.task.add(form)
		return redirect('todo:listProject')
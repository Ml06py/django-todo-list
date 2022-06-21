from django.urls import path
from todo.views import (home_page,
                        updateTask, CreateTask, DeleteTask, SearchTask,
                        listProject, ListProjectTask, 
                        CreateProject, UpdateProject,DeleteProject, 
                         CreateProjectTask,
                         CreateRoutine, UpdateRoutine, DeleteRoutine, listRoutine)
app_name = "todo"

urlpatterns = [
    path("",home_page.as_view(),name="home"),
    path("list-project/", listProject.as_view(), name="listProject"),
    path("list-project-task/<str:token>/", ListProjectTask.as_view(), name="listProjectTask"),
    path("list-routine/", listRoutine.as_view(), name="listRoutine"),

    path("update-task/<str:token>/", updateTask.as_view(),name="updateTask"),
    path("update-project/<str:token>/", UpdateProject.as_view(),name="updateProject"),
    path("update-routine/<str:token>/", UpdateRoutine.as_view(),name="updateRoutine"),

    path("create-task/",CreateTask.as_view(),name="CreateTask"),
    path("create-project/", CreateProject.as_view(), name='CreateProject'),
    path("create-project-task/<str:token>/", CreateProjectTask.as_view(), name='CreateProjectTask'),
    path("create-routine/", CreateRoutine.as_view(), name='CreateRoutine'),

    path("delete-task/<str:token>/",DeleteTask.as_view(),name="DeleteTask"),
    path("delete-project/<str:token>/",DeleteProject.as_view(),name="DeleteProject"),
    path("delete-routine/<str:token>/",DeleteRoutine.as_view(),name="DeleteRoutine"),
    
    path("search/",SearchTask.as_view(),name="SearchTask")
]
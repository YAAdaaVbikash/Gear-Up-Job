from django.urls import path
from gearupjob import views

app_name = 'gearupjob'


urlpatterns = [
    path('', views.index, name='index'),
    path('companies/', views.CompanyListView.as_view(), name='companies'),
    path('profile/addjob/', views.JobCreate.as_view(), name='post_job'),
    path('company/<int:pk>/edit/',
         views.CompanyUpdateView.as_view(), name='company_update'),
    path('job/<int:pk>/', views.job_single, name='job_single'),
    path('company/<int:pk>/', views.CompanyDetail, name='company_detail'),
    path('company/<int:pk>/addjob/', views.JobCreateView, name='add_job'),
    path('profile/job/edit/<int:pk>/',
         views.JobUpdateView.as_view(), name='edit_job'),
    path('delete/<int:pk>/', views.delete_job, name='delete_job'),
    path('profile/delete/<int:pk>/', views.DeleteJobView.as_view(), name='delete'),
    path('jobs/', views.AllJobs, name='all_jobs'),
    path('contact/', views.ContactUs, name='contact'),
    path('results/', views.Search, name='search'),
    path('test/', views.clickme, name="test"),
    path('rate/<int:pk1>/<int:pk2>/', views.rate_us, name="rate"),
]

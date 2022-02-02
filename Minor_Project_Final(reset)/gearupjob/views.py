from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db import models
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import CreteJobForm
from accounts.models import Company, Seeker,Rating
from gearupjob.models import Job
from gearupjob.decorators import company_required
from accounts.forms import CompanyForm
from accounts.list import category
# Create your views here.


def index(request):
    for company in Company.objects.all():
        company.Total_Jobs = company.jobs.all().count()
    Latest_jobs = Job.objects.all().order_by('-published_on')
    Top_jobs = Job.objects.all().order_by('-view')
    Top_company = Company.objects.all().order_by('-Total_Views')

    if request.user.is_authenticated:
        if Seeker.objects.filter(seeker=request.user).exists():
            #    if request.user.seeker.job_category_1 and request.user.seeker.job_category_2 and request.user.seeker.job_category_3 and request.user.seeker.job_category_4:
            #        job_category_list = Job.objects.filter(Q(job_category=request.user.seeker.job_category) | Q(job_category=request.user.seeker.job_category_1) | Q(job_category=request.user.seeker.job_category_2) |
            #                                              Q(job_category=request.user.seeker.job_category_3) | Q(job_category=request.user.seeker.job_category_4)).order_by('-published_on')
            #    elif request.user.seeker.job_category_1 and request.user.seeker.job_category_2 and request.user.seeker.job_category_3 :
            #        job_category_list = Job.objects.filter(Q(job_category=request.user.seeker.job_category) | Q(job_category=request.user.seeker.job_category_1) | Q(job_category=request.user.seeker.job_category_2) |
            #                                              Q(job_category=request.user.seeker.job_category_3)).order_by('-published_on')
            #    elif request.user.seeker.job_category_1 and request.user.seeker.job_category_2 :
            #        job_category_list = Job.objects.filter(Q(job_category=request.user.seeker.job_category) | Q(job_category=request.user.seeker.job_category_1) | Q(job_category=request.user.seeker.job_category_2)).order_by('-published_on')
            #    elif request.user.seeker.job_category_1 :
            #        job_category_list = Job.objects.filter(Q(job_category=request.user.seeker.job_category) | Q(job_category=request.user.seeker.job_category_1)).order_by('-published_on')
            #    else:
            #        job_category_list = Job.objects.filter(Q(job_category=request.user.seeker.job_category))

            Recomended_Job = Job.objects.filter(Q(title=request.user.seeker.history_0) | Q(title=request.user.seeker.history_1) | Q(title=request.user.seeker.history_2) | Q(title=request.user.seeker.history_3) |
                                                Q(title=request.user.seeker.history_4) | Q(title=request.user.seeker.history_5) | Q(title=request.user.seeker.history_6) | Q(title=request.user.seeker.history_7) |
                                                Q(title=request.user.seeker.history_8) | Q(title=request.user.seeker.history_9) | Q(title=request.user.seeker.history_10) | Q(title=request.user.seeker.history_11) |
                                                Q(title=request.user.seeker.history_12) | Q(title=request.user.seeker.history_13) | Q(title=request.user.seeker.history_14) |
                                                Q(job_category=request.user.seeker.job_category) | Q(job_category=request.user.seeker.job_category_1) | Q(job_category=request.user.seeker.job_category_2) |
                                                Q(job_category=request.user.seeker.job_category_3) | Q(job_category=request.user.seeker.job_category_4)).order_by('-published_on')

            return render(request, 'index.html', {'jobs': Recomended_Job, 'topcompanay': Top_company, 'categories': category})

    return render(request, 'index.html', {'jobs': Latest_jobs, 'topjob': Top_jobs, 'topcompanay': Top_company, 'catagories': category})


class CompanyListView(ListView):
    model = Company

    def get_queryset(self):
        return Company.objects.all().order_by('-Total_Views')


class CompanyDetailView(DetailView):
    model = User


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm

    def form_valid(self, form):
        if form.instance.company_username.id == self.request.user.company.id:
            return super(CompanyUpdateView, self).form_valid(form)
        else:
            return redirect('/')


class JobCreate(CreateView):
    #    fields=('title','job_type','job_location','application_deadline','salary','image','gender','vacancy','experience','responsibilities','description')
    form_class = CreteJobForm
    model = Job

    def form_valid(self, form):
        form.instance.Company_Username = self.request.user.company
        return super(JobCreate, self).form_valid(form)


class JobUpdateView(UpdateView):
    # fields=('title','job_type','job_location','application_deadline','salary','image','gender','vacancy','experience','responsibilities','description')
    form_class = CreteJobForm
    model = Job

    def form_valid(self, form):
        if form.instance.Company_Username == self.request.user.company:
            return super(JobUpdateView, self).form_valid(form)
        else:
            return redirect('/')


class DeleteJobView(DeleteView):
    model = Job
    success_url = reverse_lazy("gearupjob:index")


def delete_job(request, pk):
    job = Job.objects.filter(pk=pk)
    job.delete()
    return redirect('gearupjob:index')


@login_required(login_url='accounts:login')
def CompanyDetail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    rating = company.rating
    return render(request, 'accounts/company_detail.html', {'company_detail': company, 'rating': rating})


@login_required(login_url='accounts:login')
@company_required
def JobCreateView(request, pk):
    company = get_object_or_404(Company, pk=pk)
    job_form = CreteJobForm()
    if request.method == 'GET':
        return render(request, 'gearupjob/create_job.html', {'form': job_form})
    else:
        job_form = CreteJobForm(request.POST)
        if job_form.is_valid():
            job = job_form.save(commit=False)
            job.Company_Username = company
            job.save()
            company.update_jobs()
            messages.success(request, 'New job is Added.')
        #    return redirect('gearupjob:CompanyDetail',pk=company.pk)
            return redirect('gearupjob:index',)
        return render(request, 'gearupjob/create_job.html', {'form': job_form})


@login_required(login_url='accounts:login')
def AllJobs(request):
    jobs = Job.objects.all().order_by('-view')

    paginator = Paginator(jobs, 5)  # Show 5 jobs per page
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    return render(request, "gearupjob/all_jobs.html", {'jobs': jobs})


@login_required(login_url='accounts:login')
def job_single(request, pk):
    job_query = get_object_or_404(Job, pk=pk)
    jobs = Job.objects.filter(title=job_query.title).order_by('view')

    company_name = ''
    if Company.objects.filter(company_username=request.user).exists():

        if str(job_query.Company_Username) == str(request.user):
            company_name = job_query.Company_Username

            context = {
                'q': job_query,
                'jobs': jobs,
                'company_name': company_name
            }
        else:
            return redirect('/')
    else:
        job_query.update_jobview()
        job_query.Company_Username.update_views()
        request.user.seeker.add_history(job_query.title)
        context = {
            'q': job_query,
            'jobs': jobs
        }

    return render(request, "gearupjob/job_single.html", context)


def ContactUs(request):
    return render(request, "gearupjob/contact.html")


@login_required(login_url='accounts:login')
def Search(request):
    if request.GET.get("query") != "" or request.GET.get("query1") != "" or request.GET.get("query2") != "":
        if request.GET.get("query") != "":
            q = request.GET['query']
            jobs = Job.objects.filter(Q(title__icontains=q) | Q(job_type__icontains=q) | Q(job_location__icontains=q) |
                                      Q(responsibilities__icontains=q) | Q(gender__icontains=q) | Q(description__icontains=q))
            request.user.seeker.add_history(q)
            if request.GET.get("query1") != "":
                q1 = request.GET['query1']
                jobs = jobs.filter(Q(job_location__icontains=q1))
                if request.GET.get("query2") != "":
                    q2 = request.GET['query2']
                    jobs = jobs.filter(Q(job_category__icontains=q2))
            else:
                q2 = request.GET['query2']
                jobs = jobs.filter(Q(job_category__icontains=q2))

        elif request.GET.get("query1") != "":
            q1 = request.GET['query1']
            jobs = Job.objects.filter(Q(job_location__icontains=q1))
            if request.GET.get("query2") != "":
                q2 = request.GET['query2']
                jobs = jobs.filter(Q(job_category__icontains=q2))
        else:
            q2 = request.GET['query2']
            jobs = Job.objects.filter(Q(job_category__icontains=q2))

        paginator = Paginator(jobs, 5)  # Show 5 jobs per page
        page = request.GET.get('page')
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)
        if request.GET.get("query") != "" or request.GET.get("query1") != " ":
            if request.GET.get("query") != "":
                q = request.GET['query']
                company_list = Company.objects.filter(
                    Q(company_name__icontains=q) | Q(address__icontains=q) | Q(description__icontains=q))
                if request.GET.get("query1") != "":
                    q1 = request.GET['query1']
                    company_list = company_list.filter(
                        Q(address__icontains=q1))

            else:
                q1 = request.GET['query1']
                company_list = Company.objects.filter(Q(address__icontains=q1))

        paginator = Paginator(company_list, 5)  # Show 5 jobs per page
        page = request.GET.get('page')
        try:
            company_list = paginator.page(page)
        except PageNotAnInteger:
            company_list = paginator.page(1)
        except EmptyPage:
            company_list = paginator.page(paginator.num_pages)
        context = {
            'jobs': jobs,
            'company_list': company_list,
            'query': request.GET.get("query"),
            'query1': request.GET.get("query1"),
            'query2': request.GET.get("query2"),
        }
        return render(request, "gearupjob/search.html", context)
    else:
        return redirect('gearupjob:index')


@login_required(login_url='accounts:login')
def rate_us(request, pk1, pk2):
    company = get_object_or_404(Company, pk=pk1)
    if Seeker.objects.filter(seeker=request.user).exists():
        if Rating.objects.filter(seeker_pk=request.user.seeker.pk).exists():
            already_rated_pk = Rating.objects.filter(seeker_pk=request.user.seeker.pk)
            list=[]
            for pk in already_rated_pk:
                list.append(pk.company_pk)
            if pk1 not in list:
                company.update_rating(pk2)
                rating = Rating(seeker_pk=request.user.seeker,company_pk=pk1)
                rating.save()
                rating.save_pk(pk1)
                messages.success(
                    request, "Thank You! Your rating was submitt!")
            else:
                messages.success(
                    request, "Sorry! You have already Rated!")
        else:
            company.update_rating(pk2)
            rating = Rating(seeker_pk=request.user.seeker,company_pk=pk1)
            rating.save()
            rating.save_pk(pk1)
            messages.success(
                request, "Thank You! Your rating was submitt!")
    else:
        messages.success(
                request, "Sorry! You cannot Rated!")
    rating = company.rating
    return render(request, 'accounts/company_detail.html', {'company_detail': company, 'rating': rating})


def clickme(request):
    test = 3.1
    return render(request, 'gearupjob/test.html', {'rating': test})

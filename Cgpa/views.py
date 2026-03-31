from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse 

# Create your views here.
@login_required
def home(request):
    return render(request,'home.html')

@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request,'login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login_page') 

    return render(request, 'register.html')

@login_required
def  profile_page(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.email = request.POST.get('email')
        profile.college = request.POST.get('college')
        profile.department = request.POST.get('department')
        profile.year = request.POST.get('year')
        
        profile.save()

    return render(request, 'profile.html', {'profile':profile})

def get_subjects(request):
    dept_id  = request.GET.get('department')
    semester = request.GET.get('semester')
    data = []
    if dept_id and semester:
        subjects = Subject.objects.filter(department_id=dept_id, semester=semester)
        data = [{'id': s.id, 'name': s.name, 'credits': s.credits} for s in subjects]
    return JsonResponse({'subjects': data})
 
 
# ── Grade → points map ────────────────────────────────────────────────────────
GRADE_POINTS = {'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'U': 0}

@login_required
def add_semester_page(request):
    departments = Department.objects.all()
    gpa = cgpa = error = None
 
    if request.method == 'POST':
        dept_id  = request.POST.get('department')
        semester = request.POST.get('semester')
        subjects = Subject.objects.filter(department_id=dept_id, semester=semester)
 
        if not subjects.exists():
            error = "No subjects found. Please add subjects via the admin panel first."
        else:
            total_points = total_credits = 0
            for sub in subjects:
                grade  = request.POST.get(f'grade_{sub.id}', 'U')
                total_points  += GRADE_POINTS.get(grade, 0) * sub.credits
                total_credits += sub.credits
 
            if total_credits:
                gpa = round(total_points / total_credits, 2)
                Semester_Result.objects.update_or_create(
                    user=request.user, semester=semester,
                    defaults={'gpa': gpa}
                )
 
    all_results = Semester_Result.objects.filter(user=request.user).order_by('semester')
    if all_results.exists():
        cgpa = round(sum(r.gpa for r in all_results) / all_results.count(), 2)
 
    return render(request, 'add_semester.html', {
        'departments': departments,
        'gpa':         gpa,
        'cgpa':        cgpa,
        'all_results': all_results,
        'error':       error,
    })
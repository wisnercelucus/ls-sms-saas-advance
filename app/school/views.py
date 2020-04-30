from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from school.models import (
	Pupil,
 	Attendance,
 	Course,
 	ExamMark,
 	Teacher,
 	Responsible,
 	AcademicYear,
 	Term,
 	Grade,
 )
from customer.models import Client
from school.forms import (
	PupilForm,
	AttendanceForm,
	CourseForm,
	ExamMarkForm,
	TeacherForm,
	ResponsibleForm,
	AcademicYearForm,
	TermForm,
	GradeForm,
	)

@login_required
def index(request):
	tenant = request.tenant
	print(dir(request.user))
	context = {'school':tenant}
	return render(request, 'school/index.html', context)

@login_required
class PupilListView(ListView):
	model = Pupil
	templatename = 'list_pupil.html'
	context_object_name = 'pupils'

# Pupil related
@login_required
def get_pupil_list(request):
	if request.method == 'GET':
		pupils = Pupil.objects.all()
		form = PupilForm()
		context = { 'school':request.tenant, 'pupils': pupils, 'form': form }
		return render(request, 'school/list_pupil.html', context)
	if request.method == "POST":
		form = PupilForm(data = request.POST)
		if form.is_valid():
			pupil = form.save(commit=False)
			pupil.user = request.user
			pupil.save_m2m()
			return redirect('school:list_pupil')
		else:
			return redirect('/')


@login_required
def get_detail_pupil(request, pk):
	pupil = get_object_or_404(Pupil, pk=pk)
	context = {'pupil': pupil, 'pk':pk}
	return render(request, 'school/show_detail_pupil.html', context)


@login_required
def update_pupil(request, pk):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method == 'POST':
		pupil = get_object_or_404(Pupil, pk=pk)
		form = PupilForm(request.POST or None,  
			request.FILES or None, 
			instance=pupil)

		if form.is_valid():
			pupil = form.save(commit=False)
			pupil.save()
			form.save_m2m()
			return redirect('school:list_pupil')
	else:
		pupil = get_object_or_404(Pupil, pk=pk)
		form = PupilForm(request.POST or None,  
			request.FILES or None, 
			instance=pupil)

		label ="Update"	
		context = {
			'form': form,
			'label':label,
		}
		return render(request, 'school/pupil_form.html', context)


@login_required
def add_new_pupil(request):
	if request.method == 'GET':
		form = PupilForm()
		label ="New pupil"
		tenant = request.tenant
		context = {
			'form': form,
			'label':label,
			'school':tenant,
		}
		return render(request, 'school/pupil_form.html', context)
	elif request.method == 'POST':
		form = PupilForm(data = request.POST)
		if form.is_valid():
			pupil = form.save(commit=False)
			pupil.user = request.user
			pupil.save()
			form.save_m2m()
			return redirect('school:list_pupil')
		else:
			return redirect('/')



# Attendances

@login_required
def get_attendance_list(request):
	if request.method == 'GET':
		form = AttendanceForm()
		attendances = Attendance.objects.all()
		tenant = request.tenant

		context = {
		'school': tenant, 
		'form': form, 
		'attendances': attendances 
		}
		return render(request, 'school/list_attendance.html', context)
	else:
		form = AttendanceForm(data= request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_attendance')

@login_required
def add_new_attendance(request):
	if request.method == 'GET':
		form = AttendanceForm()
		tenant = request.tenant
		context = {
			'school': tenant, 
			'form': form,  
		}
		return render(request, 'school/attendance_form.html', context)
	if request.method == 'POST':
		form = AttendanceForm(data = request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_attendance')
		else:
			print('invalid form')
			return redirect('/')

@login_required
def get_detail_attendance(request, pk):
	attendance = get_object_or_404(Attendance, pk=pk)
	tenant = request.tenant
	context = {'school':tenant, 'attendance': attendance, 'pk':pk}
	return render(request, 'school/show_detail_attendance.html', context)

@login_required
def update_attendance(request, pk):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method == 'POST':
		attendance = get_object_or_404(Attendance, pk=pk)
		form = AttendanceForm(request.POST or None,  
				request.FILES or None, 
				instance=attendance)

		if form.is_valid():
			attendance = form.save(commit=False)		
			attendance.save()
			return redirect('school:list_attendance')
	else:
		attendance = get_object_or_404(Attendance, pk=pk)
		form = AttendanceForm(request.POST or None,  
			request.FILES or None, 
			instance=attendance)
		tenant = request.tenant
		context = {'school':tenant, 
			'form':form,
			'attendance': attendance, 
			'pk':pk}
		return render(request, 'school/attendance_form.html', context)


#Course section

@login_required
def get_course_list(request):
	if request.method == 'GET':
		form = CourseForm()
		courses = Course.objects.all()
		tenant = request.tenant
		context = {'school': tenant, 'form':form, 'courses':courses }
		return render(request, 'school/list_course.html', context)
	else:
		form = CourseForm(data = request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_course')

@login_required
def add_new_course(request):
	if request.method == 'GET':
		form = CourseForm()
		tenant = request.tenant
		context = {'school': tenant, 'form': form}
		return render(request, 'school/course_form.html', context)
	if request.method == 'POST':
		form =  CourseForm(data = request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_course')
		else:
			return redirect('/')

@login_required
def get_detail_course(request, pk):
	course = get_object_or_404(Course, pk=pk)
	tenant = request.tenant
	context = {'school': tenant, 'course': course}
	return render(request, 'school/show_detail_course.html', context)


@login_required
def update_course(request, pk):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method == 'POST':
		course = get_object_or_404(Course, pk=pk)
		form = CourseForm(request.POST or None,  request.FILES or None, instance=course)
		if form.is_valid():
			course = form.save(commit=False)		
			course.save()
			return redirect('school:list_course')
	else:
		course = get_object_or_404(Course, pk=pk)
		form = CourseForm(
			request.POST or None,  
			request.FILES or None, 
			instance=course )	

		tenant = request.tenant
		context = {
			'form': form,
			'course':course,
		}
		return render(request, 'school/course_form.html', context)

# Section Exam Marks
@login_required
def get_mark_list(request):
	if request.method == 'GET':
		form = ExamMarkForm()
		marks = ExamMark.objects.all()
		tenant = request.tenant
		context = {'school': tenant, 'form':form, 'marks':marks }
		return render(request, 'school/list_mark.html', context)
	else:
		form = ExamMarkForm(data= request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_mark')

@login_required
def add_new_mark(request):
	if request.method == 'GET':
		form = ExamMarkForm()
		tenant = request.tenant
		context = {'school': tenant, 'form':form}
		return render(request, 'school/mark_form.html', context)
	if request.method == 'POST':
		form = ExamMarkForm(data = request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_mark')
		else:
			return redirect('/')

@login_required
def get_detail_mark(request, pk):
	mark = get_object_or_404(ExamMark, pk=pk)
	tenant = request.tenant
	context = {'school': tenant, 'mark':mark}
	return render(request, 'school/show_detail_mark.html', context)

@login_required
def update_mark(request, pk):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method == 'POST':
		mark = get_object_or_404(ExamMark, pk=pk)
		form = ExamMarkForm(
			request.POST or None,  
			request.FILES or None, 
			instance=mark)

		if form.is_valid():
			mark = form.save(commit=False)		
			mark.save()
			return redirect('school:list_mark')
	else:
		mark = get_object_or_404(ExamMark, pk=pk)
		form = ExamMarkForm(
			request.POST or None,  
			request.FILES or None, 
			instance=mark)	

		tenant = request.tenant
		context = {
			'form': form,
			'mark':mark,
		}
		return render(request, 'school/mark_form.html', context)


# Section Teacher
@login_required
def get_teacher_list(request):
	if request.method == 'GET':
		teachers= Teacher.objects.all()
		tenant = request.tenant
		context = {
		'school': tenant,
		'teachers': teachers 
		}
		return render(request, 'school/list_teacher.html', context)
	else:
		form = TeacherForm(data=request.POST)
		if form.is_valid():
			teacher = form.save(commit=False)
			teacher.user = request.user
			teacher.save_m2m()
			return redirect('school:list_teacher')
		else:
			return redirect('/')

@login_required
def add_new_teacher(request):
	if request.method == 'GET':
		form = TeacherForm()
		tenant = request.tenant
		context = {
		'school': tenant, 
		'form': form,  
		}
		return render(request, 'school/teacher_form.html', context)
	else:
		form = TeacherForm(data=request.POST)
		if form.is_valid():
			teacher = form.save(commit=False)
			teacher.user = request.user
			teacher.save()
			form.save_m2m()
			return redirect('school:list_teacher')
		else:
			return redirect('/')


@login_required
def get_detail_teacher(request, pk):
	teacher = get_object_or_404(Teacher, pk=pk)
	tenant = request.tenant
	context = {'school': tenant, 'teacher':teacher}
	return render(request, 'school/show_detail_teacher.html', context)

@login_required
def update_teacher(request, pk):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method == 'POST':
		teacher = get_object_or_404(Teacher, pk=pk)
		form = TeacherForm(request.POST or None,  
			request.FILES or None, 
			instance=teacher
			)

		if form.is_valid():
			teacher = form.save(commit=False)
			teacher.save()		
			form.save_m2m()
			return redirect('school:list_teacher')
	else:
		teacher = get_object_or_404(Teacher, pk=pk)
		form = TeacherForm(
			request.POST or None,  
			request.FILES or None, 
			instance=teacher )	

		tenant = request.tenant
		context = {
			'form': form,
			'teacher':teacher,
		}
		return render(request, 'school/teacher_form.html', context)


#Grade Stuff
@login_required
def get_grade_list(request):
	if request.method == 'GET':
		grades = Grade.objects.all()
		tenant = request.tenant
		context = {'grades':grades, 'school': tenant}
		return render(request, 'school/list_grade.html', context)
	else:
		form = GradeForm(data=request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_grade')
		else:
			return redirect('/')

@login_required
def add_new_grade(request):
	if request.method == 'GET':
		form = GradeForm()
		tenant = request.tenant
		label = 'Add new academic year'
		context = {
		'school': tenant, 
		'form': form, 
		'label': label, 
		}
		return render(request, 'school/grade_form.html', context)
	else:
		form = GradeForm(data=request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_grade')
		else:
			return redirect('/')

@login_required
def get_detail_grade(request, pk):
	grade = get_object_or_404(Grade, pk=pk)
	tenant = request.tenant
	context = {'school': tenant, 'grade':grade}
	return render(request, 'school/show_detail_grade.html', context)

@login_required
def update_grade(request, pk):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method == 'POST':
		grade = get_object_or_404(Grade, pk=pk)
		form = GradeForm(
			request.POST or None,  
			request.FILES or None, 
			instance=grade)
		if form.is_valid():
			mark = form.save(commit=False)		
			mark.save()
			return redirect('school:list_grade')
	else:
		grade = get_object_or_404(Grade, pk=pk)
		form = GradeForm(
			request.POST or None,  
			request.FILES or None, 
			instance=grade)	

		tenant = request.tenant
		context = {
			'form': form,
			'mark':grade,
		}
		return render(request, 'school/grade_form.html', context)

# Term stuff
@login_required
def get_term_list(request):
	if request.method == 'GET':
		terms = Term.objects.all()
		tenant = request.tenant
		context = {'terms':terms, 'school': tenant}
		return render(request, 'school/list_term.html', context)
	else:
		form = TermForm(data=request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_term')
		else:
			return redirect('/')
	
def add_new_term(request):
	if request.method == 'GET':
		form = TermForm()
		tenant = request.tenant
		label = 'Add new term'
		context = {
		'school': tenant, 
		'form': form,
		'label': label,
		}
		return render(request, 'school/term_form.html', context)
	else:
		form = TermForm(data=request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_term')
		else:
			return redirect('/')

@login_required
def get_detail_term(request, pk):
	term = get_object_or_404(Term, pk=pk)
	tenant = request.tenant
	context = {'school': tenant, 'term':term}
	return render(request, 'school/show_detail_term.html', context)	

@login_required
def update_term(request, pk):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method == 'POST':
		term = get_object_or_404(Term, pk=pk)
		form = TermForm(request.POST or None,  
			request.FILES or None, 
			instance=term
			)

		if form.is_valid():
			term = form.save(commit=False)		
			term.save()
			return redirect('school:list_term')
	else:
		term = get_object_or_404(Term, pk=pk)
		form = TermForm(
			request.POST or None,  
			request.FILES or None, 
			instance=term )	

		tenant = request.tenant
		label='Update term'
		context = {
			'form': form,
			'term': term,
			'label': label,
		}
		return render(request, 'school/term_form.html', context)

# Academic Year
@login_required
def get_ac_list(request):
	if request.method == 'GET':
		academic_years = AcademicYear.objects.all()
		tenant = request.tenant
		context = {'academic_years': academic_years, 'school': tenant}
		return render(request, 'school/list_academic_year.html', context)
	else:
		form = AcademicYearForm(data=request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_ac')
		else:
			return redirect('/')

@login_required	
def add_new_ac(request):
	if request.method == 'GET':
		form = AcademicYearForm()
		tenant = request.tenant
		label = 'Add academic year'
		context = {
		'school': tenant, 
		'form': form,
		'label': label,  
		}
		return render(request, 'school/academic_year_form.html', context)
	else:
		form = AcademicYearForm(data=request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_ac')
		else:
			return redirect('/')

@login_required
def get_detail_ac(request, pk):
	academic_year = get_object_or_404(AcademicYear, pk=pk)
	tenant = request.tenant
	context = {'school': tenant, 'academic_year': academic_year}
	return render(request, 'school/show_detail_academic_year.html', context)
 
@login_required   
def update_ac(request, pk):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method == 'POST':
		academic_year = get_object_or_404(AcademicYear, pk=pk)
		form = AcademicYearForm(request.POST or None,  
			request.FILES or None, 
			instance=academic_year
			)

		if form.is_valid():
			academic_year = form.save(commit=False)		
			academic_year.save()
			return redirect('school:list_ac')
	else:
		academic_year = get_object_or_404(AcademicYear, pk=pk)
		form = AcademicYearForm(
			request.POST or None,  
			request.FILES or None, 
			instance=academic_year )	

		tenant = request.tenant
		label = 'Update academic year'
		context = {
			'form': form,
			'academic_year':academic_year,
			'label': label,
		}
		return render(request, 'school/ac_form.html', context)

# Section responsibles
@login_required
def get_responsible_list(request):
	if request.method == 'GET':
		form = ResponsibleForm()
		responsibles = Responsible.objects.all()
		tenant = request.tenant
		context = {'school': tenant, 'form':form, 'responsibles':responsibles}
		return render(request, 'school/list_responsible.html', context)
	else:
		form = ResponsibleForm(data = request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_responsible')

@login_required
def add_new_responsible(request):
	if request.method == 'GET':
		form = ResponsibleForm()
		tenant = request.tenant
		context = {'form': form, 'school': tenant}

		return render(request, 'school/responsible_form.html', context)
	if request.method == 'POST':
		form = ResponsibleForm(data = request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			return redirect('school:list_responsible')
		else:
			return redirect('/')

@login_required
def get_detail_responsible(request, pk):
	responsible = get_object_or_404(Responsible, pk=pk)
	tenant = request.tenant
	context = {'responsible': responsible, 'school': tenant}
	return render(request, 'school/show_detail_responsible.html', context)

@login_required
def update_responsible(request, pk):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	if request.method == 'POST':
		responsible = get_object_or_404(Responsible, pk=pk)
		form = ResponsibleForm(request.POST or None,  
			request.FILES or None, 
			instance=responsible)

		if form.is_valid():
			responsible = form.save(commit=False)		
			responsible.save()
			return redirect('school:list_responsible')
	else:
		responsible = get_object_or_404(Responsible, pk=pk)
		form = ResponsibleForm(request.POST or None,  
			request.FILES or None, 
			instance=responsible )

		tenant = request.tenant
		context = {'form': form, 'school': tenant, 'responsible':responsible}
		return render(request, 'school/responsible_form.html', context)
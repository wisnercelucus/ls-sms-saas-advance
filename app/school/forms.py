from django import forms
from school.models import *



class PupilForm(forms.ModelForm):

	class Meta:
		model = Pupil
		fields = (
			'first_name',
			'last_name',
			'email',
			'sex',
			'phone',
			'mobile',
			'city',
			'photo',
			'address',
			'enrolment_date',
			'birth_date',
			'responsible',
			)


class AttendanceForm(forms.ModelForm):

	class Meta:
		model = Attendance
		fields = (
			'date',
			'pupil',
			'attended',
			'left_early',
			'remarks',
			'reason_of_leaving',

			)


class ExamMarkForm(forms.ModelForm):

	class Meta:
		model = ExamMark
		fields = (
			'course',
			'pupil',
			'term',
			'date',
			'mark',
			)


class CourseForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = (
			'name',
			'base',
			'coefficient',
			'grade',
			'code',
			'term',
			'description',
			)


class GradeForm(forms.ModelForm):

	class Meta:
		model = Grade
		fields = (
			'name',
			'description',
			)


class TermForm(forms.ModelForm):

	class Meta:
		model = Term
		fields = (
			'name',
			'start_date',
			'end_date',
			)

class AcademicYearForm(forms.ModelForm):

	class Meta:
		model = AcademicYear
		fields = (
			'name',
			'start_date',
			'end_date',
			)

class TeacherForm(forms.ModelForm):

	class Meta:
		model = Teacher
		fields = (
			'first_name',
			'last_name',
			'email',
			'sex',
			'phone',
			'mobile',
			'city',
			'photo',
			'address',
			'active',
			'course',
			'academic_level'
			)


class ResponsibleForm(forms.ModelForm):

	class Meta:
		model = Responsible
		fields = (
			'first_name',
			'last_name',
			'email',
			'sex',
			'phone',
			'mobile',
			'city',
			'photo',
			'address',
			'profession',
			'education_level',
			'reslationshipWithPupil'
			)

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Document
		fields = (
				'upload',
			)
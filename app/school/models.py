from django.db import models
from django.utils import timezone
from django.conf import settings


SEXES = (
	('','Select'),
	('male','Male'),
	('female', 'Female'),
	('other','Other'),
	)

ACADEMIC_LEVEL = (
	('', 'Select'),
	('university', 'University'),
	('secondary', 'Secondary'),
	('primary', 'Primary'),
	('no level', 'No level'),
	)

RELATIONSHIP_WITH_PUPIL =(
	('parent', 'Parent'),
	('uncle', 'Uncle'),
	('aunt', 'Aunt'),
	('friend', 'Friend'),
	('cousin', 'Cousin'),
	('adoption', 'Adoption'),
	)


class TimeStamp(models.Model):
	""" Add created and modified date, owner 
	    and modifier to each object created
	"""
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE, null=True)

	class Meta:
		abstract = True

# Meta
class BasicDesc(models.Model):
	first_name = models.CharField(max_length=255, null=True)
	last_name = models.CharField(max_length=255, null=True)
	email = models.EmailField(null=True)
	sex = models.CharField(choices=SEXES, max_length=10, null=True)
	phone = models.CharField(max_length=50, null=True)
	mobile = models.CharField(max_length=50, null=True)
	city = models.CharField(max_length=50, null=True)
	address = models.CharField(max_length=250, null=True)

	class Meta:
		abstract = True

# End Meta


class Responsible(BasicDesc, TimeStamp):
	profession = models.CharField(max_length=255, null=True)
	education_level = models.CharField(max_length=70, null=True)
	reslationshipWithPupil = models.CharField(
							max_length=250, 
							choices=RELATIONSHIP_WITH_PUPIL, 
							null=True)
	photo = models.ImageField(upload_to='school_images', blank=True, null=True)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Pupil(BasicDesc, TimeStamp):
	enrolment_date = models.DateField(null=True)
	birth_date = models.DateField(blank=True, null=True)
	active = models.BooleanField(default=True)
	photo = models.ImageField(upload_to='school_images', blank=True, null=True)
	responsible = models.ManyToManyField(Responsible)



class Term(TimeStamp):
	name = models.CharField(max_length=255, null=True)
	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)

	def __str__(self):
		return self.name

class AcademicYear(TimeStamp):
	name = models.CharField(max_length=255, null=True)
	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)


class Document(TimeStamp):
	upload = models.FileField(upload_to='documents')


class Grade(TimeStamp):
	name = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=255, null=True)

	def __str__(self):
		return self.name



class Course(TimeStamp):
	name = models.CharField(max_length=255)
	description = models.CharField(max_length=255, null=True)
	base = models.IntegerField(default=0, null=True)
	coefficient = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)
	code = models.CharField(max_length=255, blank=True, null=True)
	term = models.ForeignKey(Term, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.name


class Teacher(BasicDesc, TimeStamp):
	academic_level = models.CharField(max_length=250, choices=ACADEMIC_LEVEL, null=True)
	active = models.BooleanField(default=True)
	photo = models.ImageField(upload_to='school_images', blank=True, null=True)
	course = models.ManyToManyField(Course)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class ExamMark(TimeStamp):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
	pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, null=True)
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)
	date = models.DateField()
	mark = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	term = models.ForeignKey(Term, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.course.name


class Attendance(TimeStamp):
	date = models.DateField()
	pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, null=True)
	attended = models.BooleanField(default=True)
	remarks = models.CharField(max_length=255, default="NA")
	left_early = models.BooleanField(default=False)
	reason_of_leaving = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.pupil.first_name + ' ' + self.pupil.first_name



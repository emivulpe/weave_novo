### Refactored + TODO ###
@requires_csrf_token
def log_info_db(request):
	try:
		time_on_step = request.POST['time']
		current_step = int(request.POST['step'])
		direction = request.POST['direction']
		application_name = request.POST['example_name']
	except KeyError:
		return HttpResponse(simplejson.dumps({'error':'Bad input supplied'}), content_type="application/json")
	session_id = request.session.session_key

	print current_step, "CURR STER"
	print direction, "DIRR"
	if direction == "back":
		current_step = int(current_step) + 1
	#### TODO add some checks if these exist ####
	try:
		application = Application.objects.filter(name=application_name)[0]
		step = Step.objects.filter(application=application, order = current_step)[0]
		print step, "STEP TEST"
	except IndexError:
		return HttpResponse(simplejson.dumps({'error':'Bad input supplied'}), content_type="application/json")
		
	record = UsageRecord(application = application, session_id = session_id, time_on_step = time_on_step, step = step, direction = direction)
	
	teacher_name=request.session.get("teacher",None)

	if teacher_name != None:
	
		user=User.objects.filter(username=teacher_name)
		teacher=Teacher.objects.filter(user=user)
		
		#### TODO maybe remove these checks. It is impossible that they don't exist.... ####
		if len(teacher)>0:
			teacher=teacher[0]
			record.teacher = teacher
			group_name=request.session.get("group",None)
			year = request.session.get("year",None)
			if group_name != None and year != None:
				academic_year = AcademicYear.objects.filter(start = year)[0]
				print academic_year, "AY TEST"
				group = Group.objects.filter(teacher=teacher, academic_year = academic_year, name = group_name)
				if len(group) > 0:
					group=group[0]
					record.group = group
					student_name=request.session.get("student", None)
					if student_name != None:
						student = Student.objects.filter(teacher=teacher,group=group,student_id=student_name)
						if len(student) > 0:
							student=student[0]
							record.student = student

	record.save()
	return HttpResponse("{}",content_type = "application/json")
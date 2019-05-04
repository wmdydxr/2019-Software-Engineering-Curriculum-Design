from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from backstage.models import Student, Teacher, College, Major, MajorPlan, ClassRoom, AdmClass,User
from scoreManagement.models import Teaching, Course, MajorPlan, MajorCourses, CourseScore, EvaluationForm
from django.http import JsonResponse,HttpResponseRedirect

def welcome(request):
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    print(teachers)

    colleges = College.objects.all()
    majors = Major.objects.all()
    major_plans = MajorPlan.objects.all()
    class_rooms = ClassRoom.objects.all()

    context = {
        'students': students,
        'teachers': teachers,
    }
    return render(request, 'scoreManage/student_score_manage.html', context)


def adm_all_course_score(request):
    all_course_score = CourseScore.objects.all()[:20]

    print(len(all_course_score))
    context = {"all_course_score": all_course_score}
    return render(request, 'scoreManage/adm_score_manage.html', context)


def score_home_page(request):
    if request.session['user_type'] == '学生':
        return render(request, 'scoreManage/student_score_manage.html')
    elif request.session['user_type'] == '教师':
        return render(request, 'scoreManage/teacher_score_manage.html')
    else:
        return render(request, 'scoreManage/adm_score_manage.html')

# 学生评教
def assess_teacher(request):
    # 判断该学生是否已经全部提交过
    def judge(s):
        items = EvaluationForm.objects.filter(student_id=s)
        if len(items) != 0:
            for item in items:
                if item.is_finish == False:
                    return False  # 该学生还未提交
                else:
                    return True   # 该学生已经提交
        else:
            return False

    log = []
    stuno = request.session['username']
    sno_id = stuno[4:]  # 得到学生id
    stu = Student.objects.filter(username = stuno)
    courses = CourseScore.objects.filter(sno = sno_id)  # 从选课表中找出该学生修的课程
    num1 = 0
    sum = 0
    for item1 in courses:
        teachings = Teaching.objects.filter(id = item1.teaching_id)
        for item2 in teachings:
            if item2.mcno.year == 2017 and item2.mcno.semester == 1:
                # print(item2)
                # print(item2.tno.name)
                # print(item2.mcno.cno.cname)
                # print(item2.mcno.cno.course_type)
                temp = dict()
                temp['student'] = stuno
                temp['sno'] = stu  # 学生
                temp['cno'] = item2.mcno.cno  # 课程
                # print(item2.mcno.cno)
                temp['course'] = item2.mcno.id
                temp['tno'] = item2.tno  # 教师
                temp['teacher'] = item2.tno_id
                # print(item2.tno_id)
                temp['state'] = False
                temp['r1'] = 0
                temp['r2'] = 0
                temp['r3'] = 0
                temp['r4'] = 0
                temp['r5'] = 0
                temp['r6'] = 0
                temp['r7'] = 0
                temp['r8'] = 0
                temp['text'] = "无"
                temp['flag'] = False
                try:
                    temp1 = EvaluationForm.objects.get(student_id=sno_id, course_id=item2.mcno.id, teacher_id=item2.tno_id)
                    temp['r1'] = temp1.item1
                    temp['r2'] = temp1.item2
                    temp['r3'] = temp1.item3
                    temp['r4'] = temp1.item4
                    temp['r5'] = temp1.item5
                    temp['r6'] = temp1.item6
                    temp['r7'] = temp1.item7
                    temp['r8'] = temp1.item8
                    temp['text'] = temp1.description
                    temp['flag'] = temp1.is_finish
                    # print("!!!")
                    # if temp1.is_finish == True:
                    temp['state'] = True
                    num1 += 1
                except:
                    temp['state'] = False
                    # print("???")
                    pass

                temp['tname'] = item2.tno.name
                temp['cname'] = item2.mcno.cno.cname
                # print(item2.tno.id)
                temp['type'] = item2.mcno.cno.course_type
                # if temp1.is_finish == True:
                #     temp['state'] = "提交"
                # else:
                #     temp['state'] = "未提交"
                sum += 1
                log.append(temp)
    # print(log)
    num2 = sum-num1
    flag = judge(sno_id)
    context = {'log' : log, 'num1': num1, 'num2': num2, 'flag': flag}

    return render(request, 'scoreManage/assess_teacher.html', context = context)


# 学生提交评价信息
def submit_result(request):
    print("!!!")
    # 得到各个等级对应的分数
    def getScore(s):
        if s == 'A':
            return 100
        elif s == 'B':
            return 90
        elif s == 'C':
            return 70
        elif s == 'D':
            return 60
        elif s == 'E':
            return 50
    # if 'submit_result' in request.POST:
    if request.GET:
        r1 = request.GET.get('r1')
        r2 = request.GET.get('r2')
        r3 = request.GET.get('r3')
        r4 = request.GET.get('r4')
        r5 = request.GET.get('r5')
        r6 = request.GET.get('r6')
        r7 = request.GET.get('r7')
        r8 = request.GET.get('r8')
        text = request.GET.get('message')
        if text == "":
            text = "无"
        item_sno = request.GET.get('item_sno')
        item_tno = request.GET.get('item_tno')
        item_cno = request.GET.get('item_cno')

        r1 = getScore(r1)
        r2 = getScore(r2)
        r3 = getScore(r3)
        r4 = getScore(r4)
        r5 = getScore(r5)
        r6 = getScore(r6)
        r7 = getScore(r7)
        r8 = getScore(r8)
        print(r1, r2, r3, r4, r5, r6, r7, r8, text)
        sum = r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8
        ave = sum*1.0 / 8
        # print(ave)
        # print(type(item_sno), type(item_tno), type(item_cno))
        # 学生对象
        student = Student.objects.get(username=item_sno)
        # print(student)
        # 教师对象
        # print(item_tno)
        teacher = Teacher.objects.get(id=item_tno)
        # print(teacher)
        # 课程对象
        course = MajorCourses.objects.get(id=item_cno)
        # print(course)
        print("!!!")
        try:
            EvaluationForm.objects.get(student=student, course=course, teacher=teacher)
            EvaluationForm.objects.filter(student=student, course=course, teacher=teacher).update(item1=r1, item2=r2, item3=r3, item4=r4, item5=r5, item6=r6, item7=r7, item8=r8, description=text, sum=ave, is_finish=False)
        except:
            EvaluationForm.objects.create(student=student, course=course, teacher=teacher, item1=r1, item2=r2, item3=r3, item4=r4, item5=r5, item6=r6, item7=r7, item8=r8, description=text, sum=ave, is_finish=False)
        return redirect('./assess_teacher')

# # 最终的提交，提交后不可更改
@csrf_exempt
def submit_all(request):
    if request.GET:
        item_sno = request.session['username']
        # 学生对象
        student = Student.objects.get(username=item_sno)
        # 更改评价表的is_finish字段
        EvaluationForm.objects.filter(student=student).update(is_finish=True)
        return redirect('scoreManagement:assess_teacher')
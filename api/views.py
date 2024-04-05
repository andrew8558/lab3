import datetime
from collections import defaultdict

from django.db.models import Count, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import viewsets
from .serializers import *
from main.models import *


class RoomViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GetTeacherSerializer
        return TeacherSerializer


class ClassViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class StudentViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get_queryset(self):
        class_id = self.request.query_params.get('class_id')
        if class_id:
            return Student.objects.filter(class_assigned=class_id)
        else:
            return Student.objects.all()


class DisciplineViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ListSchedule
        return ScheduleSerializer


class GradeViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class StudentGrades(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        student_grades = Grade.objects.filter(student=student)
        serializer = StudentGradeSerializer(student_grades, many=True)
        return Response(serializer.data)


class TeacherSchedule(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher_schedule = Schedule.objects.filter(course__teacher=teacher)
        serializer = ScheduleSerializer(teacher_schedule, many=True)
        return Response(serializer.data)


class ClassByTeacherKey(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request, pk):
        class_obj = Class.objects.get(teacher__id=pk)
        serializer = ClassSerializer(class_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FreeRooms(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.all()
        not_free_rooms = Room.objects.filter(teacher__isnull=False)
        free_rooms = rooms.difference(not_free_rooms)
        serializer = RoomSerializer(free_rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectInClass(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request):
        class_letter = request.data.get('letter')
        class_number = request.data.get('number')
        date = request.data.get('date')
        lesson_number = request.data.get('lesson_number')

        cur_class = Class.objects.get(letter=class_letter, number=class_number)
        schedule = Schedule.objects.get(class_assigned=cur_class, day_of_week=datetime.datetime.strptime(date, '%Y-%m-%d'), number=lesson_number)
        subject = schedule.course.subject.name
        serializer = DisciplineSerializer(subject)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CountTeachersPerDiscipline(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request):
        teachers_per_discipline = defaultdict(set)
        courses = Course.objects.all()
        for course in courses:
            teachers_per_discipline[course.subject.name].add(course.teacher_id)
        result = {discipline: len(teachers) for discipline, teachers in teachers_per_discipline.items()}

        return Response(result, status=status.HTTP_200_OK)


class SameSubjectsTeacherICT(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request, pk):
        cur_class = Class.objects.get(pk=pk)
        ict = Discipline.objects.get(name="Информатика")
        course = Course.objects.get(class_id=cur_class, subject=ict)
        teacher_ict = course.teacher
        teacher_ict_courses = Course.objects.filter(teacher=teacher_ict)
        subjects_taught_by_teacher = set([course.subject for course in teacher_ict_courses])
        teachers = Teacher.objects.filter(course__subject__in=subjects_taught_by_teacher).exclude(id=teacher_ict.id).distinct()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenderCountsPerClass(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request, pk):
        class_obj = Class.objects.get(pk=pk)
        gender_counts = class_obj.student_set.values('gender').annotate(count=Count('gender'))
        gender_counts_dict = {'M': 0, 'F': 0}

        for i in gender_counts:
            gender = i['gender']
            count = i['count']
            gender_counts_dict[gender] = count

        return Response(gender_counts_dict,  status=status.HTTP_200_OK)


class CountRoomsPerDisciplineType(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request):
        basic_rooms_count = Room.objects.filter(is_profile=False).count()
        profile_rooms_count = Room.objects.filter(is_profile=True).count()
        return Response({"basic_rooms_count": basic_rooms_count, "profile_rooms_count": profile_rooms_count})


class ClassReport(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request, pk):
        class_obj = Class.objects.get(id=pk)

        students = class_obj.student_set.all()
        count_students = students.count()

        class_teacher = class_obj.teacher

        subject_average_grade = {}

        courses = Course.objects.filter(class_id=class_obj)

        for course in courses:
            grades = Grade.objects.filter(lesson=course)
            average_grade = grades.aggregate(avg_grade=Avg('grade'))['avg_grade']
            subject_average_grade[course.subject.name] = average_grade

        class_report = {
            'class_name': f'{class_obj.number}{class_obj.letter}',
            'total_students': count_students,
            'class_teacher': f'{class_teacher.last_name} {class_teacher.first_name} {class_teacher.middle_name}',
            'subject_average_grade': subject_average_grade,
        }

        return Response(class_report)

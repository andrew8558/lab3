from rest_framework import serializers
from main.models import Room, Teacher, Class, Student, Discipline, Course, Schedule, Grade


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Class
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    #class_assigned = ClassSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class_id = ClassSerializer()
    subject = DisciplineSerializer()

    class Meta:
        model = Course
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class StudentGradeSerializer(serializers.ModelSerializer):
    lesson = CourseSerializer()

    class Meta:
        model = Grade
        fields = '__all__'


class GetTeacherSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'


class ListSchedule(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Schedule
        fields = '__all__'

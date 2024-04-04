from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'rooms', RoomViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'students', StudentViewSet)
router.register(r'disciplines', DisciplineViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'grades', GradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('subject-in-class/', SubjectInClass.as_view(), name='subject_in_class'),
    path('count-teachers-per-discipline/', CountTeachersPerDiscipline.as_view(), name='teachers_per_discipline'),
    path('same-subject-teacher-ict/<int:pk>/', SameSubjectsTeacherICT.as_view(), name='same_subject_teachers'),
    path('gender-counts-per-class/<int:pk>/', GenderCountsPerClass.as_view(), name='gender_counts_per_class'),
    path('count-rooms-per-discipline-type/', CountRoomsPerDisciplineType.as_view(), name='rooms_per_discipline_type'),
    path('class-report/<int:pk>/', ClassReport.as_view(), name='class_report'),
    path('teacher-class/<int:pk>/', ClassByTeacherKey.as_view(), name='class_teacher'),
    path('teacher-schedule/<int:teacher_id>/', TeacherSchedule.as_view(), name='teacher_schedule'),
    path('student-grades/<int:student_id>/', StudentGrades.as_view(), name='student_grades'),
    path('free-rooms/', FreeRooms.as_view(), name='free_rooms'),
]



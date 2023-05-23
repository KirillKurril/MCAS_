from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerPage, name = 'register'),
    path('delete/<str:pk>', views.delete_user, name = 'delete-user'),

    path('profile/<str:pk>/', views.userProfile, name = 'user-profile'),

    path('delete-new/<str:pk>', views.deleteNew, name = 'delete-new'),
    path('edit-new/<str:pk>', views.editNew, name = 'edit-new'),
    path('edit-about/', views.editAbout, name = 'edit-about'),
    path('about/', views.about, name = 'about'),
    path('preview/', views.preview, name = 'preview'),

    path('teacher-list/', views.teachers, name = 'teacher-list'),

    path('music-library', views.musicLib, name = 'music-library'),
    path('upload/', views.file_upload, name = 'file-upload'),
    path('download/<str:pk>', views.download_file, name = 'file-download'),
    path('udownload/<str:pk>', views.download_ufile, name = 'ufile-download'),
    path('file-uupload/', views.file_uupload, name='file-uupload'),
    path('delete-file/<str:pk>', views.delete_file, name = 'delete-file'),

    path('rewards/', views.rewards, name = 'rewards'),

    path('teachers-info/<str:pk>', views.teachersInfo, name = 'teachers-info'),
    path('teachers-edit/<str:pk>', views.teacher_edit, name = 'teacher-edit'),
    path('student-info/<str:pk>', views.student_info, name='student-info'),
    path('student-edit/<str:pk>', views.student_edit, name='student-edit'),
    path('admin-page/<str:pk>', views.admin_page, name='admin-page'),
    path('teacher-page/<str:pk>', views.teacher_page, name='teacher-page'),
    path('group-info/<str:pk>', views.group_info, name='group-info'),

    path('piano-dep/', views.piano_department, name='piano-dep'),
    path('folk-dep/', views.folk_department, name='folk-dep'),
    path('strings-dep/', views.strings_department, name='strings-dep'),
    path('folk-strings-dep/', views.folk_strings_department, name='folk-strings-dep'),
    path('choir-dep/', views.choir_department, name='choir-dep'),
    path('theory-dep/', views.theory_department, name='theory-dep'),

    path('piano-events/', views.get_piano, name='piano-events'),
    path('strings-events/', views.get_strings, name='strings-events'),
    path('folk-events/', views.get_folk, name='folk-events'),
    path('string-folk-events/', views.get_string_folk, name='string-folk-events'),
    path('choir-events/', views.get_choir, name='choir-events'),
    path('theory-events/', views.get_theory, name='theory-events'),

    path('new-event/', views.new_event, name='new-event'),
    path('contingent/', views.contingent, name='contingent'),

    path('diary/<str:pk>', views.diary, name='diary'),
    path('homework/', views.homework, name='homework'),


    path('', views.home, name = 'home'),
    path('new/<str:pk>/', views.new, name = 'new'),
    path('create-new/', views.createNew, name = 'create-new'),
    path('news/', views.newsPage, name = 'news'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.UserRegistrationAPIView.as_view(), name='register'),
    url(r'^edit_user/$', views.edit_user, name='edit_user'),
    url(r'^all_users/$', views.Users.as_view(), name='all_users'),
    url(r'^user/$', views.User.as_view(), name='all_users'),
    url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
    url(r'^new_school/$', views.SchoolRegistrationAPIView.as_view(), name='new_school'),
    url(r'^visited_school/$', views.VisitedSchoolList.as_view(), name='visited_school'),
    url(r'^hypo_data/$', views.HypoCreationAPIView.as_view(), name='hypo_data'),
    url(r'^user_modules/$', views.ModulesList.as_view(), name='user_modules'),
    url(r'^hypo/$', views.HypoData.as_view(), name='hypo'),
    url(r'^update_school/(?P<pk>\d+)/$', views.SchoolUpdateAPIView.as_view(), name='update_school'),
    url(r'^update_school2/(?P<pk>\d+)/$', views.SchoolUpdateAPIView2.as_view(), name='update_school2'),
    url(r'^new_apt/$', views.SchoolAppointmentAPIView.as_view(), name='new_appointment'),
    url(r'^sop/$', views.SchoolRatingAPIView.as_view(), name='sop'),
    url(r'^schools/$', views.SchoolList.as_view(), name='schools'),
    url(r'^approve/$', views.approve_school, name='approve schools'),
    url(r'^delete/$', views.del_school, name='delete schools')
    ]
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.shortcuts import render
import random, json
from rest_framework import generics, status, views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from .models import *
from . import serializers
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models import Q
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
from ipware import get_client_ip

import xlsxwriter


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer
    queryset = User.objects.all()


class UserLoginAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MobileLoginAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.MobileLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def all_users_api(request):
    if request.method == 'GET':
        users = UserProfile.objects.all()
        serializer = serializers.UsersSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


class SchoolRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.SchoolRegistrationSerializer
    queryset = School.objects.all()


class SchoolUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = serializers.SchoolUpdateSerializer
    queryset = School.objects.all()
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        serializer = serializers.SchoolUpdateSerializer(data=request.data)
        if serializer.is_valid():
            school_id = self.kwargs["pk"]
            if School.objects.filter(parent_id__exact=school_id).exists():
                instance = School.objects.filter(parent_id__exact=school_id).order_by('-id')[0]
                serializer.update(instance, serializer.validated_data)
                return Response(status=204)
            elif School.objects.filter(id=school_id, revisit=False).exists():
                instance = School.objects.get(id=school_id)
                serializer.update(instance, serializer.validated_data)
                return Response(status=204)
            elif School.objects.filter(id=school_id, revisit=True, visited=True).exists():
                parent_school = School.objects.get(id=school_id)
                new_school = School(
                    name=parent_school.name,
                    state=parent_school.state,
                    lga=parent_school.lga,
                    address=parent_school.address,
                    lat=parent_school.lat,
                    lng=parent_school.lng,
                    contact_name=parent_school.contact_name,
                    contact_phone=parent_school.contact_name,
                    target_level=parent_school.target_level,
                    target_population=parent_school.target_population,
                    landmark=parent_school.landmark,
                    user=parent_school.user,
                    school_type=parent_school.school_type,
                    visited=True,
                    approved=True,
                    email=parent_school.email,
                    parent_id=parent_school.id,
                    revisited=True,
                    designation=parent_school.designation
                )
                new_school.save()
                serializer.update(new_school, serializer.validated_data)
                parent_school.revisit = False
                parent_school.revisited = True
                parent_school.save()
                return Response(status=204)


class SchoolUpdateAPIView2(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.SchoolUpdateSerializer
    queryset = School.objects.all()
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        serializer = serializers.SchoolUpdateSerializer(data=request.data)
        if serializer.is_valid():
            school_id = self.kwargs["pk"]
            if School.objects.filter(parent_id__exact=school_id).exists():
                instance = School.objects.filter(parent_id__exact=school_id).order_by('-id')[0]
                serializer.update(instance, serializer.validated_data)
                return Response(status=204)
            elif School.objects.filter(id=school_id, revisit=False).exists():
                instance = School.objects.get(id=school_id)
                serializer.update(instance, serializer.validated_data)
                return Response(status=204)
            elif School.objects.filter(id=school_id, revisit=True, visited=True).exists():
                parent_school = School.objects.get(id=school_id)
                new_school = School(
                    name=parent_school.name,
                    state=parent_school.state,
                    lga=parent_school.lga,
                    address=parent_school.address,
                    lat=parent_school.lat,
                    lng=parent_school.lng,
                    contact_name=parent_school.contact_name,
                    contact_phone=parent_school.contact_name,
                    target_level=parent_school.target_level,
                    target_population=parent_school.target_population,
                    landmark=parent_school.landmark,
                    user=parent_school.user,
                    school_type=parent_school.school_type,
                    visited=True,
                    approved=True,
                    email=parent_school.email,
                    parent_id=parent_school.id,
                    revisited=True,
                    designation=parent_school.designation,
                    level=parent_school.level,
                    school_phone=parent_school.school_phone
                )
                new_school.save()
                serializer.update(new_school, serializer.validated_data)
                parent_school.revisit = False
                parent_school.revisited = True
                parent_school.save()
                return Response(status=204)


class SchoolAppointmentAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.SchoolAppointment
    queryset = School.objects.all()


class SchoolRatingAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.SchoolRating
    queryset = School.objects.all()


class User(generics.ListAPIView):
    serializer_class = serializers.UsersSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = UserProfile.objects.all()


class SchoolList(generics.ListAPIView):
    serializer_class = serializers.SchoolSerializerLite
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self, *args, **kwargs):
        queryset = School.objects.filter(delete=False)
        user_id = self.request.GET.get("id")
        today = datetime.now().strftime("%Y-%m-%d")
        date_1 = datetime.strptime(today, "%Y-%m-%d")
        end_date = date_1 + timedelta(days=7)

        supervisor_name = self.request.GET.get('supervisor')
        country = self.request.GET.get('country')
        if country:
            queryset = queryset.filter(user__country=country, parent_id__isnull=True)
        if supervisor_name:
            queryset = queryset.filter(user__supervisor_id=supervisor_name, parent_id__isnull=True)
        if user_id:
            queryset = queryset.filter(Q(visit_date__gte=datetime.now()) & Q(visit_date__lte=end_date),
                                       Q(visited=False) | Q(revisit=True), user__id=user_id, approved=True, delete=False)
        return queryset


class VisitedSchoolList(generics.ListAPIView):
    serializer_class = serializers.VisitedSchoolSerializerLite
    permission_classes = ()

    def get_queryset(self, *args, **kwargs):
        queryset = School.objects.filter(visited=True).prefetch_related('user__userprofile_set', 'user__user')
        supervisor_name = self.request.GET.get('supervisor')
        country = self.request.GET.get('country')

        if country:
            queryset = queryset.filter(user__country=country)
        if supervisor_name:
            queryset = queryset.filter(user__supervisor_id=supervisor_name)

        return queryset


class Users(generics.ListAPIView):
    serializer_class = serializers.UsersSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self, *args, **kwargs):
        queryset = UserProfile.objects.all()
        role = self.request.GET.get("role")
        id = self.request.GET.get("id")
        admin = self.request.GET.get("admin")
        if admin:
            admin_user = UserProfile.objects.get(id=admin)
            admin_arr = []
            for i in admin_user.supervisor_module.all():
                admin_arr.append(i.name)
                # print (admin_arr)
            queryset = queryset.filter(Q(role='Supervisor') | Q(role='Marketing Executive'),
                                       Q(user_module__in=admin_arr) | Q(supervisor_module__name__in=admin_arr))

        if role:
            queryset = queryset.filter(role=role)
        if id:
            queryset = queryset.filter(id=id)
        supervisor = self.request.GET.get('supervisor')
        if supervisor:
            queryset = queryset.filter(supervisor__id=supervisor, role='Marketing Executive')
        return queryset


class Users02(generics.ListAPIView):
    serializer_class = serializers.UsersSerializer02Lite
    permission_classes = ()

    def get_queryset(self, *args, **kwargs):
        queryset = UserProfile.objects.all().prefetch_related('supervisor_module')
        role = self.request.GET.get("role")
        id = self.request.GET.get("id")
        admin = self.request.GET.get("admin")
        if admin:
            admin_user = UserProfile.objects.get(id=admin)
            admin_arr = []
            for i in admin_user.supervisor_module.all():
                admin_arr.append(i.name)
                # print (admin_arr)
            queryset = queryset.filter(Q(role='Supervisor') | Q(role='Marketing Executive'),
                                       Q(user_module__in=admin_arr) | Q(supervisor_module__name__in=admin_arr))

        if role:
            queryset = queryset.filter(role=role)
        if id:
            queryset = queryset.filter(id=id)
        supervisor = self.request.GET.get('supervisor')
        if supervisor:
            queryset = queryset.filter(supervisor__id=supervisor, role='Marketing Executive')
        return queryset


@csrf_exempt
def approve_school(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ObjIdSerializers(data=data)
        if serializer.is_valid():
            trip = School.objects.get(id=data['id'])
            trip.approved = True
            trip.save()
            done = {
                'message': 'Successful'
            }
            return JsonResponse(done, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def del_school(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ObjIdSerializers(data=data)
        if serializer.is_valid():
            trip = School.objects.get(id=data['id'])
            trip.delete = True
            trip.save()
            done = {
                'message': 'Successful'
            }
            return JsonResponse(done, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


class HypoCreationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.HypoCreationSerializer
    queryset = Hypo.objects.all()


class HypoCreationAPIView02(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.HypoCreationSerializer02
    queryset = Hypo.objects.all()


class HypoData(generics.ListAPIView):
    serializer_class = serializers.HypoSerializer
    permission_classes = ()

    def get_queryset(self, *args, **kwargs):
        queryset = Hypo.objects.filter(duplicate=False).prefetch_related('user', 'user__userprofile_set')
        user_id = self.request.GET.get("id")
        if user_id:
            queryset = queryset.filter(user__id=user_id, approved=True, delete=False)
        return queryset


class HypoUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = serializers.HypoUpdateSerializer
    queryset = Hypo.objects.all()
    lookup_field = 'app_uuid'


class ModulesList(generics.ListAPIView):
    serializer_class = serializers.UserModuleSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = UserModules.objects.all()


@csrf_exempt
def edit_user(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.UsrProfile(data=data)
        if serializer.is_valid():
            if data['id'] is not None:
                UserProfile.objects.update_user(data)
                user = UserProfile.objects.filter(id=data['id'])
                serializer = serializers.UsersSerializer(user, many=True)
                return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def edit_school(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.SchoolEditSerializer(data=data)
        if serializer.is_valid():
            if data['id'] is not None:
                School.objects.update_school(data)
                school = School.objects.filter(id=data['id'])
                serializer = serializers.SchoolRegistrationSerializer(school, many=True)
                return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def managers_reports(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ReportFilters(data=data)
        all_managers_arr = []

        if serializer.is_valid():
            if data['state'] is not None:
                if data['state'] == 'All':
                    all_managers = UserProfile.objects.filter(role='Marketing Executive', user_module='School Sampling')
                else:
                    all_managers = UserProfile.objects.filter(role='Marketing Executive', user_module='School Sampling',
                                                              state=data['state'])

                for i in all_managers:
                    created = School.objects.filter(user=i,
                                                    date_captured__range=[data['date_from'], data['date_to']]).count()
                    visited = School.objects.filter(user=i, visited=True,
                                                    date_captured__range=[data['date_from'], data['date_to']]).count()
                    cooking_sop = School.objects.filter(visited=True, user=i, date_captured__range=[data['date_from'],
                                                                                                    data[
                                                                                                        'date_to']]).aggregate(
                        Sum('cooking_rating'))
                    feeding_sop = School.objects.filter(visited=True, user=i, date_captured__range=[data['date_from'],
                                                                                                    data[
                                                                                                        'date_to']]).aggregate(
                        Sum('feeding_rating'))
                    education_sop = School.objects.filter(visited=True, user=i, date_captured__range=[data['date_from'],
                                                                                                      data[
                                                                                                          'date_to']]).aggregate(
                        Sum('education_rating'))
                    cooking_sop_num = 0
                    feeding_sop_num = 0
                    education_sop_num = 0
                    if cooking_sop[cooking_sop.keys()[0]]:
                        cooking_sop_num = cooking_sop[cooking_sop.keys()[0]]

                    if feeding_sop[feeding_sop.keys()[0]]:
                        feeding_sop_num = feeding_sop[feeding_sop.keys()[0]]

                    if education_sop[education_sop.keys()[0]]:
                        education_sop_num = education_sop[education_sop.keys()[0]]

                    if visited > 0:
                        education_sop_num = education_sop_num / visited
                        cooking_sop_num = cooking_sop_num / visited
                        feeding_sop_num = feeding_sop_num / visited

                    manager = {
                        'name': i.user.username,
                        'state': i.state,
                        'created': created,
                        'visited': visited,
                        'cooking_sop': cooking_sop_num,
                        'feeding_sop': feeding_sop_num,
                        'education_sop': education_sop_num
                    }
                    all_managers_arr.append(manager)

                return JsonResponse(all_managers_arr, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def managers_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'manager_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Marketing Executive')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(
                    ugettext("Marketing Executive Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                header2 = '&C&G'
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'User', header)
                worksheet.write('B2', 'Schools Created', header)
                worksheet.write('C2', 'Schools Visited', header)
                worksheet.write('D2', 'Cooking SOP', header)
                worksheet.write('E2', 'Feeding SOP', header)
                worksheet.write('F2', 'Education SOP', header)
                worksheet.merge_range('A1:F1', title_text, title)
                row = 2
                col = 0
                name_width = 20

                worksheet.set_column('B:B', 15)
                worksheet.set_column('C:C', 15)
                worksheet.set_column('D:D', 15)
                worksheet.set_column('E:E', 15)
                worksheet.set_column('F:F', 15)

                for i in report:
                    worksheet.write_string(row, col, i['name'])
                    worksheet.write_number(row, col + 1, i['created'])
                    worksheet.write_number(row, col + 2, i['visited'])
                    worksheet.write_number(row, col + 3, i['cooking_sop'])
                    worksheet.write_number(row, col + 4, i['feeding_sop'])
                    worksheet.write_number(row, col + 5, i['education_sop'])
                    row += 1
                    if len(i['name']) > name_width:
                        name_width = len(i['name'])

                worksheet.set_column('A:A', name_width)
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'manager_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def feedback_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'feedback_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Feedback Form')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(ugettext("Feedback Form Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                header2 = '&C&G'
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'No. of School Sampled', header)
                worksheet.write('B2', 'Total School Population', header)
                worksheet.write('C2', 'No. of Pupil Sampled', header)
                worksheet.write('D2', 'No. of Cartons used', header)
                worksheet.merge_range('A1:D1', title_text, title)
                row = 2
                col = 0

                worksheet.set_column('B:B', 30)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 30)
                worksheet.set_column('A:A', 30)

                for i in report:
                    worksheet.write_number(row, col, i['sampled_school'])
                    worksheet.write_number(row, col + 1, i['total_population'])
                    worksheet.write_number(row, col + 2, i['sampled_population'])
                    worksheet.write_number(row, col + 3, i['cartons_used'])
                    row += 1

                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'feedback_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def supervisor_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'supervisor_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Supervisor Report')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(ugettext("Supervisor Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                header2 = '&C&G'
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'Supervisor', header)
                worksheet.write('B2', 'No Of Marketing Executive', header)
                worksheet.write('C2', 'No Of Schools Created', header)
                worksheet.write('D2', 'Average Cooking SOP', header)
                worksheet.write('E2', 'Average Feeding SOP', header)
                worksheet.write('F2', 'Average Education SOP', header)
                worksheet.merge_range('A1:F1', title_text, title)
                row = 2
                col = 0
                name_width = 25

                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 20)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 20)

                for i in report:
                    worksheet.write_string(row, col, i['name'])
                    worksheet.write_number(row, col + 1, i['marketers'])
                    worksheet.write_number(row, col + 2, i['created'])
                    worksheet.write_number(row, col + 3, i['cooking_sop'])
                    worksheet.write_number(row, col + 4, i['feeding_sop'])
                    worksheet.write_number(row, col + 5, i['education_sop'])
                    row += 1
                    if len(i['name']) > name_width:
                        name_width = len(i['name'])

                worksheet.set_column('A:A', name_width)
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'supervisor_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def schools_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook('sampled_schools_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Sampled Schools')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                cell_true = workbook.add_format({'bg_color': '#02B728', 'font_color': '#FFFFFF'})
                cell_false = workbook.add_format({'bg_color': '#FF1F08', 'font_color': '#FFFFFF'})
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                title_text = u"{0}".format(
                    ugettext("Sampled Schools Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                header2 = '&C&G'
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'UUID', header)
                worksheet.write('B2', 'Name', header)
                worksheet.write('C2', 'Address', header)
                worksheet.write('D2', 'State', header)
                worksheet.write('E2', 'LGA', header)
                worksheet.write('F2', 'Coordinates', header)
                worksheet.write('G2', 'Level', header)
                worksheet.write('H2', 'Target Level', header)
                worksheet.write('I2', 'Total Population', header)
                worksheet.write('J2', 'Target Population', header)
                worksheet.write('K2', 'Contact Name', header)
                worksheet.write('L2', 'Contact PN', header)
                worksheet.write('M2', 'School PN', header)
                worksheet.write('N2', 'Approved', header)
                worksheet.write('O2', 'Marketing Executive', header)
                worksheet.write('P2', 'Date', header)
                worksheet.write('Q2', 'Landmark', header)
                worksheet.merge_range('A1:Q1', title_text, title)
                row = 2
                col = 0
                name_width = 25
                ex_name = 25
                ad_width = 30
                contact_width = 30

                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)

                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)

                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)
                worksheet.set_column('N:N', 25)

                worksheet.set_column('O:O', 30)
                worksheet.set_column('P:P', 20)

                for i in report:
                    worksheet.write_string(row, col, i['uuid'])
                    worksheet.write_string(row, col + 1, i['name'])
                    worksheet.write_string(row, col + 2, i['address'])
                    worksheet.write_string(row, col + 3, i['state'])
                    worksheet.write_string(row, col + 4, i['lga'])
                    worksheet.write_string(row, col + 5, i['coordinates'])

                    worksheet.write_string(row, col + 6, i['level'])
                    worksheet.write_string(row, col + 7, i['target_level'])
                    worksheet.write_number(row, col + 8, i['population'])
                    worksheet.write_number(row, col + 9, i['target_population'])
                    worksheet.write_string(row, col + 10, i['contact_name'])

                    worksheet.write_string(row, col + 11, i['contact_phone'])
                    worksheet.write_string(row, col + 12, i['school_phone'])
                    if i['approved']:
                        worksheet.write_string(row, col + 13, 'YES', cell_true)
                    else:
                        worksheet.write_string(row, col + 13, 'NO', cell_false)

                    worksheet.write_string(row, col + 14, i['user'])
                    datetime.strptime('2013-01-23', '%Y-%m-%d')
                    if i['date_captured'] is not None:
                        worksheet.write_datetime(row, col + 15, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                                 date_format)
                    else:
                        worksheet.write_string(row, col + 15, ' ')

                    if i['landmark'] is not None:
                        worksheet.write_string(row, col + 16, i['landmark'])
                    else:
                        worksheet.write_string(row, col + 16, ' ')
                    row += 1
                    if len(i['name']) > name_width:
                        name_width = len(i['name'])

                    if len(i['address']) > ad_width:
                        ad_width = len(i['address'])

                    if len(i['user']) > ex_name:
                        ex_name = len(i['user'])

                    if len(i['contact_name']) > contact_width:
                        contact_width = len(i['contact_name'])

                worksheet.set_column('B:B', name_width)
                worksheet.set_column('O:O', ex_name)
                worksheet.set_column('K:K', contact_width)
                worksheet.set_column('C:C', ad_width)
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'sampled_schools_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def supervisor_reports(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ReportFilters(data=data)
        all_managers_arr = []

        if serializer.is_valid():
            if data['state'] is not None:
                if data['state'] == 'All':
                    all_supervisors = UserProfile.objects.filter(role='Supervisor',
                                                                 supervisor_module__name__exact='School Sampling')
                else:
                    all_supervisors = UserProfile.objects.filter(role='Supervisor', state=data['state'],
                                                                 supervisor_module__name__exact='School Sampling')

                for i in all_supervisors:
                    marketers = UserProfile.objects.filter(user_module='School Sampling', role='Marketing Executive',
                                                           supervisor=i).count()
                    created = School.objects.filter(date_captured__range=[data['date_from'], data['date_to']],
                                                    user__user_module='School Sampling', user__supervisor=i).count()
                    visited = School.objects.filter(user__supervisor=i, visited=True,
                                                    date_captured__range=[data['date_from'], data['date_to']]).count()
                    cooking_sop = School.objects.filter(visited=True, user__supervisor=i,
                                                        user__user_module='School Sampling',
                                                        date_captured__range=[data['date_from'],
                                                                              data['date_to']]).aggregate(
                        Sum('cooking_rating'))
                    feeding_sop = School.objects.filter(visited=True, user__supervisor=i,
                                                        user__user_module='School Sampling',
                                                        date_captured__range=[data['date_from'],
                                                                              data['date_to']]).aggregate(
                        Sum('feeding_rating'))
                    education_sop = School.objects.filter(visited=True, user__supervisor=i,
                                                          user__user_module='School Sampling',
                                                          date_captured__range=[data['date_from'],
                                                                                data['date_to']]).aggregate(
                        Sum('education_rating'))
                    cooking_sop_num = 0
                    feeding_sop_num = 0
                    education_sop_num = 0
                    if cooking_sop[cooking_sop.keys()[0]]:
                        cooking_sop_num = cooking_sop[cooking_sop.keys()[0]]

                    if feeding_sop[feeding_sop.keys()[0]]:
                        feeding_sop_num = feeding_sop[feeding_sop.keys()[0]]

                    if education_sop[education_sop.keys()[0]]:
                        education_sop_num = education_sop[education_sop.keys()[0]]

                    if visited > 0:
                        education_sop_num = education_sop_num / visited
                        cooking_sop_num = cooking_sop_num / visited
                        feeding_sop_num = feeding_sop_num / visited

                    manager = {
                        'marketers': marketers,
                        'name': i.user.username,
                        'state': i.state,
                        'created': created,
                        'visited': visited,
                        'cooking_sop': cooking_sop_num,
                        'feeding_sop': feeding_sop_num,
                        'education_sop': education_sop_num
                    }
                    all_managers_arr.append(manager)

                return JsonResponse(all_managers_arr, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def form_reports(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ReportFilters(data=data)
        if serializer.is_valid():
            if data['state'] is not None:
                if data['state'] == 'All':
                    sampled_school = School.objects.filter(
                        date_captured__range=[data['date_from'], data['date_to']]).count()
                    visited = School.objects.filter(visited=True,
                                                    date_captured__range=[data['date_from'], data['date_to']]).count()
                    sampled_population = School.objects.filter(
                        date_captured__range=[data['date_from'], data['date_to']]).aggregate(Sum('sampled_population'))
                    total_population = School.objects.filter(
                        date_captured__range=[data['date_from'], data['date_to']]).aggregate(Sum('population'))
                    cartons_used = School.objects.filter(
                        date_captured__range=[data['date_from'], data['date_to']]).aggregate(Sum('cartons'))
                else:
                    sampled_school = School.objects.filter(state=data['state'],
                                                           date_captured__range=[data['date_from'],
                                                                                 data['date_to']]).count()
                    sampled_population = School.objects.filter(state=data['state'],
                                                               date_captured__range=[data['date_from'],
                                                                                     data['date_to']]).aggregate(
                        Sum('sampled_population'))
                    total_population = School.objects.filter(state=data['state'],
                                                             date_captured__range=[data['date_from'],
                                                                                   data['date_to']]).aggregate(
                        Sum('population'))
                    cartons_used = School.objects.filter(state=data['state'],
                                                         date_captured__range=[data['date_from'],
                                                                               data['date_to']]).aggregate(
                        Sum('cartons'))
                    visited = School.objects.filter(visited=True,
                                                    date_captured__range=[data['date_from'], data['date_to']],
                                                    state=data['state']).count()

                if sampled_population[sampled_population.keys()[0]]:
                    sampled_population = sampled_population[sampled_population.keys()[0]]
                else:
                    sampled_population = 0

                if total_population[total_population.keys()[0]]:
                    total_population = total_population[total_population.keys()[0]]
                else:
                    total_population = 0

                if cartons_used[cartons_used.keys()[0]]:
                    cartons_used = cartons_used[cartons_used.keys()[0]]
                else:
                    cartons_used = 0

                res = {
                    'sampled_school': sampled_school,
                    'sampled_population': sampled_population,
                    'total_population': total_population,
                    'cartons_used': cartons_used,
                    'visited': visited
                }
                return JsonResponse(res, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def last_date(request):
    if request.method == 'GET':
        first_date = School.objects.order_by('date_captured').first()
        date = {
            'date': first_date.date_captured
        }
        return JsonResponse(date, status=201, safe=False)


@csrf_exempt
def hypo_last_date(request):
    if request.method == 'GET':
        first_date = Hypo.objects.order_by('date_captured').first()
        date = {
            'date': first_date.date_captured
        }
        return JsonResponse(date, status=201, safe=False)


@csrf_exempt
def hypo_numbers(request):
    if request.method == 'GET':
        num_array = []
        all_data = Hypo.objects.all()
        for i in all_data:
            if i.phone_number:
                num_array.append(i.phone_number)

        return JsonResponse(num_array, status=201, safe=False)


@csrf_exempt
def hypo_summary(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ReportFilters(data=data)
        if serializer.is_valid():
            if data['state'] is not None:
                if data['state'] == 'All':
                    household_sampled = Hypo.objects.filter(date_captured__range=[data['date_from'], data['date_to']],
                                                            duplicate=False).count()
                    sampled_before = Hypo.objects.filter(date_captured__range=[data['date_from'], data['date_to']],
                                                         duplicate=False, sampled='Yes').count()
                    hypo_seen = Hypo.objects.filter(date_captured__range=[data['date_from'], data['date_to']],
                                                    duplicate=False, hypo_seen='Yes').count()
                    persons_sampled = Hypo.objects.filter(
                        date_captured__range=[data['date_from'], data['date_to']]).count()
                else:
                    household_sampled = Hypo.objects.filter(state=data['state'],
                                                            date_captured__range=[data['date_from'], data['date_to']],
                                                            duplicate=False).count()
                    sampled_before = Hypo.objects.filter(state=data['state'],
                                                         date_captured__range=[data['date_from'], data['date_to']],
                                                         duplicate=False, sampled='Yes').count()
                    hypo_seen = Hypo.objects.filter(state=data['state'],
                                                    date_captured__range=[data['date_from'], data['date_to']],
                                                    duplicate=False, hypo_seen='Yes').count()
                    persons_sampled = Hypo.objects.filter(state=data['state'], date_captured__range=[data['date_from'],
                                                                                                     data[
                                                                                                         'date_to']]).count()

                res = {
                    'sampled_household': household_sampled,
                    'sampled_before': sampled_before,
                    'hypo_seen': hypo_seen,
                    'person_sampled': persons_sampled,
                    'state': data['state']
                }
                return JsonResponse(res, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def hypo_lga_report(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ReportFilters(data=data)
        if serializer.is_valid():
            _data = []
            lga = json.loads(data['lga'])
            for i in lga:
                household_sampled = Hypo.objects.filter(date_captured__range=[data['date_from'], data['date_to']],
                                                        duplicate=False, lga=i['name']).count()
                sampled_before = Hypo.objects.filter(date_captured__range=[data['date_from'], data['date_to']],
                                                     duplicate=False, sampled='Yes', lga=i['name']).count()
                hypo_seen = Hypo.objects.filter(date_captured__range=[data['date_from'], data['date_to']],
                                                duplicate=False, hypo_seen='Yes', lga=i['name']).count()
                persons_sampled = Hypo.objects.filter(date_captured__range=[data['date_from'], data['date_to']],
                                                      lga=i['name']).count()

                res = {
                    'sampled_household': household_sampled,
                    'sampled_before': sampled_before,
                    'hypo_seen': hypo_seen,
                    'person_sampled': persons_sampled,
                    'lga': i['name'],
                    'state': data['state']
                }
                _data.append(res)

            return JsonResponse(_data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def summary_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'hypo_summary_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Hypo Summary Report')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(ugettext(
                    report[0]['state'] + " State Hypo Summary Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                header2 = '&C&G'
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'No. of Household Sampled', header)
                worksheet.write('B2', 'No. of Household Sampled Before', header)
                worksheet.write('C2', 'No. of Household With Hypo', header)
                worksheet.write('D2', 'No. of Persons Sampled', header)
                worksheet.merge_range('A1:D1', title_text, title)
                row = 2
                col = 0

                worksheet.set_column('B:B', 30)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 30)
                worksheet.set_column('A:A', 30)

                for i in report:
                    worksheet.write_number(row, col, i['sampled_household'])
                    worksheet.write_number(row, col + 1, i['sampled_before'])
                    worksheet.write_number(row, col + 2, i['hypo_seen'])
                    worksheet.write_number(row, col + 3, i['person_sampled'])
                    row += 1

                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'hypo_summary_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def hypo_lga_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'lga_data_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Hypo LGA Data Report')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(ugettext(
                    report[0]['state'] + " State LGAs Hypo Data Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                header2 = '&C&G'
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'Local Government Area (LGA)', header)
                worksheet.write('B2', 'No. of Household Sampled', header)
                worksheet.write('C2', 'No. of Persons Sampled', header)
                worksheet.write('D2', 'No. of Household With Hypo', header)
                worksheet.write('E2', 'No. of Household Sample Before', header)
                worksheet.merge_range('A1:E1', title_text, title)
                row = 2
                col = 0

                worksheet.set_column('B:B', 30)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 30)
                worksheet.set_column('A:A', 30)
                worksheet.set_column('E:E', 30)

                for i in report:
                    worksheet.write_string(row, col, i['lga'])
                    worksheet.write_number(row, col + 1, i['sampled_household'])
                    worksheet.write_number(row, col + 2, i['person_sampled'])
                    worksheet.write_number(row, col + 3, i['hypo_seen'])
                    worksheet.write_number(row, col + 4, i['sampled_before'])
                    row += 1

                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'lga_data_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def hypo_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'hypo_data_' + str(today) + '.xlsx')
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                worksheet = workbook.add_worksheet('Hypo Data')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                wrap = workbook.add_format({'text_wrap': True})
                title_text = u"{0}".format(ugettext("Hypo Sampling Data " + str(today)))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'UUID', header)
                worksheet.write('B2', 'Category', header)
                worksheet.write('C2', 'Type', header)
                worksheet.write('D2', 'Name', header)
                worksheet.write('E2', 'Phone Number', header)
                worksheet.write('F2', 'Address', header)
                worksheet.write('G2', 'LGA', header)
                worksheet.write('H2', 'State', header)
                worksheet.write('I2', 'Coordinates', header)
                worksheet.write('J2', 'Landmark', header)
                worksheet.write('K2', 'Sampled Before', header)
                worksheet.write('L2', 'Hypo Seen', header)
                worksheet.write('M2', 'Demo Given', header)
                worksheet.write('N2', 'Remark', header)
                worksheet.write('O2', 'Marketing Executive', header)
                worksheet.write('P2', 'Date', header)
                worksheet.merge_range('A1:P1', title_text, title)
                row = 2
                col = 0
                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)

                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)

                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)
                worksheet.set_column('N:N', 25)

                worksheet.set_column('O:O', 30)
                worksheet.set_column('P:P', 35)

                for i in report:
                    worksheet.write_string(row, col, i['uuid'])
                    worksheet.write_string(row, col + 1, i['category'])
                    worksheet.write_string(row, col + 2, i['hypo_type'])
                    worksheet.write_string(row, col + 3, i['name'])
                    worksheet.write_string(row, col + 4, i['phone_number'])
                    worksheet.write_string(row, col + 5, i['address'])
                    worksheet.write_string(row, col + 6, i['lga'])
                    worksheet.write_string(row, col + 7, i['state'])
                    worksheet.write_string(row, col + 8, i['coordinates'])
                    if i['landmark'] is not None:
                        worksheet.write_string(row, col + 9, i['landmark'])
                    else:
                        worksheet.write_string(row, col + 9, '  ')
                    worksheet.write_string(row, col + 10, i['sampled'])
                    worksheet.write_string(row, col + 11, i['hypo_seen'])
                    worksheet.write_string(row, col + 12, i['demo_given'])
                    if i['remark'] is not None:
                        worksheet.write_string(row, col + 13, i['remark'])
                    else:
                        worksheet.write_string(row, col + 13, '  ')

                    worksheet.write_string(row, col + 14, i['user'])
                    worksheet.write_datetime(row, col + 15, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                             date_format)
                    if Hypo.objects.filter(duplicate_uuid=i['app_uuid']).exists():
                        all_persons = Hypo.objects.filter(duplicate_uuid=i['app_uuid'])
                        row += 1
                        counter = 0
                        for k in all_persons:
                            worksheet.write_string(row, col, i['uuid'])
                            worksheet.write_string(row, col + 1, i['category'])
                            worksheet.write_string(row, col + 2, i['hypo_type'])
                            worksheet.write_string(row, col + 3, k.name)
                            worksheet.write_string(row, col + 4, k.phone_number)
                            worksheet.write_string(row, col + 5, i['address'])
                            worksheet.write_string(row, col + 6, i['lga'])
                            worksheet.write_string(row, col + 7, i['state'])
                            worksheet.write_string(row, col + 8, i['coordinates'])
                            if i['landmark'] is not None:
                                worksheet.write_string(row, col + 9, i['landmark'])
                            else:
                                worksheet.write_string(row, col + 9, '  ')
                            worksheet.write_string(row, col + 10, i['sampled'])
                            worksheet.write_string(row, col + 11, i['hypo_seen'])
                            worksheet.write_string(row, col + 12, i['demo_given'])
                            if i['remark'] is not None:
                                worksheet.write_string(row, col + 13, i['remark'])
                            else:
                                worksheet.write_string(row, col + 13, '  ')

                            worksheet.write_string(row, col + 14, i['user'])
                            worksheet.write_datetime(row, col + 15, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                                     date_format)
                            if counter != len(all_persons) - 1:
                                counter += 1
                                row += 1

                    row += 1
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'hypo_data_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


class HotelData(generics.ListCreateAPIView):
    serializer_class = serializers.HotelSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Hotel.objects.all()


class NewHotel(generics.CreateAPIView):
    serializer_class = serializers.HotelSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Hotel.objects.all()


class RestaurantData(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Restaurant.objects.all()


class NewRestaurant(generics.CreateAPIView):
    serializer_class = serializers.RestaurantSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Restaurant.objects.all()


class BarData(generics.ListAPIView):
    serializer_class = serializers.BarSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Bar.objects.all()


class NewBar(generics.CreateAPIView):
    serializer_class = serializers.BarSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Bar.objects.all()


class NewCafe(generics.CreateAPIView):
    serializer_class = serializers.CafeSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Cafe.objects.all()


class CafeData(generics.ListAPIView):
    serializer_class = serializers.CafeSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Cafe.objects.all()


class HotelUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = serializers.HotelUpdateSerializer
    queryset = Hotel.objects.all()
    lookup_field = 'app_uid'


class RestaurantUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = serializers.RestaurantUpdateSerializer
    queryset = Restaurant.objects.all()
    lookup_field = 'app_uid'


class BarUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = serializers.BarUpdateSerializer
    queryset = Bar.objects.all()
    lookup_field = 'app_uid'


class CafeUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = serializers.CafeUpdateSerializer
    queryset = Cafe.objects.all()
    lookup_field = 'app_uid'


@csrf_exempt
def hotel_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'hotel_data_' + str(today) + '.xlsx')
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                time_format = workbook.add_format({'num_format': 'hh:mm:ss AM/PM'})
                worksheet = workbook.add_worksheet('Hotel Data')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                wrap = workbook.add_format({'text_wrap': True})
                title_text = u"{0}".format(ugettext("Hotels " + str(today)))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'ID', header)
                worksheet.write('B2', 'Name', header)
                worksheet.write('C2', 'Address', header)
                worksheet.write('D2', 'LGA', header)
                worksheet.write('E2', 'State', header)
                worksheet.write('F2', 'Coordinates', header)
                worksheet.write('G2', 'Phone Number', header)
                worksheet.write('H2', 'Email', header)
                worksheet.write('I2', 'Contact Name', header)
                worksheet.write('J2', 'Contact Phone Number', header)
                worksheet.write('K2', 'Designation', header)
                worksheet.write('L2', 'Rooms', header)
                worksheet.write('M2', 'Restaurants/Cafe', header)
                worksheet.write('N2', 'Amenities', header)
                worksheet.write('O2', 'Rating', header)
                worksheet.write('P2', 'Remark', header)
                worksheet.write('Q2', 'Marketing Executive', header)
                worksheet.write('R2', 'Date', header)
                worksheet.write('S2', 'Time', header)
                worksheet.write('T2', 'Branch', header)
                worksheet.merge_range('A1:T1', title_text, title)
                row = 2
                col = 0
                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)

                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)

                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)
                worksheet.set_column('N:N', 25)

                worksheet.set_column('O:O', 30)
                worksheet.set_column('P:P', 35)
                worksheet.set_column('Q:Q', 35)
                worksheet.set_column('R:R', 35)
                worksheet.set_column('S:S', 35)

                for i in report:
                    worksheet.write(row, col, i['id'])
                    worksheet.write_string(row, col + 1, i['name'])
                    worksheet.write_string(row, col + 2, i['address'])
                    if i['lga'] is not None:
                        worksheet.write_string(row, col + 3, i['lga'])
                    else:
                        worksheet.write_string(row, col + 3, ' ')
                    if i['state'] is not None:
                        worksheet.write_string(row, col + 4, i['state'])
                    else:
                        worksheet.write_string(row, col + 4, ' ')
                    worksheet.write_string(row, col + 5, i['coordinates'])
                    worksheet.write_string(row, col + 6, i['phone_number'])
                    worksheet.write_string(row, col + 7, i['email'])
                    worksheet.write_string(row, col + 8, i['contact_name'])
                    worksheet.write_string(row, col + 9, i['contact_phone'])
                    worksheet.write_string(row, col + 10, i['designation'])
                    worksheet.write_number(row, col + 11, i['no_of_rooms'])
                    worksheet.write_number(row, col + 12, i['no_of_restaurants'])
                    worksheet.write_string(row, col + 13, i['amenities'])
                    worksheet.write(row, col + 14, i['rating'])
                    if i['remark'] is not None:
                        worksheet.write_string(row, col + 15, i['remark'])
                    else:
                        worksheet.write_string(row, col + 15, '  ')
                    worksheet.write_string(row, col + 16, i['user'])
                    worksheet.write_datetime(row, col + 17, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                             date_format)
                    if i['captured_time'] is not None:
                        worksheet.write_datetime(row, col + 18, datetime.strptime(i['captured_time'], '%H:%M:%S'),
                                                 time_format)
                    else:
                        worksheet.write(row, col + 18, ' ')

                    if i['branch'] is not None:
                        worksheet.write_string(row, col + 19, i['branch'])
                    else:
                        worksheet.write_string(row, col + 19, '  ')

                    row += 1
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'hotel_data_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def restaurant_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'restaurant_data_' + str(today) + '.xlsx')
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                time_format = workbook.add_format({'num_format': 'hh:mm:ss AM/PM'})
                worksheet = workbook.add_worksheet('Restaurant Data')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(ugettext("Restaurants/Cafeteria " + str(today)))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'ID', header)
                worksheet.write('B2', 'Name', header)
                worksheet.write('C2', 'Type', header)
                worksheet.write('D2', 'Address', header)
                worksheet.write('E2', 'LGA', header)
                worksheet.write('F2', 'State', header)
                worksheet.write('G2', 'Coordinates', header)
                worksheet.write('H2', 'Phone Number', header)
                worksheet.write('I2', 'Email', header)
                worksheet.write('J2', 'Contact Name', header)
                worksheet.write('K2', 'Contact Phone Number', header)
                worksheet.write('L2', 'Designation', header)
                worksheet.write('M2', 'No. of Tables', header)
                worksheet.write('N2', 'No. of Waiting Staff', header)
                worksheet.write('O2', 'Amenities', header)
                worksheet.write('P2', 'Cuisines', header)
                worksheet.write('Q2', 'Rating', header)
                worksheet.write('R2', 'Remark', header)
                worksheet.write('S2', 'Marketing Executive', header)
                worksheet.write('T2', 'Date', header)
                worksheet.write('U2', 'Time', header)
                worksheet.write('V2', 'Branch', header)
                worksheet.merge_range('A1:V1', title_text, title)
                row = 2
                col = 0
                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)

                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)

                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)
                worksheet.set_column('N:N', 25)

                worksheet.set_column('O:O', 30)
                worksheet.set_column('P:P', 35)
                worksheet.set_column('Q:Q', 35)
                worksheet.set_column('R:R', 30)
                worksheet.set_column('S:S', 35)
                worksheet.set_column('T:T', 30)
                worksheet.set_column('U:U', 35)

                for i in report:
                    obj = State.objects.get(name__iexact=i['state'])
                    branch = obj.branch.name

                    worksheet.write(row, col, i['id'])
                    worksheet.write_string(row, col + 1, i['name'])
                    worksheet.write_string(row, col + 2, i['sample_type'])
                    worksheet.write_string(row, col + 3, i['address'])
                    if i['lga'] is not None:
                        worksheet.write_string(row, col + 4, i['lga'])
                    else:
                        worksheet.write_string(row, col + 4, ' ')
                    if i['state'] is not None:
                        worksheet.write_string(row, col + 5, i['state'])
                    else:
                        worksheet.write_string(row, col + 5, ' ')
                    worksheet.write_string(row, col + 6, i['coordinates'])
                    worksheet.write_string(row, col + 7, i['phone_number'])
                    worksheet.write_string(row, col + 8, i['email'])
                    worksheet.write_string(row, col + 9, i['contact_name'])
                    worksheet.write_string(row, col + 10, i['contact_phone'])
                    worksheet.write_string(row, col + 11, i['designation'])
                    worksheet.write_number(row, col + 12, i['no_of_tables'])
                    worksheet.write_number(row, col + 13, i['no_of_waiting_staff'])
                    worksheet.write_string(row, col + 14, i['amenities'])
                    worksheet.write_string(row, col + 15, i['cuisines'])
                    worksheet.write(row, col + 16, i['rating'])
                    if i['remark'] is not None:
                        worksheet.write_string(row, col + 17, i['remark'])
                    else:
                        worksheet.write_string(row, col + 17, '  ')
                    worksheet.write_string(row, col + 18, i['user'])
                    worksheet.write_datetime(row, col + 19, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                             date_format)
                    if i['captured_time'] is not None:
                        worksheet.write_datetime(row, col + 20, datetime.strptime(i['captured_time'], '%H:%M:%S'),
                                                 time_format)
                    else:
                        worksheet.write(row, col + 20, ' ')
                    if i['branch'] is not None:
                        worksheet.write_string(row, col + 21, i['branch'])
                    else:
                        worksheet.write_string(row, col + 21, '  ')

                    row += 1
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'restaurant_data_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def bar_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'bar_data_' + str(today) + '.xlsx')
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                time_format = workbook.add_format({'num_format': 'hh:mm:ss AM/PM'})
                worksheet = workbook.add_worksheet('Bar Pub Night Clubs Data')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                wrap = workbook.add_format({'text_wrap': True})
                title_text = u"{0}".format(ugettext("Bar Pub Night Clubs " + str(today)))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'ID', header)
                worksheet.write('B2', 'Name', header)
                worksheet.write('C2', 'Type', header)
                worksheet.write('D2', 'Address', header)
                worksheet.write('E2', 'LGA', header)
                worksheet.write('F2', 'State', header)
                worksheet.write('G2', 'Coordinates', header)
                worksheet.write('H2', 'Phone Number', header)
                worksheet.write('I2', 'Email', header)
                worksheet.write('J2', 'Contact Name', header)
                worksheet.write('K2', 'Contact Phone Number', header)
                worksheet.write('L2', 'Designation', header)
                worksheet.write('M2', 'No. of Tables', header)
                worksheet.write('N2', 'No. of Waiting Staff', header)
                worksheet.write('O2', 'Amenities', header)
                worksheet.write('P2', 'Food Type', header)
                worksheet.write('Q2', 'Rating', header)
                worksheet.write('R2', 'Remark', header)
                worksheet.write('S2', 'Marketing Executive', header)
                worksheet.write('T2', 'Date', header)
                worksheet.write('U2', 'Time', header)
                worksheet.write('V2', 'Branch', header)
                worksheet.merge_range('A1:V1', title_text, title)
                row = 2
                col = 0
                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)

                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)

                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)
                worksheet.set_column('N:N', 25)

                worksheet.set_column('O:O', 30)
                worksheet.set_column('P:P', 35)
                worksheet.set_column('Q:Q', 35)
                worksheet.set_column('R:R', 30)
                worksheet.set_column('S:S', 35)
                worksheet.set_column('T:T', 30)
                worksheet.set_column('U:U', 35)

                for i in report:
                    worksheet.write(row, col, i['id'])
                    worksheet.write_string(row, col + 1, i['name'])
                    worksheet.write_string(row, col + 2, i['sample_type'])
                    worksheet.write_string(row, col + 3, i['address'])
                    if i['lga'] is not None:
                        worksheet.write_string(row, col + 4, i['lga'])
                    else:
                        worksheet.write_string(row, col + 4, ' ')
                    if i['state'] is not None:
                        worksheet.write_string(row, col + 5, i['state'])
                    else:
                        worksheet.write_string(row, col + 5, ' ')
                    worksheet.write_string(row, col + 6, i['coordinates'])
                    worksheet.write_string(row, col + 7, i['phone_number'])
                    worksheet.write_string(row, col + 8, i['email'])
                    worksheet.write_string(row, col + 9, i['contact_name'])
                    worksheet.write_string(row, col + 10, i['contact_phone'])
                    worksheet.write_string(row, col + 11, i['designation'])
                    worksheet.write_number(row, col + 12, i['no_of_tables'])
                    worksheet.write_number(row, col + 13, i['no_of_waiting_staff'])
                    worksheet.write_string(row, col + 14, i['amenities'])
                    worksheet.write_string(row, col + 15, i['food_type'])
                    worksheet.write(row, col + 16, i['rating'])
                    if i['remark'] is not None:
                        worksheet.write_string(row, col + 17, i['remark'])
                    else:
                        worksheet.write_string(row, col + 17, '  ')
                    worksheet.write_string(row, col + 18, i['user'])
                    worksheet.write_datetime(row, col + 19, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                             date_format)
                    if i['captured_time'] is not None:
                        worksheet.write_datetime(row, col + 20, datetime.strptime(i['captured_time'], '%H:%M:%S'),
                                                 time_format)
                    else:
                        worksheet.write(row, col + 20, ' ')
                    if i['branch'] is not None:
                        worksheet.write_string(row, col + 21, i['branch'])
                    else:
                        worksheet.write_string(row, col + 21, '  ')

                    row += 1
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'bar_data_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def cafe_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'cafe_data_' + str(today) + '.xlsx')
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                time_format = workbook.add_format({'num_format': 'hh:mm:ss AM/PM'})
                worksheet = workbook.add_worksheet('Bakery Confectionery Cafe Data')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                wrap = workbook.add_format({'text_wrap': True})
                title_text = u"{0}".format(ugettext("Bakery Confectionery Cafe " + str(today)))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'ID', header)
                worksheet.write('B2', 'Name', header)
                worksheet.write('C2', 'Type', header)
                worksheet.write('D2', 'Address', header)
                worksheet.write('E2', 'LGA', header)
                worksheet.write('F2', 'State', header)
                worksheet.write('G2', 'Coordinates', header)
                worksheet.write('H2', 'Phone Number', header)
                worksheet.write('I2', 'Email', header)
                worksheet.write('J2', 'Contact Name', header)
                worksheet.write('K2', 'Contact Phone Number', header)
                worksheet.write('L2', 'Designation', header)
                worksheet.write('M2', 'No. of Tables', header)
                worksheet.write('N2', 'No. of Waiting Staff', header)
                worksheet.write('O2', 'Showroom', header)
                worksheet.write('P2', 'Amenities', header)
                worksheet.write('Q2', 'Offering', header)
                worksheet.write('R2', 'Rating', header)
                worksheet.write('S2', 'Remark', header)
                worksheet.write('T2', 'Marketing Executive', header)
                worksheet.write('U2', 'Date', header)
                worksheet.write('V2', 'Time', header)
                worksheet.write('W2', 'Branch', header)

                worksheet.merge_range('A1:W1', title_text, title)
                row = 2
                col = 0
                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)

                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)

                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)
                worksheet.set_column('N:N', 25)

                worksheet.set_column('O:O', 30)
                worksheet.set_column('P:P', 35)
                worksheet.set_column('Q:Q', 35)
                worksheet.set_column('R:R', 30)
                worksheet.set_column('S:S', 35)
                worksheet.set_column('T:T', 35)
                worksheet.set_column('U:U', 35)
                worksheet.set_column('V:V', 35)

                for i in report:
                    worksheet.write(row, col, i['id'])
                    worksheet.write_string(row, col + 1, i['name'])
                    worksheet.write_string(row, col + 2, i['sample_type'])
                    worksheet.write_string(row, col + 3, i['address'])
                    if i['lga'] is not None:
                        worksheet.write_string(row, col + 4, i['lga'])
                    else:
                        worksheet.write_string(row, col + 4, ' ')
                    if i['state'] is not None:
                        worksheet.write_string(row, col + 5, i['state'])
                    else:
                        worksheet.write_string(row, col + 5, ' ')
                    worksheet.write_string(row, col + 6, i['coordinates'])
                    worksheet.write_string(row, col + 7, i['phone_number'])
                    worksheet.write_string(row, col + 8, i['email'])
                    worksheet.write_string(row, col + 9, i['contact_name'])
                    worksheet.write_string(row, col + 10, i['contact_phone'])
                    worksheet.write_string(row, col + 11, i['designation'])
                    worksheet.write_number(row, col + 12, i['no_of_tables'])
                    worksheet.write_number(row, col + 13, i['no_of_waiting_staff'])
                    worksheet.write_string(row, col + 14, i['showroom'])
                    worksheet.write_string(row, col + 15, i['amenities'])
                    worksheet.write_string(row, col + 16, i['offering'])
                    worksheet.write(row, col + 17, i['rating'])
                    if i['remark'] is not None:
                        worksheet.write_string(row, col + 18, i['remark'])
                    else:
                        worksheet.write_string(row, col + 18, '  ')
                    worksheet.write_string(row, col + 19, i['user'])
                    worksheet.write_datetime(row, col + 20, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                             date_format)
                    if i['captured_time'] is not None:
                        worksheet.write_datetime(row, col + 21, datetime.strptime(i['captured_time'], '%H:%M:%S'),
                                                 time_format)
                    else:
                        worksheet.write(row, col + 21, ' ')
                    if i['branch'] is not None:
                        worksheet.write_string(row, col + 22, i['branch'])
                    else:
                        worksheet.write_string(row, col + 22, '  ')

                    row += 1
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'cafe_data_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


class KelloggsRetailAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.KelloggsRetailSerializer
    queryset = KelloggsRetail.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = KelloggsRetail.objects.all()
        sample_type = self.request.GET.get("sample_type")

        if sample_type:
            queryset = queryset.filter(sampling_type=sample_type)

        return queryset


class KelloggsPreSamplingAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.KelloggsPreSamplingSerializer
    queryset = KelloggsPreSampling.objects.all()


class KelloggsPostSamplingAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.KelloggsPostSamplingSerializer
    queryset = KelloggsPostSampling.objects.all()


@csrf_exempt
def k_pre_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'pre_sampling_' + str(today) + '.xlsx')
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                time_format = workbook.add_format({'num_format': 'hh:mm:ss AM/PM'})
                worksheet = workbook.add_worksheet('Pre Sampling ( Household )')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })

                title_text = u"{0}".format(ugettext("Kelloggs Pre Sampling" + str(today)))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'ID', header)
                worksheet.write('B2', 'Name', header)
                worksheet.write('C2', 'Address', header)
                worksheet.write('D2', 'LGA', header)
                worksheet.write('E2', 'Phone Number', header)
                worksheet.write('F2', 'knows Kelloggs', header)
                worksheet.write('G2', 'knows Coco Pops', header)
                worksheet.write('H2', 'Sachet seen', header)
                worksheet.write('I2', 'Consumes Coco Pops', header)
                worksheet.write('J2', 'Consumption Rate', header)
                worksheet.write('K2', 'Consumption Style', header)
                worksheet.write('L2', 'Consumption Time', header)
                worksheet.write('M2', 'As Kids Breakfast', header)
                worksheet.write('N2', 'Preferred Kids Breakfast', header)
                worksheet.write('O2', 'Preferred Adult Breakfast', header)
                worksheet.write('P2', 'Date', header)
                worksheet.write('Q2', 'Branch', header)
                worksheet.write('R2', 'Coordinates', header)
                worksheet.merge_range('A1:R1', title_text, title)
                row = 2
                col = 0
                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)

                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)

                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)
                worksheet.set_column('N:N', 25)

                worksheet.set_column('O:O', 40)
                worksheet.set_column('P:P', 40)

                worksheet.set_column('Q:Q', 40)
                worksheet.set_column('R:R', 40)

                for i in report:
                    worksheet.write(row, col, i['id'])
                    worksheet.write_string(row, col + 1, i['name'])
                    worksheet.write_string(row, col + 2, i['address'])
                    if i['lga'] is not None:
                        worksheet.write_string(row, col + 3, i['lga'])
                    else:
                        worksheet.write_string(row, col + 3, ' ')

                    if i['phone_number'] is not None:
                        worksheet.write_string(row, col + 4, i['phone_number'])
                    else:
                        worksheet.write_string(row, col + 4, 'N/A')

                    worksheet.write_string(row, col + 5, i['knows_kelloggs'])
                    worksheet.write_string(row, col + 6, i['knows_coco_pops'])
                    worksheet.write_string(row, col + 7, i['coco_pops_sachet_seen'])
                    worksheet.write_string(row, col + 8, i['eats_coco_pops'])
                    if i['consumption_rate'] is not None:
                        worksheet.write_string(row, col + 9, i['consumption_rate'])
                    else:
                        worksheet.write_string(row, col + 9, 'N/A')
                    if i['consumption_style'] is not None:
                        worksheet.write_string(row, col + 10, i['consumption_style'])
                    else:
                        worksheet.write_string(row, col + 10, 'N/A')
                    if i['consumption_time'] is not None:
                        worksheet.write_string(row, col + 11, i['consumption_time'])
                    else:
                        worksheet.write_string(row, col + 11, 'N/A')

                    worksheet.write_string(row, col + 12, i['as_kids_breakfast'])
                    if i['preferred_kids_breakfast'] is not None:
                        worksheet.write_string(row, col + 13, i['preferred_kids_breakfast'])
                    else:
                        worksheet.write_string(row, col + 13, 'N/A')

                    if i['preferred_adult_breakfast'] is not None:
                        worksheet.write_string(row, col + 14, i['preferred_adult_breakfast'])
                    else:
                        worksheet.write_string(row, col + 14, 'N/A')

                    if i['date_captured'] is not None:
                        worksheet.write_datetime(row, col + 15, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                                 date_format)
                    else:
                        worksheet.write_string(row, col + 15, 'N/A')

                    if i['branch'] is not None:
                        worksheet.write_string(row, col + 16, i['branch'])
                    else:
                        worksheet.write_string(row, col + 16, 'N/A')
                    if i['coordinates'] is not None:
                        worksheet.write(row, col + 17, i['coordinates'])
                    else:
                        worksheet.write_string(row, col + 17, 'N/A')

                    row += 1
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'pre_sampling_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def k_post_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'post_sampling_' + str(today) + '.xlsx')
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                worksheet = workbook.add_worksheet('Post Sampling ( Household )')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })

                title_text = u"{0}".format(ugettext("Kelloggs Post Sampling " + str(today)))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'ID', header)
                worksheet.write('B2', 'Name', header)
                worksheet.write('C2', 'Address', header)
                worksheet.write('D2', 'LGA', header)
                worksheet.write('E2', 'Phone Number', header)
                worksheet.write('F2', 'knows Kelloggs', header)
                worksheet.write('G2', 'knows Coco Pops', header)
                worksheet.write('H2', 'knows From', header)
                worksheet.write('I2', 'Sachet seen', header)
                worksheet.write('J2', 'Consumes Coco Pops', header)
                worksheet.write('K2', 'Consumption Rate', header)
                worksheet.write('L2', 'Consumption Style', header)
                worksheet.write('M2', 'Consumption Time', header)
                worksheet.write('N2', 'As Kids Breakfast', header)
                worksheet.write('O2', 'Preferred As Kids Breakfast', header)
                worksheet.write('P2', 'Requested By Kids As Breakfast', header)
                worksheet.write('Q2', 'Preferred Kids Breakfast', header)
                worksheet.write('R2', 'Preferred Adult Breakfast', header)
                worksheet.write('S2', 'Date', header)
                worksheet.write('T2', 'Branch', header)
                worksheet.write('U2', 'Coordinates', header)
                worksheet.merge_range('A1:U1', title_text, title)
                row = 2
                col = 0
                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)

                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)

                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)
                worksheet.set_column('N:N', 25)

                worksheet.set_column('O:O', 40)
                worksheet.set_column('P:P', 40)
                worksheet.set_column('Q:Q', 40)
                worksheet.set_column('R:R', 40)
                worksheet.set_column('S:S', 40)
                worksheet.set_column('T:T', 40)
                worksheet.set_column('U:U', 40)

                for i in report:
                    worksheet.write(row, col, i['id'])
                    worksheet.write_string(row, col + 1, i['name'])
                    worksheet.write_string(row, col + 2, i['address'])
                    if i['lga'] is not None:
                        worksheet.write_string(row, col + 3, i['lga'])
                    else:
                        worksheet.write_string(row, col + 3, ' ')

                    if i['phone_number'] is not None:
                        worksheet.write_string(row, col + 4, i['phone_number'])
                    else:
                        worksheet.write_string(row, col + 4, 'N/A')

                    worksheet.write_string(row, col + 5, i['knows_kelloggs'])
                    worksheet.write_string(row, col + 6, i['knows_coco_pops'])
                    if i['known_from'] is not None:
                        worksheet.write_string(row, col + 7, i['known_from'])
                    else:
                        worksheet.write_string(row, col + 7, 'N/A')

                    worksheet.write_string(row, col + 8, i['coco_pops_sachet_seen'])
                    worksheet.write_string(row, col + 9, i['eats_coco_pops'])
                    if i['consumption_rate'] is not None:
                        worksheet.write_string(row, col + 10, i['consumption_rate'])
                    else:
                        worksheet.write_string(row, col + 10, 'N/A')

                    if i['consumption_style'] is not None:
                        worksheet.write_string(row, col + 11, i['consumption_style'])
                    else:
                        worksheet.write_string(row, col + 11, 'N/A')

                    if i['consumption_time'] is not None:
                        worksheet.write_string(row, col + 12, i['consumption_time'])
                    else:
                        worksheet.write_string(row, col + 12, 'N/A')

                    worksheet.write_string(row, col + 13, i['as_kids_breakfast'])
                    worksheet.write_string(row, col + 14, i['preferred_as_kids_breakfast'])
                    worksheet.write_string(row, col + 15, i['kids_requested'])
                    if i['preferred_kids_breakfast'] is not None:
                        worksheet.write_string(row, col + 16, i['preferred_kids_breakfast'])
                    else:
                        worksheet.write_string(row, col + 16, 'N/A')

                    if i['preferred_adult_breakfast'] is not None:
                        worksheet.write_string(row, col + 17, i['preferred_adult_breakfast'])
                    else:
                        worksheet.write_string(row, col + 17, 'N/A')

                    if i['date_captured'] is not None:
                        worksheet.write_datetime(row, col + 18, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                                 date_format)
                    else:
                        worksheet.write_string(row, col + 18, 'N/A')

                    if i['branch'] is not None:
                        worksheet.write_string(row, col + 19, i['branch'])
                    else:
                        worksheet.write_string(row, col + 19, 'N/A')
                    if i['coordinates'] is not None:
                        worksheet.write(row, col + 20, i['coordinates'])
                    else:
                        worksheet.write_string(row, col + 20, 'N/A')
                    row += 1
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'post_sampling_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def k_retail_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'retail_sampling_' + str(today) + '.xlsx')
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                worksheet = workbook.add_worksheet('Retail Sampling')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })

                title_text = u"{0}".format(ugettext("Kelloggs Retail Sampling" + str(today)))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'ID', header)
                worksheet.write('B2', 'Outlet Name', header)
                worksheet.write('C2', 'Address', header)
                worksheet.write('D2', 'LGA', header)
                worksheet.write('E2', 'Phone Number', header)
                worksheet.write('F2', 'Kelloggs Available', header)
                worksheet.write('G2', 'SKU', header)
                worksheet.write('H2', 'knows Kelloggs', header)
                worksheet.write('I2', 'knows Coco Pops', header)
                worksheet.write('J2', 'Consumes Coco Pops at Home', header)
                worksheet.write('K2', 'Sale (Cartons)', header)
                worksheet.write('L2', 'Selling Price (Sachet)', header)
                worksheet.write('M2', 'Date', header)
                worksheet.write('N2', 'Sample Type', header)
                worksheet.write('O2', 'Branch', header)
                worksheet.write('P2', 'Coordinates', header)
                worksheet.merge_range('A1:M1', title_text, title)
                row = 2
                col = 0
                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)

                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)

                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)

                worksheet.set_column('N:N', 30)
                worksheet.set_column('O:O', 20)
                worksheet.set_column('P:P', 20)

                for i in report:
                    worksheet.write(row, col, i['id'])
                    worksheet.write_string(row, col + 1, i['name'])
                    worksheet.write_string(row, col + 2, i['address'])
                    if i['lga'] is not None:
                        worksheet.write_string(row, col + 3, i['lga'])
                    else:
                        worksheet.write_string(row, col + 3, ' ')

                    if i['phone_number'] is not None:
                        worksheet.write_string(row, col + 4, i['phone_number'])
                    else:
                        worksheet.write_string(row, col + 4, 'N/A')

                    worksheet.write_string(row, col + 5, i['kelloggs_available'])
                    if i['sku'] is not None:
                        worksheet.write_string(row, col + 6, i['sku'])
                    else:
                        worksheet.write_string(row, col + 6, 'N/A')

                    worksheet.write_string(row, col + 7, i['knows_kelloggs'])
                    worksheet.write_string(row, col + 8, i['knows_coco_pops'])
                    worksheet.write_string(row, col + 9, i['consumes_at_home'])
                    worksheet.write_number(row, col + 10, i['carton_sales'])
                    worksheet.write_number(row, col + 11, i['sachet_selling_price'])

                    if i['date_captured'] is not None:
                        worksheet.write_datetime(row, col + 12, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                                 date_format)
                    else:
                        worksheet.write_string(row, col + 12, 'N/A')

                    if i['sampling_type'] is not None:
                        worksheet.write_string(row, col + 13, i['sampling_type'])
                    else:
                        worksheet.write_string(row, col + 13, 'N/A')
                    if i['branch'] is not None:
                        worksheet.write_string(row, col + 14, i['branch'])
                    else:
                        worksheet.write_string(row, col + 14, 'N/A')
                    if i['coordinates'] is not None:
                        worksheet.write(row, col + 15, i['coordinates'])
                    else:
                        worksheet.write_string(row, col + 15, 'N/A')
                    row += 1
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'retail_sampling_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


class KelloggsSchoolSamplingAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.KelloggsSamplingSerializer
    queryset = KelloggsSchool.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = KelloggsSchool.objects.all()
        user_id = self.request.GET.get("id")
        supervisor_id = self.request.GET.get('supervisor')

        if supervisor_id:
            queryset = queryset.filter(user__supervisor_id=supervisor_id, visited=False)
        if user_id:
            # print user_id
            queryset = queryset.filter(user__id=user_id, visited=False)
        return queryset


class KelloggsSchoolUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.KelloggsUpdateSchoolSerializer
    queryset = KelloggsSchool.objects.all()
    lookup_field = 'app_uid'


class KVisitedSchoolsAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.KVisitedSerializer

    queryset = KelloggsSchool.objects.filter(visited=True)


@csrf_exempt
def kelloggs_schools_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'kelloggs_schools_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Sampled Schools')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
                title_text = u"{0}".format(
                    ugettext("Sampled Schools Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'Name', header)
                worksheet.write('B2', 'Address', header)
                worksheet.write('C2', 'Branch', header)
                worksheet.write('D2', 'State', header)
                worksheet.write('E2', 'LGA', header)
                worksheet.write('F2', 'Coordinates', header)
                worksheet.write('G2', 'Level', header)
                worksheet.write('H2', 'Target Level', header)
                worksheet.write('I2', 'Total Population', header)
                worksheet.write('J2', 'Target Population', header)
                worksheet.write('K2', 'Contact Name', header)
                worksheet.write('L2', 'Contact PN', header)
                worksheet.write('M2', 'School PN', header)
                worksheet.write('N2', 'Marketing Executive', header)
                worksheet.write('O2', 'Date', header)
                worksheet.merge_range('A1:O1', title_text, title)
                row = 2
                col = 0
                name_width = 25
                ex_name = 25
                ad_width = 30
                contact_width = 30

                worksheet.set_column('A:A', 15)
                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 25)
                worksheet.set_column('G:G', 25)
                worksheet.set_column('H:H', 30)
                worksheet.set_column('I:I', 20)
                worksheet.set_column('J:J', 25)
                worksheet.set_column('K:K', 30)
                worksheet.set_column('L:L', 20)
                worksheet.set_column('M:M', 20)
                worksheet.set_column('N:N', 25)
                worksheet.set_column('O:O', 30)

                for i in report:
                    worksheet.write_string(row, col, i['name'])
                    worksheet.write_string(row, col + 1, i['address'])
                    if i['branch']:
                        worksheet.write_string(row, col + 2, i['branch'])
                    else:
                        worksheet.write_string(row, col + 2, 'N/A')
                    worksheet.write_string(row, col + 3, i['state'])
                    worksheet.write_string(row, col + 4, i['lga'])
                    worksheet.write_string(row, col + 5, i['coordinates'])
                    worksheet.write_string(row, col + 6, i['level'])

                    worksheet.write_string(row, col + 7, i['target_level'])
                    worksheet.write_number(row, col + 8, i['population'])
                    worksheet.write_number(row, col + 9, i['target_population'])
                    worksheet.write_string(row, col + 10, i['contact_name'])

                    worksheet.write_string(row, col + 11, i['contact_phone'])

                    worksheet.write_string(row, col + 12, i['school_phone'])
                    worksheet.write_string(row, col + 13, i['user'])
                    worksheet.write_datetime(row, col + 14, datetime.strptime(i['date_captured'], '%Y-%m-%d'),
                                             date_format)
                    row += 1
                    if len(i['name']) > name_width:
                        name_width = len(i['name'])

                    if len(i['address']) > ad_width:
                        ad_width = len(i['address'])

                    if len(i['user']) > ex_name:
                        ex_name = len(i['user'])

                    if len(i['contact_name']) > contact_width:
                        contact_width = len(i['contact_name'])

                worksheet.set_column('B:B', name_width)
                worksheet.set_column('O:O', ex_name)
                worksheet.set_column('K:K', contact_width)
                worksheet.set_column('C:C', ad_width)
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'kelloggs_schools_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def first_date(request):
    first_obj = None
    if request.method == 'GET':
        if request.GET.get('module') == 'kelloggs':
            first_obj = KelloggsSchool.objects.order_by('date_captured').first()
        if request.GET.get('module') == 'hypo':
            first_obj = Hypo.objects.order_by('date_captured').first()
        date = {
            'date': first_obj.date_captured
        }
        return JsonResponse(date, status=201, safe=False)


@csrf_exempt
def kelloggs_summary(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ReportFilters(data=data)
        if serializer.is_valid():
            if data['branch'] is not None:
                if data['branch'] == 'All':
                    sampled_school = KelloggsSchool.objects.filter(
                        date_captured__range=[data['date_from'], data['date_to']]).count()
                    visited = KelloggsSchool.objects.filter(visited=True,
                                                            date_captured__range=[data['date_from'],
                                                                                  data['date_to']]).count()
                    sampled_population = KelloggsSchool.objects.filter(date_captured__range=[data['date_from'],
                                                                                             data['date_to']],
                                                                       visited=True).aggregate(
                        Sum('sampled_population'))
                    total_population = KelloggsSchool.objects.filter(date_captured__range=[data['date_from'],
                                                                                           data['date_to']]).aggregate(
                        Sum('population'))
                else:
                    sampled_school = KelloggsSchool.objects.filter(branch=data['branch'],
                                                                   date_captured__range=[data['date_from'],
                                                                                         data['date_to']]).count()
                    sampled_population = KelloggsSchool.objects.filter(branch=data['branch'],
                                                                       date_captured__range=[data['date_from'],
                                                                                             data['date_to']],
                                                                       visited=True).aggregate(
                        Sum('sampled_population'))
                    total_population = KelloggsSchool.objects.filter(branch=data['branch'],
                                                                     date_captured__range=[data['date_from'],
                                                                                           data['date_to']]).aggregate(
                        Sum('population'))
                    visited = KelloggsSchool.objects.filter(visited=True,
                                                            date_captured__range=[data['date_from'], data['date_to']],
                                                            state=data['state']).count()

                if sampled_population[sampled_population.keys()[0]]:
                    sampled_population = sampled_population[sampled_population.keys()[0]]
                else:
                    sampled_population = 0

                if total_population[total_population.keys()[0]]:
                    total_population = total_population[total_population.keys()[0]]
                else:
                    total_population = 0

                res = {
                    'sampled_school': sampled_school,
                    'sampled_population': sampled_population,
                    'total_population': total_population,
                    'visited': visited
                }
                return JsonResponse(res, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def k_managers_reports(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ReportFilters(data=data)
        all_managers_arr = []

        if serializer.is_valid():
            if data['branch'] is not None:
                if data['branch'] == 'All':
                    all_managers = UserProfile.objects.filter(role='Marketing Executive', user_module='Kelloggs')
                else:
                    all_managers = UserProfile.objects.filter(role='Marketing Executive', user_module='Kelloggs',
                                                              branch=data['branch'])

                for i in all_managers:
                    created = KelloggsSchool.objects.filter(user=i, date_captured__range=[data['date_from'],
                                                                                          data['date_to']]).count()
                    visited = KelloggsSchool.objects.filter(user=i, visited=True,
                                                            date_captured__range=[data['date_from'],
                                                                                  data['date_to']]).count()
                    avrg_time = KelloggsSchool.objects.filter(user=i, visited=True,
                                                              date_captured__range=[data['date_from'], data['date_to']])
                    total_population = KelloggsSchool.objects.filter(user=i, date_captured__range=[data['date_from'],
                                                                                                   data['date_to']],
                                                                     visited=True).aggregate(Sum('sampled_population'))
                    new_time = 0
                    average_time = 0
                    if total_population[total_population.keys()[0]]:
                        total_population = total_population[total_population.keys()[0]]
                    else:
                        total_population = 0

                    for k in avrg_time:
                        new_time = new_time + k.duration()

                    if visited > 0:
                        average_time = new_time / visited

                    manager = {
                        'name': i.user.username,
                        'state': i.state,
                        'created': created,
                        'visited': visited,
                        'avg_time': average_time,
                        'total_population': total_population
                    }
                    all_managers_arr.append(manager)

                return JsonResponse(all_managers_arr, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def k_supervisor_reports(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ReportFilters(data=data)
        all_managers_arr = []

        if serializer.is_valid():
            if data['branch'] is not None:
                if data['branch'] == 'All':
                    all_supervisors = UserProfile.objects.filter(role='Supervisor',
                                                                 supervisor_module__name__exact='Kelloggs')
                else:
                    all_supervisors = UserProfile.objects.filter(role='Supervisor', branch=data['branch'],
                                                                 supervisor_module__name__exact='Kelloggs')

                for i in all_supervisors:
                    marketers = UserProfile.objects.filter(user_module='Kelloggs', role='Marketing Executive',
                                                           supervisor=i).count()
                    created = KelloggsSchool.objects.filter(date_captured__range=[data['date_from'], data['date_to']],
                                                            user__supervisor=i).count()
                    visited = KelloggsSchool.objects.filter(user__supervisor=i, visited=True,
                                                            date_captured__range=[data['date_from'],
                                                                                  data['date_to']]).count()
                    avrg_time = KelloggsSchool.objects.filter(user__supervisor=i, visited=True,
                                                              date_captured__range=[data['date_from'], data['date_to']])
                    total_population = KelloggsSchool.objects.filter(user__supervisor=i,
                                                                     date_captured__range=[data['date_from'],
                                                                                           data['date_to']],
                                                                     visited=True).aggregate(Sum('sampled_population'))

                    new_time = 0
                    average_time = 0

                    for k in avrg_time:
                        new_time = new_time + k.duration()

                    if total_population[total_population.keys()[0]]:
                        total_population = total_population[total_population.keys()[0]]
                    else:
                        total_population = 0

                    if visited > 0:
                        average_time = new_time / visited

                    manager = {
                        'marketers': marketers,
                        'name': i.user.username,
                        'state': i.state,
                        'created': created,
                        'visited': visited,
                        'avg_time': average_time,
                        'total_population': total_population

                    }
                    all_managers_arr.append(manager)

                return JsonResponse(all_managers_arr, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def k_feedback_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'kelloggs_feedback_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Feedback Form')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(ugettext("Feedback Form Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'No. of School Sampled', header)
                worksheet.write('B2', 'Total School Population', header)
                worksheet.write('C2', 'No. of Pupil Sampled', header)
                worksheet.merge_range('A1:D1', title_text, title)
                row = 2
                col = 0

                worksheet.set_column('B:B', 30)
                worksheet.set_column('C:C', 30)
                worksheet.set_column('A:A', 30)

                for i in report:
                    worksheet.write_number(row, col, i['sampled_school'])
                    worksheet.write_number(row, col + 1, i['total_population'])
                    worksheet.write_number(row, col + 2, i['sampled_population'])
                    row += 1

                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'kelloggs_feedback_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def k_managers_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'kelloggs_manager_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Marketing Executive')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(
                    ugettext("Marketing Executive Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'User', header)
                worksheet.write('B2', 'Schools Created', header)
                worksheet.write('C2', 'Schools Visited', header)
                worksheet.write('D2', 'Total Students Sampled', header)
                worksheet.write('E2', 'Average Time / School', header)
                worksheet.merge_range('A1:E1', title_text, title)
                row = 2
                col = 0
                name_width = 20

                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 25)
                worksheet.set_column('D:D', 25)
                worksheet.set_column('E:E', 25)

                for i in report:
                    worksheet.write_string(row, col, i['name'])
                    worksheet.write_number(row, col + 1, i['created'])
                    worksheet.write_number(row, col + 2, i['visited'])
                    worksheet.write_number(row, col + 3, i['total_population'])
                    worksheet.write_string(row, col + 4, i['avg_time'])

                    row += 1
                    if len(i['name']) > name_width:
                        name_width = len(i['name'])

                worksheet.set_column('A:A', name_width)
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'kelloggs_manager_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def k_supervisor_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'kelloggs_supervisor_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Supervisor Report')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(ugettext("Supervisor Report " + str(datetime.now().strftime('%Y-%m-%d'))))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'Supervisor', header)
                worksheet.write('B2', 'No Of Marketing Executive', header)
                worksheet.write('C2', 'No Of Schools Created', header)
                worksheet.write('D2', 'No Of Schools Visited', header)
                worksheet.write('E2', 'Total Students Sampled', header)
                worksheet.write('F2', 'Average Time / School', header)
                worksheet.merge_range('A1:F1', title_text, title)
                row = 2
                col = 0
                name_width = 25

                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 20)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 20)

                for i in report:
                    worksheet.write_string(row, col, i['name'])
                    worksheet.write_number(row, col + 1, i['marketers'])
                    worksheet.write_number(row, col + 2, i['created'])
                    worksheet.write_number(row, col + 3, i['visited'])
                    worksheet.write_number(row, col + 4, i['total_population'])
                    worksheet.write_string(row, col + 5, i['avg_time'])
                    row += 1
                    if len(i['name']) > name_width:
                        name_width = len(i['name'])

                worksheet.set_column('A:A', name_width)
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'kelloggs_supervisor_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


class CountryAPIView(generics.ListAPIView):
    permission_classes = ()
    serializer_class = serializers.CountrySerializer02
    queryset = Country.objects.all().prefetch_related('branch_set', 'branch_set__state_set',
                                                      'branch_set__state_set__lga_set')


class CountryCreateAPIView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = serializers.CreateCountrySerializer
    queryset = Country.objects.all()


class HotelListView(views.APIView):
    def get(self, request):
        users = Hotel.objects.all()
        serializer = serializers.HotelSerializerLite(users)
        return Response(serializer.data)


class HotelList(generics.ListAPIView):
    serializer_class = serializers.HotelSerializerLite
    permission_classes = ()
    queryset = Hotel.objects.all().prefetch_related('user', 'user__user')


class RestaurantLite(generics.ListAPIView):
    serializer_class = serializers.RestaurantSerializerLite
    permission_classes = ()
    queryset = Restaurant.objects.all().prefetch_related('user', 'user__user')


class BarLite(generics.ListAPIView):
    serializer_class = serializers.BarSerializerLite
    permission_classes = ()
    queryset = Bar.objects.all().prefetch_related('user', 'user__user')


class CafeLite(generics.ListAPIView):
    serializer_class = serializers.CafeSerializerLite
    permission_classes = ()
    queryset = Cafe.objects.all().prefetch_related('user', 'user__user')


@csrf_exempt
def school_numbers(request):
    client_ip, is_routable = get_client_ip(request)
    print (request.META["REMOTE_ADDR"])
    if request.method == 'GET':
        if client_ip is None:
            pass
        else:
            num_array = []
            all_data = School.objects.all()
            for i in all_data:
                if i.school_phone:
                    num_array.append(i.contact_phone)
                    num_array.append(i.school_phone)

            return JsonResponse(num_array, status=201, safe=False)


@csrf_exempt
def maintain(request):
    client_ip, is_routable = get_client_ip(request)
    if request.method == 'GET':
        if client_ip is None:
            pass
        else:
            all_pre = KelloggsPreSampling.objects.all()
            all_post = KelloggsPostSampling.objects.all()
            all_retail = KelloggsRetail.objects.all()
            for obj in all_pre:
                obj.branch = obj.branch.upper()
                obj.save()
            for obj in all_post:
                obj.branch = obj.branch.upper()
                obj.save()
            for obj in all_retail:
                obj.branch = obj.branch.upper()
                obj.save()
            num_array = ['Done']

            return JsonResponse(num_array, status=201, safe=False)


@csrf_exempt
def users_excel(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ExcelSerializer(data=data)
        if serializer.is_valid():
            if data['report'] is not None:
                report = json.loads(data['report'])
                today = datetime.now().strftime('%Y-%m-%d%H:%M:%S')
                workbook = xlsxwriter.Workbook(settings.MEDIA_ROOT + 'engage_users_' + str(today) + '.xlsx')
                worksheet = workbook.add_worksheet('Engage Users')
                title = workbook.add_format({
                    'bold': True,
                    'font_size': 14,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                header = workbook.add_format({
                    'bg_color': '#F7F7F7',
                    'color': 'black',
                    'align': 'center',
                    'valign': 'top',
                    'border': 1
                })
                title_text = u"{0}".format(ugettext("Engage Users " + str(datetime.now().strftime('%Y-%m-%d'))))
                worksheet.set_margins(top=1.3)
                worksheet.write('A2', 'Name', header)
                worksheet.write('B2', 'Username', header)
                worksheet.write('C2', 'Email Address', header)
                worksheet.write('D2', 'Phone Number', header)
                worksheet.write('E2', 'Password', header)
                worksheet.write('F2', 'Role', header)
                worksheet.write('G2', 'IMEI', header)
                worksheet.write('H2', 'Module', header)
                worksheet.write('I2', 'Country', header)
                worksheet.write('J2', 'Branch', header)
                worksheet.write('K2', 'State', header)
                worksheet.merge_range('A1:K1', title_text, title)
                row = 2
                col = 0
                name_width = 25

                worksheet.set_column('B:B', 25)
                worksheet.set_column('C:C', 20)
                worksheet.set_column('D:D', 20)
                worksheet.set_column('E:E', 20)
                worksheet.set_column('F:F', 20)

                for i in report:
                    worksheet.write_string(row, col, i['name'])
                    worksheet.write_string(row, col + 1, i['username'])
                    worksheet.write_string(row, col + 2, i['email'])
                    worksheet.write_string(row, col + 3, i['phone_number'])
                    worksheet.write_string(row, col + 4, i['password'])
                    worksheet.write_string(row, col + 5, i['role'])
                    if i['imei'] is not None:
                        worksheet.write_string(row, col + 6, i['imei'])
                    else:
                        worksheet.write_string(row, col + 6, 'N/A')

                    if i['module'] is not None:
                        worksheet.write_string(row, col + 7, i['module'])
                    elif i['supervisor_module'] is not None:
                        worksheet.write_string(row, col + 7, i['supervisor_module'])
                    else:
                        worksheet.write_string(row, col + 7, 'N/A')

                    if i['country'] is not None:
                        worksheet.write_string(row, col + 8, i['country'])
                    else:
                        worksheet.write_string(row, col + 8, 'N/A')

                    if i['branch'] is not None:
                        worksheet.write_string(row, col + 9, i['branch'])
                    else:
                        worksheet.write_string(row, col + 9, 'N/A')

                    if i['state'] is not None:
                        worksheet.write_string(row, col + 10, i['state'])
                    else:
                        worksheet.write_string(row, col + 10, 'N/A')

                    row += 1
                    if len(i['name']) > name_width:
                        name_width = len(i['name'])

                worksheet.set_column('A:A', name_width)
                workbook.close()
                message = {
                    'url': 'http://54.72.172.83:9000/media/' + 'engage_users_' + str(today) + '.xlsx'
                }
                return JsonResponse(message, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


class SchoolUpdateAPIViewAdmin(generics.RetrieveUpdateAPIView):
    permission_classes = ()
    serializer_class = serializers.SchoolUpdateSerializerAdmin
    queryset = School.objects.all()
    lookup_field = 'pk'

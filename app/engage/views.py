# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
from django.db.models import Q


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserRegistrationSerializer
    queryset = User.objects.all()


class UserLoginAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserLoginSerializer

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
    permission_classes = (permissions.AllowAny, )
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = serializers.SchoolRegistrationSerializer
    queryset = School.objects.all()


class SchoolUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny, )
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = serializers.SchoolUpdateSerializer
    queryset = School.objects.all()
    lookup_field = 'pk'


class SchoolUpdateAPIView2(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.SchoolUpdateSerializer
    queryset = School.objects.all()
    lookup_field = 'pk'


class SchoolAppointmentAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.SchoolAppointment
    queryset = School.objects.all()


class SchoolRatingAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.SchoolRating
    queryset = School.objects.all()


class User(generics.ListAPIView):
    serializer_class = serializers.UsersSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = UserProfile.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     queryset = School.objects.all()
    #     user_id = self.request.GET.get("id")
    #     supervisor_name = self.request.GET.get('supervisor')
    #     if supervisor_name:
    #         queryset = queryset.filter(user__supervisor_id=supervisor_name)
    #     if user_id:
    #         queryset = queryset.filter(user__id=user_id, approved=True, delete=False, visited=False)
    #     return queryset

class SchoolList(generics.ListAPIView):
    serializer_class = serializers.SchoolSerializer
    permission_classes = (permissions.AllowAny,)
    all_school = School.objects.filter(visited=False)
    for i in all_school:
        if i.cooking_video and i.feeding_video is not None:
            i.visited = True
            i.save()

    def get_queryset(self, *args, **kwargs):
        queryset = School.objects.all()
        user_id = self.request.GET.get("id")
        today = datetime.now().strftime("%Y-%m-%d")
        date_1 = datetime.strptime(today, "%Y-%m-%d")
        end_date = date_1 + timedelta(days=7)

        supervisor_name = self.request.GET.get('supervisor')
        if supervisor_name:
            queryset = queryset.filter(user__supervisor_id=supervisor_name)
        if user_id:
            queryset = queryset.filter(Q(visit_date__gte=datetime.now()) & Q(visit_date__lte=end_date), user__id=user_id, approved=True, delete=False, visited=False)
        return queryset


class VisitedSchoolList(generics.ListAPIView):
    # pass
    all_school = School.objects.filter(visited=False)
    for i in all_school:
        if i.cooking_video and i.feeding_video is not None:
            i.visited = True
            i.save()
    serializer_class = serializers.SchoolSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (permissions.AllowAny,)
    queryset = School.objects.filter(visited=True)


class Users(generics.ListAPIView):
    serializer_class = serializers.UsersSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self, *args, **kwargs):
        queryset = UserProfile.objects.all()
        role = self.request.GET.get("role")
        id = self.request.GET.get("id")
        admin = self.request.GET.get("admin")
        if admin:
            queryset = queryset.filter(Q(role='Supervisor') | Q(role='Marketing Executive'))

        if role:
            queryset = queryset.filter(role=role)
        if id:
            queryset = queryset.filter(id=id)
        supervisor = self.request.GET.get('supervisor')
        if supervisor:
            queryset = queryset.filter(supervisor__id=supervisor)
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
                'message' : 'Successful'
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
                'message' : 'Successful'
            }
            return JsonResponse(done, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


# class SchoolRegAPIView(generics.CreateAPIView):
#     permission_classes = (permissions.AllowAny, )
#     serializer_class = serializers.SchoolRegSerializer
#     queryset = School.objects.all()


class HypoCreationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.HypoCreationSerializer
    queryset = Hypo.objects.all()


class HypoData(generics.ListAPIView):
    serializer_class = serializers.HypoSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self, *args, **kwargs):
        queryset = Hypo.objects.all()
        user_id = self.request.GET.get("id")
        if user_id:

            queryset = queryset.filter(user__id=user_id, approved=True, delete=False)
        return queryset


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
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Q
from .models import *
import base64, uuid
from django.core.files.base import ContentFile

User = get_user_model()

main_dpt = datetime.strptime("2018-08-19", "%Y-%m-%d")


class UserModuleSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserModules
        fields = ['id', 'name', 'active']


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    supervisor = serializers.IntegerField(required=False)
    role = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    supervisor_module = serializers.CharField(required=False)
    user_module = serializers.CharField(required=False)

    class Meta(object):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'supervisor', 'phone_number', 'state', 'user_module', 'supervisor_module']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        user_data = {
            'username': validated_data.get('username'),
            'email': validated_data.get('email'),
            'password': validated_data.get('password'),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name'),
            'supervisor': validated_data.get('supervisor'),
            'role': validated_data.get('role'),
            'phone_number': validated_data.get('phone_number'),
            'state': validated_data.get('state'),
            'user_module' : validated_data.get('user_module'),
            'supervisor_module': validated_data.get('supervisor_module')
        }

        UserProfile.objects.create_user(data=user_data)

        return validated_data

    def update(self, instance, validated_data):
        UserProfile.objects


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username']


class UsersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    supervisor_module = UserModuleSerializer(many=True)


    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'phone_number', 'password_string', 'user_module', 'state', 'supervisor_module', 'supervisor', 'visited', 'created']


class UserLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField( required=False, allow_blank=True)
    email = serializers.EmailField( required=False, allow_blank=True)
    password = serializers.CharField(required=True, write_only=True)
    role = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)
    state = serializers.CharField(required=False)
    user_module = serializers.CharField(required=False)
    created = serializers.IntegerField(required=False)
    group = serializers.CharField(required=False)
    visited = serializers.CharField(required=False)
    supervisor_module = UserModuleSerializer(many=True, required=False)

    class Meta(object):
        model = User
        fields = ['email', 'username', 'password',  'role', 'id', 'group', 'state', 'created', 'user_module', 'visited', 'supervisor_module']

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if not email and not username:
            raise serializers.ValidationError("Please enter username or email to login.")

        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).exclude(
            email__isnull=True
        ).exclude(
            email__iexact=''
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            main_user = UserProfile.objects.get(user=user_obj)
            data['email'] = user_obj.email
            data['username'] = user_obj.username
            data['role'] = main_user.role
            data['id'] = main_user.id
            data['state'] = main_user.state
            data['user_module'] = main_user.user_module
            data['supervisor_module'] = main_user.supervisor_module
            data['created']= main_user.created()
            data['visited'] = main_user.visited()

        else:
            raise serializers.ValidationError("User not active.")

        return data


class SchoolSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta(object):
        model = School
        fields = [
                  'id',
                  'name',
                  'address',
                  'state',
                  'lga',
                  'lat',
                  'lng',
                  'final_lat',
                  'final_lng',
                  'contact_name',
                  'contact_phone',
                  'school_phone',
                  'level',
                  'nursery_population',
                  'population',
                  'user',
                  'approved',
                  'landmark',
                  'designation',
                  'date_captured',
                  'delete',
                  'visit_date',
                  'supervisor',
                  'school_image',
                  'cooking_video',
                  'feeding_video',
                  'other_video',
                  'education_video',
                  'reschedule_reason',
                  'visit_start_time',
                  'visit_end_time',
                  'visit_start_date',
                  'visit_end_date',
                  'lunch_box_with_noddles',
                  'lunch_box',
                  'cartons',
                  'sampled_population',
                  'final_population',
                  'approve_filter',
                  'duration',
                  'promoters',
                  'cooking_rating',
                  'feeding_rating',
                  'education_rating',
                  'visited'
                  ]


class SchoolRegistrationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    user_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True, max_length=200)
    school_type = serializers.CharField(required=True, max_length=100)
    address = serializers.CharField(required=True, max_length=200)
    state = serializers.CharField(required=True, max_length=50)
    lga = serializers.CharField(required=True, max_length=100)
    lat = serializers.FloatField(required=False)
    lng = serializers.FloatField(required=False)
    contact_name = serializers.CharField(allow_blank=True, max_length=100, required=False)
    contact_phone = serializers.CharField(allow_blank=True, max_length=20, required=False)
    school_phone = serializers.CharField(allow_blank=True, max_length=20, required=False)
    level = serializers.CharField(allow_blank=True, max_length=100, required=False)
    population = serializers.IntegerField(required=True,)
    nursery_population = serializers.IntegerField(required=True)
    landmark = serializers.CharField(max_length=200, required=False)
    designation = serializers.CharField(max_length=200, required=False)
    date_captured = serializers.CharField(max_length=100, required=False)
    status = serializers.CharField(max_length=100, required=False)
    school_image = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    cooking_video = serializers.FileField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    feeding_video = serializers.FileField(max_length=None, use_url=True, allow_empty_file=True, required=False)

    def validate_user_id(self, value):
        if not value:
            return 0
        try:
            value = int(value)
        except ValueError:
            raise serializers.ValidationError("Not Number")
        return value

    def create(self, validated_data):

        return School.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.cooking_video = validated_data.get('cooking_video', instance.cooking_video)
        instance.feeding_video = validated_data.get('feeding_video', instance.feeding_video)
        instance.feedback = validated_data.get('feedback', instance.feedback)
        return instance


class ObjIdSerializers(serializers.Serializer):
    id = serializers.IntegerField(required=False)

    def validate(self, data):
        obj_id = data.get('id')
        return {
            'id': obj_id,
        }


class SchoolAppointment(serializers.Serializer):
    id = serializers.IntegerField()
    visit_date = serializers.CharField(max_length=100, required=False)
    reschedule_reason = serializers.CharField(max_length=600, required=False)

    def create(self, validated_data):

        return School.objects.book_appointment(validated_data)

    def update(self, instance, validated_data):
        pass


class SchoolRating(serializers.Serializer):
    id = serializers.IntegerField()
    mode = serializers.CharField(max_length=100, required=False)
    rate = serializers.IntegerField(required=False)

    def create(self, validated_data):

        return School.objects.rate_school(validated_data)

    def update(self, instance, validated_data):
        pass


class UsrProfile(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    supervisor = serializers.IntegerField(required=False)
    role = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    password_string = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    supervisor_module = serializers.CharField(required=False)
    user_module = serializers.CharField(required=False)


# class SchoolRegSerializer(serializers.ModelSerializer):
#     user = UsrProfile()
#
#     class Meta(object):
#         model = School
#         fields = [
#                   'id',
#                   'name',
#                   'address',
#                   'school_image',
#                   'user'
#                   ]


class SchoolUpdateSerializer(serializers.ModelSerializer):
    cooking_video = serializers.FileField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    feeding_video = serializers.FileField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    education_video = serializers.FileField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    other_video = serializers.FileField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    final_population = serializers.IntegerField(required=False)
    sampled_population = serializers.IntegerField(required=False)
    cartons = serializers.IntegerField(required=False)
    lunch_box = serializers.IntegerField(required=False)
    lunch_box_with_noddles = serializers.IntegerField(required=False)
    promoters = serializers.IntegerField(required=False)
    visit_start_time = serializers.CharField(max_length=None, required=False)
    visit_end_time = serializers.CharField(max_length=None, required=False)
    visit_start_date = serializers.CharField(max_length=None, required=False)
    visit_end_date = serializers.CharField(max_length=None, required=False)
    final_lat = serializers.FloatField(required=False)
    final_lng = serializers.FloatField(required=False)

    class Meta(object):
        model = School
        fields = [
            'cooking_video',
            'feeding_video',
            'education_video',
            'other_video',
            'final_population',
            'sampled_population',
            'cartons',
            'lunch_box',
            'lunch_box_with_noddles',
            'promoters',
            'visit_start_time',
            'visit_end_time',
            'visit_start_date',
            'visit_end_date',
            'final_lat',
            'final_lng'
        ]


class HypoCreationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    user_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True, max_length=200)
    category = serializers.CharField(required=True, max_length=100)
    address = serializers.CharField(required=True, max_length=200)
    state = serializers.CharField(required=True, max_length=50)
    lga = serializers.CharField(required=True, max_length=100)
    lat = serializers.FloatField(required=False)
    lng = serializers.FloatField(required=False)
    landmark = serializers.CharField(max_length=200, required=False)
    remark = serializers.CharField(max_length=200, required=False)
    date_captured = serializers.CharField(max_length=100, required=False)

    def validate_user_id(self, value):
        if not value:
            return 0
        try:
            value = int(value)
        except ValueError:
            raise serializers.ValidationError("Not Number")
        return value

    def create(self, validated_data):

        return Hypo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class HypoSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta(object):
        model = Hypo
        fields = [
                  'id',
                  'name',
                  'address',
                  'state',
                  'user',
                  'category',
                  'state',
                  'lga',
                  'lat',
                  'lng',
                  'landmark',
                  'remark',
                  'date_captured'
                  ]
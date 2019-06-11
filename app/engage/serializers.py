from django.contrib.auth import get_user_model
from rest_framework import serializers, fields
from django.db.models import Q
from .models import *
import base64, uuid
from django.core.files.base import ContentFile

User = get_user_model()

main_dpt = datetime.strptime("2018-08-19", "%Y-%m-%d")


AMENITIES = (
    ('Restaurant', 'Restaurant'),
    ('Bar', 'Bar'),
    ('Swimming Pool', 'Swimming Pool'),
    ('Gym', 'Gym'),
    ('Spa', 'Spa'),
    ('Casino', 'Casino'),
    ('Salon', 'Salon'),
    ('Boutiques', 'Boutiques'),
    ('Elevator', 'Elevator'),
    ('Wifi', 'Wifi'),
    ('Concierge', 'Concierge'),
    ('Recreation Room', 'Recreation Room'),
    ('Night Club', 'Night Club'),
    ('Banquet', 'Banquet'),
    ('Kids play area', 'Kids play area'),
    ('Dance Floor', 'Dance Floor'),
    ('Recreational Area', 'Recreational Area'),
    ('Pool Side', 'Pool Side')
)

CUISINE = (
    ('Nigerian', 'Nigerian'),
    ('Chinese', 'Chinese'),
    ('Continental', 'Continental'),
    ('Indian', 'Indian'),
    ('Arabic/Lebanese', 'Arabic/Lebanese'),
    ('Mexican', 'Mexican'),
    ('Italian', 'Italian'),
    ('Asian', 'Asian'),
    ('Fast Food', 'Fast Food')
)

TYPE = (
    ('Night Club', 'Night Club'),
    ('Lounge', 'Lounge'),
    ('Beer Parlor', 'Beer Parlor'),
    ('Fine Dine', 'Fine Dine'),
    ('Cafe', 'Cafe'),
    ('Casual', 'Casual'),
    ('Fast Food', 'Fast Food'),
    ('Buka', 'Buka'),
    ('Canteen', 'Canteen'),
    ('Night Club', 'Night Club'),
    ('Lounge', 'Lounge'),
    ('Beer Parlor', 'Beer Parlor'),
    ('Take Away', 'Take Away'),
    ('Eat In', 'Eat In')
)

OFFERINGS = (
    ('Bread', 'Bread'),
    ('Pastries', 'Pastries'),
    ('Cakes', 'Cakes'),
    ('Ice Cream', 'Ice Cream'),
    ('Coffee', 'Coffee'),
    ('Beverages', 'Beverages'),
    ('Finger Food', 'Finger Food')
)


class UserModuleSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserModules
        fields = ['id', 'name', 'active']


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    supervisor = serializers.IntegerField(required=False)
    role = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    branch = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    supervisor_module = serializers.CharField(required=False)
    user_module = serializers.CharField(required=False)

    class Meta(object):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'supervisor', 'phone_number', 'state',
                  'user_module', 'supervisor_module', 'password', 'country', 'branch']

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
            'country': validated_data.get('country'),
            'user_module' : validated_data.get('user_module'),
            'supervisor_module': validated_data.get('supervisor_module'),
            'branch': validated_data.get('branch'),
        }

        UserProfile.objects.create_user(data=user_data)

        return validated_data

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username']


class UsersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    supervisor_module = UserModuleSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['id',
                  'user',
                  'role',
                  'phone_number',
                  'password_string',
                  'user_module',
                  'state',
                  'country',
                  'branch',
                  'supervisor_module',
                  'supervisor',
                  'visited',
                  'created',
                  'username',
                  'imei',
                  'lga',
                  'last_month_planned',
                  'this_month_planned',
                  'last_month_visited',
                  'this_month_visited',
                  'last_month_cooking_sop',
                  'this_month_cooking_sop',
                  'last_month_feeding_sop',
                  'this_month_feeding_sop',
                  'last_month_education_sop',
                  'this_month_education_sop',
                  'pupils_sampled_this_month',
                  'pupils_sampled_last_month',
                  'lunch_box_this_month',
                  'lunch_box_last_month',
                  'with_noddles_this_month',
                  'with_noddles_last_month'
                  ]


class UsersSerializer02(serializers.ModelSerializer):
    user = UserSerializer()
    supervisor_module = UserModuleSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['id',
                  'user',
                  'role',
                  ]


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField( required=False, allow_blank=True)
    email = serializers.EmailField( required=False, allow_blank=True)
    password = serializers.CharField(required=True, write_only=True)
    role = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)
    state = serializers.CharField(required=False)
    branch = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    user_module = serializers.CharField(required=False)
    created = serializers.IntegerField(required=False)
    group = serializers.CharField(required=False)
    visited = serializers.CharField(required=False)
    supervisor_module = UserModuleSerializer(many=True, required=False)

    class Meta(object):
        model = User
        fields = ['email', 'username', 'password',  'role', 'id', 'group', 'state', 'country', 'created',
                  'user_module', 'visited', 'supervisor_module', 'branch']

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
            data['branch'] = main_user.branch
            data['country'] = main_user.country
            data['user_module'] = main_user.user_module
            data['supervisor_module'] = main_user.supervisor_module
            data['created']= main_user.created()
            data['visited'] = main_user.visited()


        else:
            raise serializers.ValidationError("User not active.")

        return data


class MobileLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField( required=False, allow_blank=True)
    email = serializers.EmailField( required=False, allow_blank=True)
    password = serializers.CharField(required=True, write_only=True)
    role = serializers.CharField(required=False)
    imei = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)
    state = serializers.CharField(required=False)
    lga = serializers.JSONField(required=False)
    branch = serializers.CharField(required=False)
    user_module = serializers.CharField(required=False)
    created = serializers.IntegerField(required=False)
    visited = serializers.CharField(required=False)

    class Meta(object):
        model = User
        fields = ['email', 'username', 'password', 'last_name', 'first_name' , 'role', 'id', 'state', 'created',
                  'user_module', 'visited', 'imei', 'branch', 'lga']

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)
        imei = data.get('imei', None)

        if not email and not username:
            raise serializers.ValidationError("Please enter username or email to login.")

        if not imei:
            raise serializers.ValidationError("No IMEI Number")

        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).exclude(
            email__isnull=True
        ).exclude(
            email__iexact=''
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
            mobile_user = UserProfile.objects.get(user=user_obj)
        else:
            raise serializers.ValidationError("This username/email is not valid.")

        check_imei = UserProfile.objects.filter(imei=imei)

        if check_imei.exists() and check_imei.count() == 1:
            with_imei = check_imei.first()
            if imei != with_imei.imei:
                raise serializers.ValidationError("Wrong IMEI for this user")

        if check_imei.exists() and not mobile_user.imei:
            raise serializers.ValidationError("User not assigned to this device")

        if not check_imei.exists() and not mobile_user.imei:
            mobile_user.imei = imei
            mobile_user.save()

        if mobile_user.imei:
            user_imei = mobile_user.imei
            if user_imei != imei:
                raise serializers.ValidationError("Wrong IMEI for this user")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            lga = []
            main_user = UserProfile.objects.get(user=user_obj)
            all_lga = LGA.objects.filter(state__name=main_user.state, state__branch__name=main_user.branch)
            for i in all_lga:
                lga.append(i.name)
            data['email'] = user_obj.email
            data['username'] = user_obj.username
            data['first_name'] = user_obj.first_name
            data['last_name'] = user_obj.last_name
            data['role'] = main_user.role
            data['id'] = main_user.id
            data['state'] = main_user.state
            data['branch'] = main_user.branch
            data['user_module'] = main_user.user_module
            data['created']= main_user.created()
            data['visited'] = main_user.visited()
            data['lga'] = lga

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
                  'school_type',
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
                  'visited',
                  'branch',
                  'uuid',
                  'target_level',
                  'target_population'
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
    target_level = serializers.CharField(allow_blank=True, max_length=100, required=False)
    population = serializers.IntegerField(required=True,)
    target_population = serializers.IntegerField(required=False)
    nursery_population = serializers.IntegerField(required=False, default=0)
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


class SchoolEditSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    name = serializers.CharField(required=False, max_length=200)
    school_type = serializers.CharField(required=False, max_length=100)
    address = serializers.CharField(required=False, max_length=200)
    state = serializers.CharField(required=False, max_length=50)
    lga = serializers.CharField(required=False, max_length=100)
    contact_name = serializers.CharField(allow_blank=True, max_length=100, required=False)
    contact_phone = serializers.CharField(allow_blank=True, max_length=20, required=False)
    school_phone = serializers.CharField(allow_blank=True, max_length=20, required=False)
    level = serializers.CharField(allow_blank=False, max_length=100, required=False)
    population = serializers.IntegerField(required=False)
    nursery_population = serializers.IntegerField(required=False)
    landmark = serializers.CharField(max_length=200, required=False)
    designation = serializers.CharField(max_length=200, required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


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
    reset_imei = serializers.BooleanField(required=False)


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
    visited = serializers.BooleanField(required=False, default=True)
    visit_date = serializers.DateField(required=False, allow_null=True)
    revisit = serializers.BooleanField(required=False,)
    cooking_rating = serializers.IntegerField(required=False)
    feeding_rating = serializers.IntegerField(required=False)
    education_rating = serializers.IntegerField(required=False)
    allow = serializers.BooleanField(required=False,)
    reschedule_reason = serializers.CharField(max_length=None, required=False)
    delete = serializers.BooleanField(required=False,)

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
            'final_lng',
            'visited',
            'visit_date',
            'revisit',
            'cooking_rating',
            'feeding_rating',
            'education_rating',
            'allow',
            'reschedule_reason',
            'delete'
        ]


class HypoCreationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    user_id = serializers.IntegerField(required=False)
    app_uuid = serializers.CharField(required=False, max_length=200)
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
    image = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    phone_number = serializers.CharField(allow_blank=True, max_length=20, required=False)
    hypo_type = serializers.CharField(allow_blank=True, max_length=60, required=False)
    sampled = serializers.CharField(allow_blank=True, max_length=60, required=False)
    hypo_seen = serializers.CharField(allow_blank=True, max_length=60, required=False)
    demo_given = serializers.CharField(allow_blank=True, max_length=60, required=False)
    fb_liked = serializers.CharField(allow_blank=True, max_length=60, required=False)

    def validate_user_id(self, value):
        if not value:
            return 0
        try:
            value = int(value)
        except ValueError:
            raise serializers.ValidationError("Not Number")
        return value

    def create(self, validated_data):
        app_uid = validated_data.get('app_uuid')
        if Hypo.objects.filter(app_uuid=app_uid, duplicate=False).exists():
            Hypo.objects.filter(app_uuid=app_uid, duplicate=False).delete()

        return Hypo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class HypoCreationSerializer02(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)
    user_id = serializers.IntegerField(required=False)
    duplicate_uuid = serializers.CharField(required=False, max_length=200)
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
    phone_number = serializers.CharField(allow_blank=True, max_length=20, required=False)
    hypo_type = serializers.CharField(allow_blank=True, max_length=60, required=False)
    sampled = serializers.CharField(allow_blank=True, max_length=60, required=False)
    hypo_seen = serializers.CharField(allow_blank=True, max_length=60, required=False)
    demo_given = serializers.CharField(allow_blank=True, max_length=60, required=False)
    fb_liked = serializers.CharField(allow_blank=True, max_length=60, required=False)
    duplicate = serializers.BooleanField(default=True)

    def validate_user_id(self, value):
        if not value:
            return 0
        try:
            value = int(value)
        except ValueError:
            raise serializers.ValidationError("Not Number")
        return value

    def create(self, validated_data):
        app_uid = validated_data.get('app_uuid')
        if Hypo.objects.filter(app_uuid=app_uid, duplicate=False).exists():
            Hypo.objects.filter(app_uuid=app_uid, duplicate=False).delete()

        return Hypo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class HypoSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Hypo
        fields = [
                  'id',
                  'username',
                  'name',
                  'address',
                  'state',
                  'category',
                  'state',
                  'lga',
                  'lat',
                  'lng',
                  'landmark',
                  'remark',
                  'date_captured',
                  'image',
                  'phone_number',
                  'hypo_type',
                  'sampled',
                  'hypo_seen',
                  'demo_given',
                  'fb_liked',
                  'uuid',
                  'prd_1',
                  'prd_2',
                  'prd_3',
                  'prd_4',
                  'prd_5'
                  ]


class HypoUpdateSerializer(serializers.ModelSerializer):
    prd_1 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    prd_2 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    prd_3 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    prd_4 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    prd_5 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)

    class Meta(object):
        model = Hypo
        fields = [
            'prd_1',
            'prd_2',
            'prd_3',
            'prd_4',
            'prd_5'
        ]


class ReportSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=False, required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ExcelSerializer(serializers.Serializer):
    report = serializers.JSONField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ReportFilters(serializers.Serializer):
    state = serializers.CharField(required=False, max_length=9000)
    branch = serializers.CharField(required=False, max_length=100, allow_null=True, allow_blank=True)
    date_to = serializers.CharField(required=False, max_length=100)
    date_from = serializers.CharField(required=False, max_length=100)
    lga = serializers.CharField(required=False, max_length=9000)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class HotelSerializer(serializers.ModelSerializer):
    amenities = fields.MultipleChoiceField(choices=AMENITIES)
    user_id = serializers.IntegerField(required=False)
    user = UsersSerializer(required=False)

    class Meta:
        model = Hotel
        fields = ['id',
                  'amenities',
                  'name',
                  'address',
                  'state',
                  'lga',
                  'phone_number',
                  'email',
                  'contact_name',
                  'contact_phone',
                  'designation',
                  'no_of_rooms',
                  'no_of_restaurants',
                  'date_captured',
                  'user',
                  'user_id',
                  'rating',
                  'lat',
                  'lng',
                  'app_uid',
                  'image_1',
                  'image_2',
                  'image_3',
                  'image_4',
                  'image_5',
                  'remark',
                  'captured_time'
                  ]


class RestaurantSerializer(serializers.ModelSerializer):
    amenities = fields.MultipleChoiceField(choices=AMENITIES, required=False, allow_null=True, allow_blank=True)
    user_id = serializers.IntegerField(required=False)
    cuisines = fields.MultipleChoiceField(choices=CUISINE, required=False, allow_null=True, allow_blank=True)
    user = UsersSerializer(required=False)

    class Meta:
        model = Restaurant
        fields = ['id',
                  'amenities',
                  'name',
                  'address',
                  'state',
                  'lga',
                  'phone_number',
                  'email',
                  'contact_name',
                  'contact_phone',
                  'designation',
                  'no_of_tables',
                  'no_of_waiting_staff',
                  'cuisines',
                  'sample_type',
                  'date_captured',
                  'user',
                  'rating',
                  'user_id',
                  'lat',
                  'lng',
                  'app_uid',
                  'image_1',
                  'image_2',
                  'image_3',
                  'image_4',
                  'image_5',
                  'remark',
                  'captured_time'
                  ]


class BarSerializer(serializers.ModelSerializer):
    amenities = fields.MultipleChoiceField(choices=AMENITIES, required=False, allow_null=True, allow_blank=True)
    user_id = serializers.IntegerField(required=False)
    food_type = fields.MultipleChoiceField(choices=CUISINE, required=False, allow_null=True, allow_blank=True)
    user = UsersSerializer(required=False)

    class Meta:
        model = Bar
        fields = ['id',
                  'amenities',
                  'name',
                  'address',
                  'state',
                  'lga',
                  'phone_number',
                  'email',
                  'contact_name',
                  'contact_phone',
                  'designation',
                  'no_of_tables',
                  'no_of_waiting_staff',
                  'food_type',
                  'sample_type',
                  'date_captured',
                  'user',
                  'rating',
                  'user_id',
                  'lat',
                  'lng',
                  'app_uid',
                  'image_1',
                  'image_2',
                  'image_3',
                  'image_4',
                  'image_5',
                  'remark',
                  'captured_time'
                  ]


class CafeSerializer(serializers.ModelSerializer):
    amenities = fields.MultipleChoiceField(choices=AMENITIES, required=False, allow_null=True, allow_blank=True)
    user_id = serializers.IntegerField(required=False)
    offering = fields.MultipleChoiceField(choices=OFFERINGS, required=False, allow_null=True, allow_blank=True)
    user = UsersSerializer(required=False)

    class Meta:
        model = Cafe
        fields = ['id',
                  'amenities',
                  'name',
                  'address',
                  'state',
                  'lga',
                  'phone_number',
                  'email',
                  'contact_name',
                  'contact_phone',
                  'designation',
                  'no_of_tables',
                  'no_of_waiting_staff',
                  'showroom',
                  'sample_type',
                  'offering',
                  'showroom',
                  'date_captured',
                  'user',
                  'rating',
                  'user_id',
                  'lat',
                  'lng',
                  'app_uid',
                  'image_1',
                  'image_2',
                  'image_3',
                  'image_4',
                  'image_5',
                  'remark',
                  'captured_time'
                  ]


class HotelUpdateSerializer(serializers.ModelSerializer):
    image_1 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_2 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_3 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_4 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_5 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = Hotel
        fields = [
            'image_1',
            'image_2',
            'image_3',
            'image_4',
            'image_5'
        ]


class RestaurantUpdateSerializer(serializers.ModelSerializer):
    image_1 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_2 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_3 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_4 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_5 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = Restaurant
        fields = [
            'image_1',
            'image_2',
            'image_3',
            'image_4',
            'image_5'
        ]


class BarUpdateSerializer(serializers.ModelSerializer):
    image_1 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_2 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_3 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_4 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_5 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = Bar
        fields = [
            'image_1',
            'image_2',
            'image_3',
            'image_4',
            'image_5'
        ]


class CafeUpdateSerializer(serializers.ModelSerializer):
    image_1 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_2 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_3 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_4 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image_5 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)

    class Meta:
        model = Cafe
        fields = [
            'image_1',
            'image_2',
            'image_3',
            'image_4',
            'image_5'
        ]


class KelloggsRetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = KelloggsRetail
        fields = '__all__'


class KelloggsPreSamplingSerializer(serializers.ModelSerializer):
    class Meta:
        model = KelloggsPreSampling
        fields = '__all__'


class KelloggsPostSamplingSerializer(serializers.ModelSerializer):
    class Meta:
        model = KelloggsPostSampling
        fields = '__all__'


class KelloggsSamplingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False, max_length=200, allow_blank=True, allow_null=True)

    class Meta:
        model = KelloggsSchool
        fields = [
            'id',
            'user_id',
            'name',
            'school_type',
            'address',
            'lga',
            'landmark',
            'lat',
            'lng',
            'state',
            'contact_name',
            'contact_phone',
            'designation',
            'school_phone',
            'level',
            'target_level',
            'population',
            'target_population',
            'sampled_population',
            'school_image',
            'feedback_form',
            'students_uc_img',
            'mc_video',
            'students_sc_img',
            'date_captured',
            'app_uid',
            'username',
            'branch',
            'cocopops_32g_qty',
            'cocopops_450g_qty',
            'dano_cool_cow_25g_qty',
            'dano_cool_cow_360g_qty',
            'total_population',
            'lunch_box',
            'lunch_box_kelloggs'
        ]


class KelloggsUpdateSchoolSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)

    class Meta:
        model = KelloggsSchool
        fields = [
            'id',
            'user_id',
            'feedback_form',
            'students_uc_img',
            'mc_video',
            'students_sc_img',
            'final_lng',
            'final_lat',
            'visit_end_date',
            'visit_start_time',
            'visit_end_time',
            'visit_start_date',
            'sampled_population',
            'visited',
            'mc_name',
            'app_uid'
        ]


class KVisitedSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, max_length=200, allow_blank=True, allow_null=True)
    supervisor = serializers.CharField(required=False, max_length=200, allow_blank=True, allow_null=True)
    duration = serializers.CharField(required=False, max_length=200, allow_blank=True, allow_null=True)

    class Meta:
        model = KelloggsSchool
        fields = [
            'id',
            'name',
            'state',
            'branch',
            'sampled_population',
            'feedback_form',
            'students_uc_img',
            'mc_video',
            'students_sc_img',
            'date_captured',
            'username',
            'supervisor',
            'mc_name',
            'visit_start_time',
            'visit_end_time',
            'visit_start_date',
            'visit_end_date',
            'duration',
            'final_lat',
            'final_lng',
            'cocopops_32g_qty',
            'cocopops_450g_qty',
            'dano_cool_cow_25g_qty',
            'dano_cool_cow_360g_qty',
            'total_population',
            'lunch_box',
            'lunch_box_kelloggs'
        ]


class StateSerializer01(serializers.ModelSerializer):
    lga = serializers.StringRelatedField(many=True, source='lga_set')

    class Meta:
        model = State
        fields = ('name', 'lga')


class BranchSerializer01(serializers.ModelSerializer):
    state = StateSerializer01(many=True, source='state_set')

    class Meta:
        model = Branch
        fields = ('name', 'state')


class CountrySerializer02(serializers.ModelSerializer):
    branch = BranchSerializer01(many=True, source='branch_set')

    class Meta:
        model = Country
        fields = ['name', 'branch']


class CreateCountrySerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=100)
    branch_array = serializers.JSONField(allow_null=True, required=False)
    state_array = serializers.JSONField(allow_null=True, required=False)

    def validate_name(self, value):
        if Country.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Country already exists.")
        return value

    def create(self, validated_data):
        return Country.objects.create_country(validated_data)

    def update(self, instance, validated_data):
        pass


class UserSerializerLite(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta(object):
        model = UserProfile
        fields = ['user', 'id']


class SchoolSerializerLite(serializers.ModelSerializer):

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
                  'contact_name',
                  'contact_phone',
                  'school_phone',
                  'school_type',
                  'level',
                  'population',
                  'username',
                  'approved',
                  'landmark',
                  'designation',
                  'date_captured',
                  'delete',
                  'visit_date',
                  'supervisor',
                  'school_image',
                  'reschedule_reason',
                  'approve_filter',
                  'visited',
                  'branch',
                  'uuid',
                  'target_level',
                  'target_population',
                  'country',
                  'email',
                  'allow'
                  ]

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related(
            'user')

        return queryset


class HotelSerializerLite(serializers.ModelSerializer):
    amenities = fields.MultipleChoiceField(choices=AMENITIES)

    class Meta:
        model = Hotel
        fields = ['id',
                  'username',
                  'amenities',
                  'name',
                  'address',
                  'state',
                  'lga',
                  'phone_number',
                  'email',
                  'contact_name',
                  'contact_phone',
                  'designation',
                  'no_of_rooms',
                  'no_of_restaurants',
                  'date_captured',
                  'rating',
                  'lat',
                  'lng',
                  'image_1',
                  'image_2',
                  'image_3',
                  'image_4',
                  'image_5',
                  'remark',
                  'captured_time',
                  'branch'
                  ]


class RestaurantSerializerLite(serializers.ModelSerializer):
    amenities = fields.MultipleChoiceField(choices=AMENITIES, required=False, allow_null=True, allow_blank=True)
    cuisines = fields.MultipleChoiceField(choices=CUISINE, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Restaurant
        fields = ['id',
                  'amenities',
                  'name',
                  'address',
                  'state',
                  'lga',
                  'phone_number',
                  'email',
                  'contact_name',
                  'contact_phone',
                  'designation',
                  'no_of_tables',
                  'no_of_waiting_staff',
                  'cuisines',
                  'sample_type',
                  'date_captured',
                  'username',
                  'rating',
                  'lat',
                  'lng',
                  'image_1',
                  'image_2',
                  'image_3',
                  'image_4',
                  'image_5',
                  'remark',
                  'captured_time',
                  'branch'
                  ]


class BarSerializerLite(serializers.ModelSerializer):
    amenities = fields.MultipleChoiceField(choices=AMENITIES, required=False, allow_null=True, allow_blank=True)
    food_type = fields.MultipleChoiceField(choices=CUISINE, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Bar
        fields = ['id',
                  'amenities',
                  'name',
                  'address',
                  'state',
                  'lga',
                  'phone_number',
                  'email',
                  'contact_name',
                  'contact_phone',
                  'designation',
                  'no_of_tables',
                  'no_of_waiting_staff',
                  'food_type',
                  'sample_type',
                  'date_captured',
                  'username',
                  'rating',
                  'lat',
                  'lng',
                  'image_1',
                  'image_2',
                  'image_3',
                  'image_4',
                  'image_5',
                  'remark',
                  'captured_time',
                  'branch'
                  ]


class CafeSerializerLite(serializers.ModelSerializer):
    amenities = fields.MultipleChoiceField(choices=AMENITIES, required=False, allow_null=True, allow_blank=True)
    offering = fields.MultipleChoiceField(choices=OFFERINGS, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Cafe
        fields = ['id',
                  'amenities',
                  'name',
                  'address',
                  'state',
                  'lga',
                  'phone_number',
                  'email',
                  'contact_name',
                  'contact_phone',
                  'designation',
                  'no_of_tables',
                  'no_of_waiting_staff',
                  'showroom',
                  'sample_type',
                  'offering',
                  'showroom',
                  'date_captured',
                  'username',
                  'rating',
                  'lat',
                  'lng',
                  'image_1',
                  'image_2',
                  'image_3',
                  'image_4',
                  'image_5',
                  'remark',
                  'captured_time',
                  'branch'
                  ]


class VisitedSchoolSerializerLite(serializers.ModelSerializer):

    class Meta(object):
        model = School
        fields = [
                  'id',
                  'name',
                  'address',
                  'state',
                  'final_lat',
                  'final_lng',
                  'level',
                  'population',
                  'supervisor',
                  'cooking_video',
                  'feeding_video',
                  'education_video',
                  'visit_start_time',
                  'visit_end_time',
                  'visit_start_date',
                  'visit_end_date',
                  'lunch_box_with_noddles',
                  'lunch_box',
                  'cartons',
                  'sampled_population',
                  'final_population',
                  'duration',
                  'promoters',
                  'cooking_rating',
                  'feeding_rating',
                  'education_rating',
                  'branch',
                  'target_level',
                  'target_population',
                  'uuid',
                  'revisit',
                  'parent_id'
                  ]


class UsersSerializer02Lite(serializers.ModelSerializer):
    user = UserSerializer()
    supervisor_module = UserModuleSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['id',
                  'user',
                  'role',
                  'phone_number',
                  'password_string',
                  'user_module',
                  'state',
                  'country',
                  'branch',
                  'supervisor_module',
                  'supervisor',
                  'imei',
                  'username'
                  ]


class SchoolUpdateSerializerAdmin(serializers.ModelSerializer):
    visit_date = serializers.DateField(required=False, allow_null=True)
    revisit = serializers.BooleanField(required=False,)
    cooking_rating = serializers.IntegerField(required=False)
    feeding_rating = serializers.IntegerField(required=False)
    education_rating = serializers.IntegerField(required=False)
    allow = serializers.BooleanField(required=False,)
    reschedule_reason = serializers.CharField(max_length=None, required=False)
    delete = serializers.BooleanField(required=False,)
    approved = serializers.BooleanField(required=False, )

    class Meta(object):
        model = School
        fields = [
            'visit_date',
            'revisit',
            'cooking_rating',
            'feeding_rating',
            'education_rating',
            'allow',
            'reschedule_reason',
            'delete',
            'approved'
        ]
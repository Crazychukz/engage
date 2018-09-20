
from __future__ import unicode_literals

from django.db import models, transaction
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random, json
import string


class UserProfileRegistrationManager(models.Manager):

    @transaction.atomic
    def create_user(self, data):
        password = data.get('password')
        email = data.get('email')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user = User(
            email=email,
            last_name=last_name,
            username=username,
            first_name=first_name
        )
        user.is_active = True
        user.set_password(password)
        user.save()
        self.create_user_profile(user, data, password)
        return user

    def create_user_profile(self, user, data, password):
        role = data.get('role')
        branch = data.get('branch')
        phone_number = data.get('phone_number')
        supervisor = data.get('supervisor')
        user_module = data.get('user_module')
        state = data.get("state")
        if role == 'Marketing Executive':
            supervisor_user = UserProfile.objects.get(id=supervisor)
            user_state = supervisor_user.state
            user_branch = supervisor_user.branch

            new_profile = self.create(
                user=user,
                role=role,
                phone_number=phone_number,
                password_string=password,
                user_module=user_module,
                state=user_state,
                supervisor=supervisor_user,
                branch=user_branch

            )

            return new_profile

        if role == 'Supervisor' or role == 'Admin':
            supervisor_module = json.loads(data.get('supervisor_module'))
            new_profile = self.create(
                user=user,
                role=role,
                phone_number=phone_number,
                password_string=password,
                user_module=user_module,
                state=state,
                branch=branch
            )
            for i in supervisor_module:
                sup_module = UserModules.objects.get(id=i)
                new_profile.supervisor_module.add(sup_module)
                new_profile.save()

            return new_profile

        new_profile = self.create(
            user=user,
            role=role,
            phone_number=phone_number,
            password_string=password,
            user_module=user_module,
            state=state,
            branch=branch
        )

        return new_profile

    def generate_password(self):
        chars = string.ascii_lowercase + string.digits
        new_password = ''.join(random.choice(chars) for _ in range(8))

        return new_password

    @transaction.atomic
    def update_user(self, data):
        id = data.get('id')
        role = data.get('role')
        password_string = data.get('password_string')
        branch = data.get('branch')
        phone_number = data.get('phone_number')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        supervisor = data.get('supervisor')
        user_module = data.get('user_module')
        state = data.get("state")

        mainuser = UserProfile.objects.get(id=id)
        mainuser.role = role
        mainuser.password_string = password_string
        mainuser.phone_number = phone_number
        mainuser.save()

        mainuser.user.set_password(password_string)
        mainuser.user.first_name = first_name
        mainuser.user.email = email
        mainuser.user.last_name = last_name
        mainuser.user.save()

        if role == 'Marketing Executive':
            mainuser.user_module = user_module
            mainuser.save()
            if supervisor is not None:
                new_supervisor = UserProfile.objects.get(id=supervisor)
                mainuser.supervisor = new_supervisor
                mainuser.state = new_supervisor.state
                mainuser.branch = new_supervisor.branch
                mainuser.save()

        if role == 'Admin' or role == 'Supervisor':
            mainuser.branch = branch
            mainuser.state = state
            mainuser.save()
            supervisor_module = json.loads(data.get('supervisor_module'))
            mainuser.supervisor_module.clear()
            for i in supervisor_module:
                sup_module = UserModules.objects.get(id=i)
                mainuser.supervisor_module.add(sup_module)
                mainuser.save()

        if role == 'Supervisor':
            all_users = UserProfile.objects.filter(supervisor=mainuser, role='Marketing Executive')
            for i in all_users:
                i.state = state
                i.branch = branch
                i.save()

        return mainuser


class UserModules(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name', blank=True, null=True)
    active = models.BooleanField(verbose_name='Active', default=True)

    class Meta:
        verbose_name_plural = "User Modules"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    ROLES = (
        ('Supervisor', 'Supervisor'),
        ('Marketing Executive', 'Marketing Executive'),
        ('Branch Admin', 'Branch Admin'),
        ('Super Admin', 'Super Admin'),
        ('Admin', 'Admin'),
    )

    MODULE = (
        ('School Sampling', 'School Sampling'),
        ('Hypo Sampling', 'Hypo Sampling'),
        ('University Sampling', 'University Sampling'),
        ('Fan Clubs', 'Fan Clubs'),
        ('All', 'All'),
    )
    STATES = (
        ('Abuja', 'Abuja'),
        ('Abia', 'Abia'),
        ('University Sampling', 'University Sampling'),
        ('Fan Clubs', 'Fan Clubs'),
        ('All', 'All'),
    )

    user = models.OneToOneField(User, verbose_name='User')
    password_string = models.CharField(max_length=20, null=False, verbose_name='Password String')
    phone_number = models.CharField(max_length=11, verbose_name='Phone Number')
    role = models.CharField(max_length=50, choices=ROLES, verbose_name='Role',  blank=True)
    imei = models.CharField(max_length=50, verbose_name='IMEI', blank=True)
    supervisor = models.ForeignKey('UserProfile', verbose_name='Supervisor', null=True, blank=True)
    user_module = models.CharField(choices=MODULE, null=True, blank=True, verbose_name='User Module', max_length=200)
    supervisor_module = models.ManyToManyField(UserModules, null=True, blank=True, verbose_name='Supervisor User Module')
    super_admin = models.BooleanField(default=False, verbose_name='Super Admin')
    state = models.CharField(max_length=200, verbose_name='State', null=True)
    branch = models.CharField(max_length=300, verbose_name='Branch', null=True, blank=True)
    objects = UserProfileRegistrationManager()

    class Meta:
        verbose_name_plural = "User Profiles"
        ordering = ['-id']

    def __str__(self):
        return self.user.username

    def created(self):
        created = 0
        if self.user_module == 'School Sampling':
            created = School.objects.filter(user=self).count()

        if self.user_module == 'Hypo Sampling':
            created = Hypo.objects.filter(user=self).count()
        return created

    def visited(self):
        visited = School.objects.filter(user=self, visited=True).count()
        return visited


class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name='Branch Name')
    address = models.CharField(max_length=200, verbose_name='Address')


class SchoolRegistrationManager(models.Manager):

    @transaction.atomic
    def create_school(self, data):
        user_id = data.get("user_id")
        name = data.get("name")
        state = data.get("state")
        lga = data.get("lga")
        lat = data.get("lat")
        lng = data.get("lng")
        contact_name = data.get("contact_name")
        contact_phone = data.get("contact_phone")
        school_phone = data.get("school_phone")
        level = data.get("level")
        nursery_population = data.get("nursery_population")
        population = data.get("population")
        school_type = data.get("school_type")
        address = data.get("address")
        landmark = data.get("landmark")
        designation = data.get("designation")
        img_string = data.get("img_string")
        date_cap = data.get("date_captured")
        school_image = data.get("school_image")
        date_captured = datetime.strptime(date_cap, "%Y-%m-%d")

        if user_id is not None:
            check_user = UserProfile.objects.filter(id=user_id).exists()
            if check_user is True:
                field_manager = UserProfile.objects.get(id=user_id)

                new_school = School(
                    user=field_manager,
                    name=name,
                    state=state,
                    lga=lga,
                    lat=lat,
                    lng=lng,
                    contact_name=contact_name,
                    contact_phone=contact_phone,
                    school_phone=school_phone,
                    level=level,
                    nursery_population=nursery_population,
                    population=population,
                    school_type=school_type,
                    address=address,
                    landmark=landmark,
                    designation=designation,
                    img_string=img_string,
                    date_captured=date_captured,
                    school_image=school_image
                )
                new_school.save()
        return data

    @transaction.atomic
    def book_appointment(self, data):
        date_vit = data.get("visit_date")
        visit_date = datetime.strptime(date_vit, "%Y-%m-%d")
        school_id = data.get("id")
        reschedule_reason = data.get("reschedule_reason")
        school = School.objects.get(id=school_id)
        school.visit_date = visit_date
        if reschedule_reason:
            school.reschedule_reason = reschedule_reason

        school.save()

        return data

    @transaction.atomic
    def rate_school(self, data):
        school_id = data.get("id")
        mode = data.get("mode")
        rate = data.get("rate")
        school = School.objects.get(id=school_id)

        if mode == 'Cooking':
            school.cooking_rating = rate
            school.save()
            return data

        if mode == 'Feeding':
            school.feeding_rating = rate
            school.save()
            return data

        if mode == 'Education':
            school.education_rating = rate
            school.save()
            return data

        return data

    @transaction.atomic
    def update_school(self, data):
        id = data.get('id')
        name = data.get('name')
        school_type = data.get('school_type')
        address = data.get('address')
        lga = data.get('lga')
        contact_name = data.get('contact_name')
        contact_phone = data.get('contact_phone')
        school_phone = data.get('school_phone')
        level = data.get('level')
        population = data.get('population')
        nursery_population = data.get('nursery_population')
        landmark = data.get('landmark')
        designation = data.get('designation')

        main_school = School.objects.get(id=id)
        main_school.name = name
        main_school.school_type = school_type
        main_school.address = address
        main_school.lga = lga
        main_school.contact_name = contact_name
        main_school.contact_phone = contact_phone
        main_school.school_phone = school_phone
        main_school.level = level
        main_school.population = population
        main_school.nursery_population = nursery_population
        main_school.landmark = landmark
        main_school.designation = designation

        main_school.save()

        return True
        pass


class School(models.Model):
    TYPE = (
        ('Government', 'Government'),
        ('Private', 'Private'),
    )
    STATUS = (
        ('Pending Approval', 'Pending Approval'),
        ('Approved', 'Approved'),
        ('Visit Scheduled', 'Visit Scheduled'),
    )

    LEVEL = (
        ('Nursery', 'Nursery'),
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('Nursery - Primary', 'Nursery - Primary'),
        ('Nursery - Secondary', 'Nursery - Secondary'),
        ('Primary - Secondary', 'Primary - Secondary'),
        ('Creche/Nursery/Primary/Secondary', 'Creche/Nursery/Primary/Secondary'),
    )
    name = models.CharField(max_length=200, verbose_name='School Name', blank=True)
    school_type = models.CharField(max_length=100, verbose_name='School Type', choices=TYPE, null=True)
    approved = models.BooleanField(default=False, verbose_name='Approved')
    visited = models.BooleanField(default=False, verbose_name='Visited')
    address = models.CharField(max_length=200, verbose_name='Address')
    landmark = models.CharField(max_length=200, verbose_name='Landmark', null=True)
    designation = models.CharField(max_length=200, verbose_name='Designation', null=True)
    state = models.CharField(max_length=50, verbose_name='State')
    lga = models.CharField(max_length=100, verbose_name='LGA')
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    final_lat = models.FloatField(verbose_name='Final Latitude', default=0.0, null=True)
    final_lng = models.FloatField(verbose_name='Final Longitude', default=0.0, null=True)
    contact_name = models.CharField(verbose_name='Contact Person', max_length=200, null=True)
    contact_phone = models.CharField(verbose_name='Contact Phone Number', max_length=20, null=True)
    school_phone = models.CharField(verbose_name='School Phone Number', max_length=20, null=True)
    level = models.CharField(verbose_name='Level', max_length=100, choices=LEVEL)
    nursery_population = models.IntegerField(verbose_name='Nursery Population', default=0)
    population = models.IntegerField(verbose_name='Total Population', default=0)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True)
    school_image = models.ImageField(verbose_name='School Image', default='schools/images/noimage.jpg', blank=True, upload_to='schools/images/')
    cooking_video = models.FileField(verbose_name='Cooking Video', blank=True, null=True, upload_to='schools/videos/' )
    feeding_video = models.FileField(verbose_name='Feeding Video', blank=True, null=True, upload_to='schools/videos/')
    education_video = models.FileField(verbose_name='Education Video', blank=True, null=True, upload_to='schools/videos/' )
    other_video = models.FileField(verbose_name='Education Video', blank=True, null=True, upload_to='schools/videos/')
    final_population = models.IntegerField(verbose_name='Final Population', default=0)
    sampled_population = models.IntegerField(verbose_name='Sampled Population', default=0)
    cartons = models.IntegerField(verbose_name='Cartons', default=0)
    lunch_box = models.IntegerField(verbose_name='Lunch Box', default=0)
    lunch_box_with_noddles = models.IntegerField(verbose_name='Lunch Box With Noddles', default=0)
    promoters = models.IntegerField(verbose_name='Promoters', default=0)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    visit_date = models.DateField(verbose_name='Visit Date', null=True, blank=True)
    visit_start_time = models.TimeField(verbose_name='Visit Start Time', null=True, blank=True)
    visit_end_time = models.TimeField(verbose_name='Visit End Time', null=True, blank=True)
    visit_start_date = models.DateField(verbose_name='Visit Start Date', null=True, blank=True)
    visit_end_date = models.DateField(verbose_name='Visit End Date', null=True, blank=True)
    status = models.CharField(max_length=200, choices=STATUS, verbose_name='Status', null=True, blank=True)
    reschedule_reason = models.TextField(verbose_name='Reason for Reschedule', null=True, blank=True)
    delete = models.BooleanField(default=False, verbose_name='Delete')
    cooking_rating = models.IntegerField(default=0, null=True, blank=True, verbose_name='Cooking Rating')
    feeding_rating = models.IntegerField(default=0, null=True, blank=True, verbose_name='Feeding Rating')
    education_rating = models.IntegerField(default=0, null=True, blank=True, verbose_name='Cooking Rating')
    objects = SchoolRegistrationManager()

    class Meta:
        verbose_name_plural = "School Sampling"
        ordering = ['-id']

    def __str__(self):
        return self.name

    def supervisor(self):
        if self.user is not None and self.user.supervisor is not None:
            supervisor = self.user.supervisor.user.username

            return supervisor
        else:

            return 'None'

    def branch(self):
        if self.user is not None and self.user.branch is not None:
            branch = self.user.branch

            return branch
        else:

            return 'None'

    def approve_filter(self):
        if self.approved:
            return 'Yes'
        if not self.approved:
            return 'No'

    def check_visited(self):
        if self.cooking_video and self.feeding_video is not None:
            self.visited = True

    def duration(self):
        if self.visit_end_date and self.visit_end_time and self.visit_start_date and self.visit_start_time:
            main_dpt = datetime.strptime(str(self.visit_start_date ) + str(self.visit_start_time), "%Y-%m-%d%H:%M:%S")
            main_dpt2 = datetime.strptime(str(self.visit_end_date ) + str(self.visit_end_time), "%Y-%m-%d%H:%M:%S")
            return (main_dpt2 - main_dpt).seconds


class Hypo(models.Model):
    TYPE = (
        ('Hospital', 'Hospital'),
        ('Home', 'Home'),
    )

    FILTER = (
        ('Bleach', 'Bleach'),
        ('Toilet Cleaner', 'Toilet Cleaner'),
        ('Both', 'Both')
    )

    name = models.CharField(max_length=200, verbose_name='School Name', blank=True)
    category = models.CharField(max_length=100, verbose_name='Category', choices=TYPE, null=True)
    address = models.CharField(max_length=200, verbose_name='Address', null=True, blank=True)
    landmark = models.CharField(max_length=200, verbose_name='Landmark', null=True, blank=True)
    state = models.CharField(max_length=50, verbose_name='State', null=True, blank=True )
    lga = models.CharField(max_length=100, verbose_name='LGA', null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)
    remark = models.TextField(verbose_name='Remark', null=True, blank=True)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    image = models.ImageField(verbose_name='Hypo Image', default='hypo/images/noimage.jpg', blank=True,
                              upload_to='hypo/images/')
    phone_number = models.CharField(verbose_name='Phone Number', max_length=20, null=True)
    hypo_type = models.CharField(verbose_name='Hypo Type',max_length=30, null=True, blank=True, choices=FILTER)

    class Meta:
        verbose_name_plural = "Hypo Sampling"
        ordering = ['-id']

    def __str__(self):
        return self.name

    def supervisor(self):
        if self.user is not None and self.user.supervisor is not None:
            supervisor = self.user.supervisor.user.username

            return supervisor
        else:
            return 'None'

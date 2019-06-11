from __future__ import unicode_literals
from django.db import models, transaction
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random, json
import string
from django.db.models import Sum
from multiselectfield import MultiSelectField
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class CountryManager(models.Manager):

    @transaction.atomic
    def create_country(self, data):
        name = data.get('name')
        branches = data.get('branch_array')
        states_data = data.get('state_array')

        new_country = Country(
            name=name
        )
        new_country.save()
        branch_json = branches.replace('\\', '')
        branch_array = json.loads(branch_json)
        for i in branch_array:
            new_branch = Branch(
                name=i,
                country=new_country
            )
            new_branch.save()
        state_json = states_data.replace('\\', '')
        state_array = json.loads(state_json)

        for i in state_array:
            check_state = State.objects.filter(branch__country=new_country, branch__name=i['branch'],
                                               name=i['state']).exists()
            if check_state is False:
                new_state = State(
                    name=i['state'],
                    branch=Branch.objects.get(name=i['branch'], country=new_country)
                )
                new_state.save()

            new_lga = LGA(
                name=i['lga'],
                state=State.objects.get(name=i['state'], branch__country=new_country, branch__name=i['branch'])
            )
            new_lga.save()

        return new_country


class Country(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name', blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name='Active')
    objects = CountryManager()

    class Meta:
        verbose_name_plural = "Country"
        ordering = ['-id']

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'No Name'


class Branch(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name', null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, verbose_name='Country')
    address = models.CharField(max_length=200, verbose_name='Address')
    active = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        verbose_name_plural = "Branch"
        ordering = ['-id']

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'No Name'


class State(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name', null=True, blank=True)
    branch = models.ForeignKey(Branch, null=True, blank=True, verbose_name='Branch')
    active = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        verbose_name_plural = "State"
        ordering = ['-id']

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'No Name'


class LGA(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name', null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True, verbose_name='State')
    active = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        verbose_name_plural = "LGA"
        ordering = ['-id']

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'No Name'


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
        country = data.get("country")
        if role == 'Marketing Executive':
            supervisor_user = UserProfile.objects.get(id=supervisor)
            user_state = supervisor_user.state
            user_country = supervisor_user.country
            user_branch = supervisor_user.branch

            new_profile = self.create(
                user=user,
                role=role,
                phone_number=phone_number,
                password_string=password,
                user_module=user_module,
                state=user_state,
                country=user_country,
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
                country=country,
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
            country=country,
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
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        supervisor = data.get('supervisor')
        user_module = data.get('user_module')
        state = data.get("state")
        country = data.get("country")
        reset_imei = data.get("reset_imei")

        mainuser = UserProfile.objects.get(id=id)
        mainuser.role = role
        mainuser.password_string = password_string
        mainuser.phone_number = phone_number
        mainuser.save()

        mainuser.user.set_password(password_string)
        mainuser.user.first_name = first_name
        mainuser.user.username = username
        mainuser.user.email = email
        mainuser.user.last_name = last_name
        mainuser.user.save()

        if role == 'Marketing Executive':
            mainuser.user_module = user_module
            mainuser.save()
            if reset_imei:
                sn_trash = SNTrash(
                    serial_number=mainuser.imei,
                    user=mainuser
                )
                sn_trash.save()
                mainuser.imei = ''
                mainuser.save()

            if supervisor is not None:
                new_supervisor = UserProfile.objects.get(id=supervisor)
                mainuser.supervisor = new_supervisor
                mainuser.state = new_supervisor.state
                mainuser.country = new_supervisor.country
                mainuser.branch = new_supervisor.branch
                mainuser.save()

        if role == 'Admin' or role == 'Supervisor':
            mainuser.branch = branch
            mainuser.state = state
            mainuser.country = country
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
                i.country = country
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

    COUNTRY = (
        ('Algeria', 'Algeria'),
        ('Angola', 'Angola'),
        ('Benin', 'Benin'),
        ('Botswana', 'Botswana'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cabo Verde', 'Cabo Verde'),
        ('Cameroon', 'Cameroon'),
        ('Central African Republic', 'Central African Republic'),
        ('Botswana', 'Botswana'),
        ('Chad', 'Chad'),
        ('Comoros', 'Comoros'),
        ('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),
        ('Republic of the Congo', 'Republic of the Congo'),
        ('Cote d\'Ivoire', 'Cote d\'Ivoire'),
        ('Djibouti', 'Djibouti'),
        ('Egypt', 'Egypt'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Eswatini', 'Eswatini'),
        ('Ethiopia', 'Ethiopia'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Ghana', 'Ghana'),
        ('Guinea', 'Guinea'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Kenya', 'Kenya'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Madagascar', 'Madagascar'),
        ('Malawi', 'Malawi'),
        ('Mali', 'Mali'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Namibia', 'Namibia'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Rwanda', 'Rwanda'),
        ('Sao Tome and Principe', 'Sao Tome and Principe'),
        ('Senegal', 'Senegal'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('South Sudan', 'South Sudan'),
        ('Sudan', 'Sudan'),
        ('Tanzania', 'Tanzania'),
        ('Togo', 'Togo'),
        ('Tunisia', 'Tunisia'),
        ('Uganda', 'Uganda'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe'),
    )

    MODULE = (
        ('School Sampling', 'School Sampling'),
        ('Hypo Sampling', 'Hypo Sampling'),
        ('University Sampling', 'University Sampling'),
        ('Fan Clubs', 'Fan Clubs'),
        ('HORECA', 'HORECA'),
        ('Kelloggs', 'Kelloggs'),
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
    role = models.CharField(max_length=50, choices=ROLES, verbose_name='Role', blank=True)
    imei = models.CharField(max_length=50, verbose_name='IMEI', blank=True)
    supervisor = models.ForeignKey('UserProfile', verbose_name='Supervisor', null=True, blank=True)
    user_module = models.CharField(choices=MODULE, null=True, blank=True, verbose_name='User Module', max_length=200)
    supervisor_module = models.ManyToManyField(UserModules, null=True, blank=True,
                                               verbose_name='Supervisor User Module')
    super_admin = models.BooleanField(default=False, verbose_name='Super Admin')
    state = models.CharField(max_length=200, verbose_name='State', null=True)
    country = models.CharField(max_length=200, verbose_name='Country', choices=COUNTRY, null=True, blank=True)
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

        if self.user_module == 'Kelloggs':
            created = KelloggsSchool.objects.filter(user=self).count()
        return created

    def visited(self):
        visited = School.objects.filter(user=self, visited=True).count()
        return visited

    def last_month_planned(self):
        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=last_month, visit_date__year=now.year).count()
            return schools
        else:
            return 0

    def this_month_planned(self):
        now = datetime.now()
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=now.month, visit_date__year=now.year).count()
            return schools
        else:
            return 0

    def last_month_visited(self):
        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=last_month, visit_date__year=now.year,
                                            visited=True).count()
            return schools
        else:
            return 0

    def this_month_visited(self):
        now = datetime.now()
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=now.month, visit_date__year=now.year,
                                            visited=True).count()
            return schools
        else:
            return 0

    def last_month_cooking_sop(self):
        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=last_month, visit_date__year=now.year,
                                            visited=True, cooking_rating__lt=5).count()
            return schools
        else:
            return 0

    def this_month_cooking_sop(self):
        now = datetime.now()
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=now.month, visit_date__year=now.year,
                                            visited=True, cooking_rating__lt=5).count()
            return schools
        else:
            return 0

    def last_month_feeding_sop(self):
        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=last_month, visit_date__year=now.year,
                                            visited=True, feeding_rating__lt=5).count()
            return schools
        else:
            return 0

    def this_month_feeding_sop(self):
        now = datetime.now()
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=now.month, visit_date__year=now.year,
                                            visited=True, feeding_rating__lt=5).count()
            return schools
        else:
            return 0

    def last_month_education_sop(self):
        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=last_month, visit_date__year=now.year,
                                            visited=True, education_rating__lt=5).count()
            return schools
        else:
            return 0

    def this_month_education_sop(self):
        now = datetime.now()
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            schools = School.objects.filter(user=self, visit_date__month=now.month, visit_date__year=now.year,
                                            visited=True, education_rating__lt=5).count()
            return schools
        else:
            return 0

    def pupils_sampled_this_month(self):
        now = datetime.now()
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            total_pupil = 0
            pupils = School.objects.filter(user=self, visit_date__month=now.month,
                                           visit_date__year=now.year).aggregate(Sum('target_population'))
            if pupils[pupils.keys()[0]]:
                total_pupil = pupils[pupils.keys()[0]]

            return total_pupil
        else:
            return 0

    def pupils_sampled_last_month(self):
        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            total_pupil = 0
            pupils = School.objects.filter(user=self, visit_date__month=last_month,
                                           visit_date__year=now.year).aggregate(Sum('target_population'))
            if pupils[pupils.keys()[0]]:
                total_pupil = pupils[pupils.keys()[0]]

            return total_pupil
        else:
            return 0

    def lunch_box_this_month(self):
        now = datetime.now()
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            lunch_box = 0
            pupils = School.objects.filter(user=self, visit_date__month=now.month,
                                           visit_date__year=now.year).aggregate(Sum('lunch_box'))
            if pupils[pupils.keys()[0]]:
                lunch_box = pupils[pupils.keys()[0]]

            return lunch_box
        else:
            return 0

    def lunch_box_last_month(self):
        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            lunch_box = 0
            pupils = School.objects.filter(user=self, visit_date__month=last_month,
                                           visit_date__year=now.year).aggregate(Sum('lunch_box'))
            if pupils[pupils.keys()[0]]:
                lunch_box = pupils[pupils.keys()[0]]

            return lunch_box
        else:
            return 0

    def with_noddles_this_month(self):
        now = datetime.now()
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            lunch_box = 0
            pupils = School.objects.filter(user=self, visit_date__month=now.month,
                                           visit_date__year=now.year).aggregate(Sum('lunch_box_with_noddles'))
            if pupils[pupils.keys()[0]]:
                lunch_box = pupils[pupils.keys()[0]]

            return lunch_box
        else:
            return 0

    def with_noddles_last_month(self):
        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        if self.role == 'Marketing Executive' and self.user_module == 'School Sampling':
            lunch_box = 0
            pupils = School.objects.filter(user=self, visit_date__month=last_month,
                                           visit_date__year=now.year).aggregate(Sum('lunch_box_with_noddles'))
            if pupils[pupils.keys()[0]]:
                lunch_box = pupils[pupils.keys()[0]]

            return lunch_box
        else:
            return 0

    def username(self):
        if self.user.username is not None:
            return self.user.username.lower()
        else:
            return 'None'

    def lga(self):
        lga = []
        all_lga = LGA.objects.filter(state__name=self.state, state__branch__name=self.branch)
        for i in all_lga:
            lga.append(i.name)
        return lga


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
        target_level = data.get("target_level")
        target_population = data.get("target_population")
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
                    school_image=school_image,
                    target_level=target_level,
                    target_population=target_population
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
        target_level = data.get("target_level")
        target_population = data.get("target_population")

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
        main_school.target_level = target_level
        main_school.target_population = target_population

        main_school.save()

        return True


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
        ('Secondary School', 'Secondary School'),
        ('Creche/Nursery/Primary/Secondary', 'Creche/Nursery/Primary/Secondary'),
    )
    TARGET_LEVEL = (
        ('Nursery', 'Nursery'),
        ('Primary', 'Primary'),
        ('Nursery & Primary', 'Nursery & Primary'),
        ('Junior Secondary', 'Junior Secondary'),
        ('Senior Secondary', 'Senior Secondary'),
        ('Junior & Senior Secondary', 'Junior & Senior Secondary'),
        ('Creche', 'Creche'),
        ('Kindergarten', 'Kindergarten')
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
    target_level = models.CharField(verbose_name='Target Level', max_length=100, choices=TARGET_LEVEL, null=True)
    target_population = models.IntegerField(verbose_name='Target Population', default=0)
    nursery_population = models.IntegerField(verbose_name='Nursery Population', default=0, null=True, blank=True)
    population = models.IntegerField(verbose_name='Total Population', default=0, null=True, blank=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True)
    school_image = models.ImageField(verbose_name='School Image', default='schools/images/noimage.jpg', blank=True,
                                     upload_to='schools/images/')
    cooking_video = models.FileField(verbose_name='Cooking Video', blank=True, null=True, upload_to='schools/videos/')
    feeding_video = models.FileField(verbose_name='Feeding Video', blank=True, null=True, upload_to='schools/videos/')
    education_video = models.FileField(verbose_name='Education Video', blank=True, null=True,
                                       upload_to='schools/videos/')
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
    email = models.CharField(max_length=200, verbose_name='Email', blank=True, null=True, default='N/A')
    allow = models.BooleanField(default=False,)
    revisit = models.BooleanField(default=False,)
    revisited = models.BooleanField(default=False,)
    parent_id = models.IntegerField(null=True, blank=True, verbose_name='Parent ID')
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
            main_dpt = datetime.strptime(str(self.visit_start_date) + str(self.visit_start_time), "%Y-%m-%d%H:%M:%S")
            main_dpt2 = datetime.strptime(str(self.visit_end_date) + str(self.visit_end_time), "%Y-%m-%d%H:%M:%S")
            return (main_dpt2 - main_dpt).seconds

    def uuid(self):
        if self.parent_id is not None:
            return 'SS' + self.state.upper()[:3] + str(self.parent_id)
        else:
            return 'SS' + self.state.upper()[:3] + str(self.id)

    def username(self):
        return self.user.user.username

    def country(self):
        if self.user.country:
            return self.user.country
        else:
            return 'None'


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

    CHOICE = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )

    name = models.CharField(max_length=200, verbose_name='Name', blank=True)
    category = models.CharField(max_length=100, verbose_name='Category', choices=TYPE, null=True)
    address = models.CharField(max_length=200, verbose_name='Address', null=True, blank=True)
    landmark = models.CharField(max_length=200, verbose_name='Landmark', null=True, blank=True)
    state = models.CharField(max_length=50, verbose_name='State', null=True, blank=True)
    lga = models.CharField(max_length=100, verbose_name='LGA', null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)
    remark = models.TextField(verbose_name='Remark', null=True, blank=True)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    image = models.ImageField(verbose_name='Hypo Image', default='hypo/images/noimage.jpg', blank=True,
                              upload_to='hypo/images/')
    prd_1 = models.ImageField(verbose_name='Product Demo 1', default='hypo/images/noimage.jpg', blank=True, null=True,
                              upload_to='hypo/images/')
    prd_2 = models.ImageField(verbose_name='Product Demo 2', default='hypo/images/noimage.jpg', blank=True, null=True,
                              upload_to='hypo/images/')
    prd_3 = models.ImageField(verbose_name='Product Demo 3', default='hypo/images/noimage.jpg', blank=True, null=True,
                              upload_to='hypo/images/')
    prd_4 = models.ImageField(verbose_name='Product Demo 4', default='hypo/images/noimage.jpg', blank=True, null=True,
                              upload_to='hypo/images/')
    prd_5 = models.ImageField(verbose_name='Product Demo 5', default='hypo/images/noimage.jpg', blank=True, null=True,
                              upload_to='hypo/images/')
    phone_number = models.CharField(verbose_name='Phone Number', max_length=20, null=True)
    app_uuid = models.CharField(verbose_name='App UUID', max_length=200, null=True, blank=True)
    hypo_type = models.CharField(verbose_name='Hypo Type', max_length=30, null=True, blank=True, choices=FILTER)
    sampled = models.CharField(verbose_name='Sampled Before', max_length=30, null=True, blank=True, choices=CHOICE)
    hypo_seen = models.CharField(verbose_name='Hypo Seen', max_length=30, null=True, blank=True, choices=CHOICE)
    demo_given = models.CharField(verbose_name='Demo Given', max_length=30, null=True, blank=True, choices=CHOICE)
    fb_liked = models.CharField(verbose_name='Facebook Page Liked', max_length=30, null=True, blank=True,
                                choices=CHOICE)
    duplicate = models.BooleanField(verbose_name='Duplicate', default=False)
    duplicate_uuid = models.CharField(verbose_name='Duplicate UUID', max_length=200, null=True, blank=True)

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

    def uuid(self):
        return 'HS' + self.state.upper()[:3] + str(self.id)

    def username(self):
        return self.user.user.username


class Hotel(models.Model):
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
        ('Night Club', 'Night Club')
    )
    name = models.CharField(max_length=200, verbose_name='Name', null=True, blank=True)
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    state = models.CharField(max_length=50, verbose_name='State', null=True, blank=True)
    lga = models.CharField(max_length=100, verbose_name='LGA', null=True, blank=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=12, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    contact_name = models.CharField(verbose_name='Contact Name', max_length=200, null=True, blank=True)
    contact_phone = models.CharField(verbose_name='Contact Phone Number', max_length=12, null=True, blank=True)
    designation = models.CharField(verbose_name='Contact Designation', max_length=100, null=True, blank=True)
    no_of_rooms = models.IntegerField(verbose_name='Number of Rooms', null=True, blank=True, default=0)
    no_of_restaurants = models.IntegerField(verbose_name='Number of Restaurants/Cafeteria', null=True, blank=True,
                                            default=0)
    amenities = MultiSelectField(choices=AMENITIES, max_length=100, max_choices=30, null=True, blank=True,
                                 verbose_name='Amenities')
    image_1 = models.ImageField(verbose_name='Image 1', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_2 = models.ImageField(verbose_name='Image 2', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_3 = models.ImageField(verbose_name='Image 3', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_4 = models.ImageField(verbose_name='Image 4', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_5 = models.ImageField(verbose_name='Image 5', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    app_uid = models.CharField(verbose_name='App UID', max_length=200, blank=True, null=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    captured_time = models.TimeField(verbose_name='Time Captured', null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    remark = models.TextField(verbose_name='Remark', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Hotels"
        ordering = ['-id']

    def __str__(self):
        return self.name

    def branch(self):
        if self.state is not None:
            obj = State.objects.filter(name__iexact=self.state)
            if obj.exists():
                branch = obj.first().branch.name
                return branch
            else:
                return 'N/A'
        else:
            return 'N/A'

    def rating(self):
        if self.amenities is not None:
            amenities = len(self.amenities)
        else:
            amenities = 0

        if amenities >= 9:
            return 'A'
        if 3 <= amenities <= 7:
            return 'B'
        if amenities <= 2:
            return 'C'

    def username(self):
        return self.user.user.username


class Restaurant(models.Model):
    AMENITIES = (
        ('Banquet', 'Banquet'),
        ('Bar', 'Bar'),
        ('Kids play area', 'Kids play area')
    )
    TYPE = (
        ('Fine Dine', 'Fine Dine'),
        ('Cafe', 'Cafe'),
        ('Casual', 'Casual'),
        ('Fast Food', 'Fast Food'),
        ('Buka', 'Buka'),
        ('Canteen', 'Canteen')
    )
    CUISINE = (
        ('Nigerian', 'Nigerian'),
        ('Chinese', 'Chinese'),
        ('Continental', 'Continental'),
        ('Indian', 'Indian'),
        ('Arabic/Lebanese', 'Arabic/Lebanese'),
        ('Mexican', 'Mexican'),
        ('Italian', 'Italian'),
        ('Asian', 'Asian')
    )
    name = models.CharField(max_length=200, verbose_name='Name', null=True, blank=True)
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    state = models.CharField(max_length=50, verbose_name='State', null=True, blank=True)
    lga = models.CharField(max_length=100, verbose_name='LGA', null=True, blank=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=12, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    contact_name = models.CharField(verbose_name='Contact Name', max_length=200, null=True, blank=True)
    contact_phone = models.CharField(verbose_name='Contact Phone Number', max_length=12, null=True, blank=True)
    designation = models.CharField(verbose_name='Contact Designation', max_length=100, null=True, blank=True)
    no_of_tables = models.IntegerField(verbose_name='Number of Tables', null=True, blank=True, default=0)
    no_of_waiting_staff = models.IntegerField(verbose_name='Number of Waiting Staff', null=True, blank=True, default=0)
    cuisines = MultiSelectField(choices=CUISINE, verbose_name='Cuisines', max_length=100, max_choices=30, null=True,
                                blank=True)
    amenities = MultiSelectField(choices=AMENITIES, max_length=100, max_choices=30, null=True, blank=True,
                                 verbose_name='Amenities')
    sample_type = models.CharField(verbose_name='Type', max_length=100, choices=TYPE, null=True, blank=True)
    image_1 = models.ImageField(verbose_name='Image 1', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_2 = models.ImageField(verbose_name='Image 2', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_3 = models.ImageField(verbose_name='Image 3', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_4 = models.ImageField(verbose_name='Image 4', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_5 = models.ImageField(verbose_name='Image 5', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    app_uid = models.CharField(verbose_name='App UID', max_length=200, blank=True, null=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    captured_time = models.TimeField(verbose_name='Time Captured', null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    remark = models.TextField(verbose_name='Remark', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Restaurant / Cafeteria"
        ordering = ['-id']

    def __str__(self):
        return self.name

    def branch(self):
        if self.state is not None:
            obj = State.objects.filter(name__iexact=self.state)
            if obj.exists():
                branch = obj.first().branch.name
                return branch
            else:
                return 'N/A'
        else:
            return 'N/A'

    def rating(self):
        if self.amenities is not None:
            amenities = len(self.amenities)
        else:
            amenities = 0

        if self.no_of_tables >= 20 and self.no_of_waiting_staff >= 15 and self.sample_type == 'Fine Dine' and amenities >= 2:
            return 'A'

        if self.no_of_tables >= 15 and self.no_of_waiting_staff >= 10 and amenities >= 1:
            return 'B'

        if self.no_of_tables <= 10 and self.no_of_waiting_staff <= 10 and amenities >= 0:
            return 'C'

    def username(self):
        return self.user.user.username


class Bar(models.Model):
    AMENITIES = (
        ('Dance Floor', 'Dance Floor'),
        ('Recreational Area', 'Recreational Area'),
        ('Pool Side', 'Pool Side')
    )
    FOOD_TYPE = (
        ('Nigerian', 'Nigerian'),
        ('Fast Food', 'Fast Food'),
        ('Continental', 'Continental')
    )
    TYPE = (
        ('Night Club', 'Night Club'),
        ('Lounge', 'Lounge'),
        ('Beer Parlor', 'Beer Parlor')
    )
    name = models.CharField(max_length=200, verbose_name='Name', null=True, blank=True)
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    state = models.CharField(max_length=50, verbose_name='State', null=True, blank=True)
    lga = models.CharField(max_length=100, verbose_name='LGA', null=True, blank=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=12, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    contact_name = models.CharField(verbose_name='Contact Name', max_length=200, null=True, blank=True)
    contact_phone = models.CharField(verbose_name='Contact Phone Number', max_length=12, null=True, blank=True)
    designation = models.CharField(verbose_name='Contact Designation', max_length=100, null=True, blank=True)
    no_of_tables = models.IntegerField(verbose_name='Number of Tables', null=True, blank=True, default=0)
    no_of_waiting_staff = models.IntegerField(verbose_name='Number of Waiting Staff', null=True, blank=True, default=0)
    amenities = MultiSelectField(choices=AMENITIES, max_length=100, max_choices=30, null=True, blank=True,
                                 verbose_name='Amenities')
    sample_type = models.CharField(verbose_name='Type', max_length=100, choices=TYPE, null=True, blank=True)
    food_type = MultiSelectField(choices=FOOD_TYPE, max_length=100, max_choices=30, null=True, blank=True,
                                 verbose_name='Food Type')
    image_1 = models.ImageField(verbose_name='Image 1', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_2 = models.ImageField(verbose_name='Image 2', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_3 = models.ImageField(verbose_name='Image 3', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_4 = models.ImageField(verbose_name='Image 4', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_5 = models.ImageField(verbose_name='Image 5', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    app_uid = models.CharField(verbose_name='App UID', max_length=200, blank=True, null=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    captured_time = models.TimeField(verbose_name='Time Captured', null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    remark = models.TextField(verbose_name='Remark', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Bars/Pubs/Night Clubs"
        ordering = ['-id']

    def __str__(self):
        return self.name

    def branch(self):
        if self.state is not None:
            obj = State.objects.filter(name__iexact=self.state)
            if obj.exists():
                branch = obj.first().branch.name
                return branch
            else:
                return 'N/A'
        else:
            return 'N/A'

    def rating(self):
        if self.amenities is not None:
            amenities = len(self.amenities)
        else:
            amenities = 0
        if self.no_of_tables >= 20 and self.no_of_waiting_staff >= 15 and amenities >= 2:
            return 'A'

        if self.no_of_tables >= 15 and self.no_of_waiting_staff >= 10 and amenities >= 1:
            return 'B'

        if self.no_of_tables <= 10 and self.no_of_waiting_staff <= 10 and amenities >= 0:
            return 'C'


class Cafe(models.Model):
    OFFERINGS = (
        ('Bread', 'Bread'),
        ('Pastries', 'Pastries'),
        ('Cakes', 'Cakes'),
        ('Ice Cream', 'Ice Cream'),
        ('Coffee', 'Coffee'),
        ('Beverages', 'Beverages'),
        ('Finger Food', 'Finger Food')
    )
    TYPE = (
        ('Take Away', 'Take Away'),
        ('Eat In', 'Eat In')
    )
    AMENITIES = (
        ('Banquet', 'Banquet'),
        ('Bar', 'Bar'),
        ('Kids play area', 'Kids play area')
    )
    name = models.CharField(max_length=200, verbose_name='Name', null=True, blank=True)
    address = models.TextField(verbose_name='Address', null=True, blank=True)
    state = models.CharField(max_length=50, verbose_name='State', null=True, blank=True)
    lga = models.CharField(max_length=100, verbose_name='LGA', null=True, blank=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=12, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    contact_name = models.CharField(verbose_name='Contact Name', max_length=200, null=True, blank=True)
    contact_phone = models.CharField(verbose_name='Contact Phone Number', max_length=12, null=True, blank=True)
    designation = models.CharField(verbose_name='Contact Designation', max_length=100, null=True, blank=True)
    no_of_tables = models.IntegerField(verbose_name='Number of Tables', null=True, blank=True, default=0)
    no_of_waiting_staff = models.IntegerField(verbose_name='Number of Waiting Staff', null=True, blank=True, default=0)
    showroom = models.CharField(verbose_name='Showroom', max_length=5, null=True, blank=True)
    offering = MultiSelectField(choices=OFFERINGS, max_length=100, max_choices=30, null=True, blank=True,
                                verbose_name='Food Offering')
    sample_type = models.CharField(verbose_name='Type', max_length=100, choices=TYPE, null=True, blank=True)
    amenities = MultiSelectField(choices=AMENITIES, max_length=100, max_choices=30, null=True, blank=True,
                                 verbose_name='Amenities')
    image_1 = models.ImageField(verbose_name='Image 1', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_2 = models.ImageField(verbose_name='Image 2', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_3 = models.ImageField(verbose_name='Image 3', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_4 = models.ImageField(verbose_name='Image 4', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    image_5 = models.ImageField(verbose_name='Image 5', default='horeca/images/noimage.jpg', blank=True,
                                upload_to='horeca/images/')
    app_uid = models.CharField(verbose_name='App UID', max_length=200, blank=True, null=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    captured_time = models.TimeField(verbose_name='Time Captured', null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    remark = models.TextField(verbose_name='Remark', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Bakery/Confectionery/Cafe"
        ordering = ['-id']

    def __str__(self):
        return self.name

    def branch(self):
        if self.state is not None:
            obj = State.objects.filter(name__iexact=self.state)
            if obj.exists():
                branch = obj.first().branch.name
                return branch
            else:
                return 'N/A'
        else:
            return 'N/A'

    def rating(self):
        if self.amenities is not None:
            amenities = len(self.amenities)
        else:
            amenities = 0
        if self.offering is not None:
            offering = len(self.offering)
        else:
            offering = 0

        if self.no_of_tables >= 20 and self.no_of_waiting_staff >= 15 and amenities >= 2 and offering >= 5:
            return 'A'

        if self.no_of_tables >= 15 and self.no_of_waiting_staff >= 10 and amenities >= 1 and offering >= 5:
            return 'B'

        if self.no_of_tables <= 10 and self.no_of_waiting_staff <= 10 and amenities >= 0 and offering >= 3:
            return 'C'


class KelloggsRetail(models.Model):
    CHOICE_ONE = (
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('N/A', 'N/A')
    )
    TYPE = (
        ('Post_Sampling', 'Post_Sampling'),
        ('Pre_Sampling', 'Pre_Sampling')
    )
    BRANCHES = (
        ('Central', 'Central'),
        ('East 1', 'East 1'),
        ('East 2', 'East 2'),
        ('East 3', 'East 3'),
        ('East 4', 'East 4'),
        ('East 5', 'East 5'),
        ('East 6', 'East 6'),
        ('Lagos 1', 'Lagos 1'),
        ('Lagos 2', 'Lagos 2'),
        ('North 1', 'North 1'),
        ('North 2', 'North 2'),
        ('North 3', 'North 3'),
        ('South Central', 'South Central'),
        ('South West', 'South West')
    )
    name = models.CharField(max_length=100, verbose_name='Name of Outlet', blank=True, null=True)
    lga = models.CharField(max_length=100, verbose_name='LGA', blank=True, null=True)
    address = models.CharField(max_length=300, verbose_name='Address', blank=True, null=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=12, null=True, blank=True)
    kelloggs_available = models.CharField(max_length=20, verbose_name='Kellogg Available', choices=CHOICE_ONE,
                                          default='N/A', null=True, blank=True)
    sku = models.CharField(max_length=200, verbose_name='SKU', null=True, blank=True)
    knows_kelloggs = models.CharField(max_length=20, verbose_name='Do You Know Kelloggs', choices=CHOICE_ONE,
                                      default='N/A', null=True, blank=True)
    knows_coco_pops = models.CharField(max_length=20, verbose_name='Do You Know Kelloggs Coco Pops', choices=CHOICE_ONE,
                                       default='N/A', null=True, blank=True)
    carton_sales = models.FloatField(default=0.0, verbose_name='Weekly Carton Sales', null=True, blank=True)
    consumes_at_home = models.CharField(max_length=20, verbose_name='Consumes Kelloggs At Home', choices=CHOICE_ONE,
                                        default='N/A', null=True, blank=True)
    sachet_selling_price = models.FloatField(verbose_name='Selling Price Per Sachet', default=0.0, null=True,
                                             blank=True)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    sampling_type = models.CharField(max_length=100, verbose_name='Sampling Type', choices=TYPE, null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    branch = models.CharField(max_length=100, verbose_name='Branch', choices=BRANCHES, null=True, blank=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Kelloggs Retail"
        ordering = ['-id']

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'No Name'


class KelloggsPreSampling(models.Model):
    CHOICE_ONE = (
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('N/A', 'N/A')
    )
    BRANCHES = (
        ('Central', 'Central'),
        ('East 1', 'East 1'),
        ('East 2', 'East 2'),
        ('East 3', 'East 3'),
        ('East 4', 'East 4'),
        ('East 5', 'East 5'),
        ('East 6', 'East 6'),
        ('Lagos 1', 'Lagos 1'),
        ('Lagos 2', 'Lagos 2'),
        ('North 1', 'North 1'),
        ('North 2', 'North 2'),
        ('North 3', 'North 3'),
        ('South Central', 'South Central'),
        ('South West', 'South West')
    )
    name = models.CharField(max_length=100, verbose_name='Name', blank=True, null=True)
    lga = models.CharField(max_length=100, verbose_name='LGA', blank=True, null=True)
    address = models.CharField(max_length=300, verbose_name='Address', blank=True, null=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=12, null=True, blank=True)
    knows_kelloggs = models.CharField(max_length=20, verbose_name='Knows Kelloggs', choices=CHOICE_ONE, default='N/A',
                                      null=True,
                                      blank=True)
    knows_coco_pops = models.CharField(max_length=20, verbose_name='Knows Kelloggs Coco Pops', choices=CHOICE_ONE,
                                       default='N/A', null=True, blank=True)
    coco_pops_sachet_seen = models.CharField(max_length=20, verbose_name='Coco Pops Sachet Seen', choices=CHOICE_ONE,
                                             default='N/A', null=True, blank=True)
    eats_coco_pops = models.CharField(max_length=20, verbose_name='Consumes Kelloggs Coco Pops', choices=CHOICE_ONE,
                                      default='N/A', null=True, blank=True)
    consumption_rate = models.CharField(max_length=120, verbose_name='Comsumption Rate', null=True, blank=True)
    consumption_style = models.TextField(max_length=700, verbose_name='Consumption Style', null=True, blank=True)
    consumption_time = models.CharField(max_length=200, verbose_name='Consumption Time', null=True, blank=True)
    as_kids_breakfast = models.CharField(max_length=20, verbose_name='Given to Kids as Breakfast', choices=CHOICE_ONE,
                                         default='N/A', null=True, blank=True)
    preferred_as_kids_breakfast = models.CharField(max_length=20, verbose_name='Preferred as Kids Breakfast',
                                                   choices=CHOICE_ONE, default='N/A', null=True, blank=True)
    preferred_kids_breakfast = models.CharField(max_length=600, verbose_name='Preferred Kids Breakfast', null=True,
                                                blank=True)
    preferred_adult_breakfast = models.CharField(max_length=600, verbose_name='Preferred Adult Breakfast', null=True,
                                                 blank=True)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    branch = models.CharField(max_length=100, verbose_name='Branch', choices=BRANCHES, null=True, blank=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Kelloggs Pre Sampling"
        ordering = ['-id']

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'No Name'


class KelloggsPostSampling(models.Model):
    CHOICE_ONE = (
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('N/A', 'N/A')
    )
    BRANCHES = (
        ('Central', 'Central'),
        ('East 1', 'East 1'),
        ('East 2', 'East 2'),
        ('East 3', 'East 3'),
        ('East 4', 'East 4'),
        ('East 5', 'East 5'),
        ('East 6', 'East 6'),
        ('Lagos 1', 'Lagos 1'),
        ('Lagos 2', 'Lagos 2'),
        ('North 1', 'North 1'),
        ('North 2', 'North 2'),
        ('North 3', 'North 3'),
        ('South Central', 'South Central'),
        ('South West', 'South West')
    )
    name = models.CharField(max_length=100, verbose_name='Name', blank=True, null=True)
    lga = models.CharField(max_length=100, verbose_name='LGA', blank=True, null=True)
    address = models.CharField(max_length=300, verbose_name='Address', blank=True, null=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=12, null=True, blank=True)
    knows_kelloggs = models.CharField(max_length=20, verbose_name='Knows Kelloggs', choices=CHOICE_ONE, default='N/A',
                                      null=True,
                                      blank=True)
    knows_coco_pops = models.CharField(max_length=20, verbose_name='Knows Kelloggs Coco Pops', choices=CHOICE_ONE,
                                       default='N/A',
                                       null=True, blank=True)
    coco_pops_sachet_seen = models.CharField(max_length=20, verbose_name='Coco Pops Sachet Seen', choices=CHOICE_ONE,
                                             default='N/A',
                                             null=True, blank=True)
    known_from = models.TextField(max_length=700, verbose_name='Known From', null=True, blank=True)
    eats_coco_pops = models.CharField(max_length=20, verbose_name='Consumes Kelloggs Coco Pops', choices=CHOICE_ONE,
                                      default='N/A',
                                      null=True, blank=True)
    consumption_rate = models.CharField(max_length=120, verbose_name='Comsumption Rate', null=True, blank=True)
    consumption_style = models.TextField(max_length=700, verbose_name='Consumption Style', null=True, blank=True)
    consumption_time = models.CharField(max_length=200, verbose_name='Consumption Time', null=True, blank=True)
    as_kids_breakfast = models.CharField(max_length=20, verbose_name='Given to Kids as Breakfast', choices=CHOICE_ONE,
                                         default='N/A',
                                         null=True, blank=True)
    preferred_as_kids_breakfast = models.CharField(max_length=20, verbose_name='Preferred as Kids Breakfast',
                                                   choices=CHOICE_ONE, default='N/A', null=True, blank=True)
    preferred_kids_breakfast = models.CharField(max_length=600, verbose_name='Preferred Kids Breakfast', null=True,
                                                blank=True)
    preferred_adult_breakfast = models.CharField(max_length=600, verbose_name='Preferred Adult Breakfast', null=True,
                                                 blank=True)
    kids_requested = models.CharField(max_length=20, verbose_name='Kids Requested Coco Pos for Breakfast',
                                      choices=CHOICE_ONE, default='N/A', null=True, blank=True)
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True)
    branch = models.CharField(max_length=100, verbose_name='Branch', choices=BRANCHES, null=True, blank=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Kelloggs Post Sampling"
        ordering = ['-id']

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'No Name'


class KelloggsSchool(models.Model):
    LEVEL = (
        ('Nursery', 'Nursery'),
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('Nursery - Primary', 'Nursery - Primary'),
        ('Nursery - Secondary', 'Nursery - Secondary'),
        ('Primary - Secondary', 'Primary - Secondary'),
        ('Secondary School', 'Secondary School'),
        ('Creche/Nursery/Primary/Secondary', 'Creche/Nursery/Primary/Secondary'),
    )
    TARGET_LEVEL = (
        ('Nursery', 'Nursery'),
        ('Primary', 'Primary'),
        ('Nursery & Primary', 'Nursery & Primary'),
        ('Junior Secondary', 'Junior Secondary'),
        ('Senior Secondary', 'Senior Secondary'),
        ('Junior & Senior Secondary', 'Junior & Senior Secondary'),
        ('Creche', 'Creche'),
        ('Kindergarten', 'Kindergarten')
    )
    TYPE = (
        ('Government', 'Government'),
        ('Private', 'Private'),
    )

    name = models.CharField(max_length=200, verbose_name='School Name', blank=True, null=True)
    school_type = models.CharField(max_length=100, verbose_name='School Type', choices=TYPE, null=True, blank=True)
    visited = models.BooleanField(default=False, verbose_name='Visited')
    address = models.CharField(max_length=200, verbose_name='Address', null=True, blank=True)
    landmark = models.CharField(max_length=200, verbose_name='Landmark', null=True, blank=True)
    designation = models.CharField(max_length=200, verbose_name='Designation', null=True, blank=True)
    state = models.CharField(max_length=50, verbose_name='State', null=True, blank=True)
    lga = models.CharField(max_length=100, verbose_name='LGA', null=True, blank=True)
    lat = models.FloatField(verbose_name='Latitude', default=0.0, null=True, blank=True)
    lng = models.FloatField(verbose_name='Longitude', default=0.0, null=True, blank=True)
    contact_name = models.CharField(verbose_name='Contact Person', max_length=200, null=True, blank=True)
    contact_phone = models.CharField(verbose_name='Contact Phone Number', max_length=20, null=True, blank=True)
    school_phone = models.CharField(verbose_name='School Phone Number', max_length=20, null=True, blank=True)
    level = models.CharField(verbose_name='Level', max_length=100, choices=LEVEL, null=True, blank=True)
    target_level = models.CharField(verbose_name='Target Level', max_length=100, choices=TARGET_LEVEL, null=True)
    population = models.IntegerField(verbose_name='Total Population', default=0, blank=True)
    target_population = models.IntegerField(verbose_name='Target Population', default=0, null=True)
    sampled_population = models.IntegerField(verbose_name='Sampled Population', default=0, null=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)
    school_image = models.ImageField(verbose_name='School Image', default='kelloggs/images/noimage.jpg', null=True,
                                     blank=True, upload_to='kelloggs/images/')
    feedback_form = models.ImageField(verbose_name='Feedback Form', default='kelloggs/images/noimage.jpg', null=True,
                                      blank=True, upload_to='kelloggs/images/')
    mc_video = models.FileField(verbose_name='MC Video', blank=True, null=True, upload_to='kelloggs/videos/')
    students_sc_img = models.ImageField(verbose_name='Students With Cups and Sachets Image', blank=True, null=True,
                                        upload_to='kelloggs/images/', default='kelloggs/images/noimage.jpg')
    students_uc_img = models.ImageField(verbose_name='Students With Uncle Coco', blank=True, null=True,
                                        upload_to='kelloggs/images/', default='kelloggs/images/noimage.jpg')
    date_captured = models.DateField(verbose_name='Date Captured', null=True, blank=True)
    app_uid = models.CharField(verbose_name='App UID', null=True, blank=True, max_length=200)
    mc_name = models.CharField(max_length=200, verbose_name='MC Name', blank=True, null=True)
    branch = models.CharField(max_length=200, verbose_name='Branch', blank=True, null=True)
    visit_start_time = models.TimeField(verbose_name='Visit Start Time', null=True, blank=True)
    visit_end_time = models.TimeField(verbose_name='Visit End Time', null=True, blank=True)
    visit_start_date = models.DateField(verbose_name='Visit Start Date', null=True, blank=True)
    visit_end_date = models.DateField(verbose_name='Visit End Date', null=True, blank=True)
    final_lat = models.FloatField(verbose_name='Final Latitude', default=0.0, null=True)
    final_lng = models.FloatField(verbose_name='Final Longitude', default=0.0, null=True)
    cocopops_32g_qty = models.FloatField(verbose_name='Coco Pops 32g', default=0.0, blank=True, null=True)
    cocopops_450g_qty = models.FloatField(verbose_name='Coco Pops 450g', default=0.0, blank=True, null=True)
    dano_cool_cow_25g_qty = models.FloatField(verbose_name='Dano Cool Cow 25g', default=0.0, blank=True, null=True)
    dano_cool_cow_360g_qty = models.FloatField(verbose_name='Dano Cool Cow 360g', default=0.0, blank=True, null=True)
    total_population = models.FloatField(verbose_name='Total Population', default=0.0, blank=True, null=True)
    lunch_box = models.FloatField(verbose_name='Lunch Box', default=0.0, blank=True, null=True)
    lunch_box_kelloggs = models.FloatField(verbose_name='Lunch Box Kelloggs', default=0.0, blank=True, null=True)
    approved = models.BooleanField(verbose_name='Approved', default=False)

    class Meta:
        verbose_name_plural = "Kelloggs School"
        ordering = ['-id']

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'No Name'

    def username(self):
        if self.user:
            return self.user.user.username
        else:
            return 'None'

    def supervisor(self):
        if self.user.supervisor:
            return self.user.supervisor.user.username
        else:
            return 'None'

    def duration(self):
        if self.visit_end_date and self.visit_end_time and self.visit_start_date and self.visit_start_time:
            main_dpt = datetime.strptime(str(self.visit_start_date) + str(self.visit_start_time), "%Y-%m-%d%H:%M:%S")
            main_dpt2 = datetime.strptime(str(self.visit_end_date) + str(self.visit_end_time), "%Y-%m-%d%H:%M:%S")
            return (main_dpt2 - main_dpt).seconds
        else:
            return 0


class SNTrash(models.Model):
    serial_number = models.CharField(max_length=200, verbose_name='Serial Number', blank=True, null=True)
    user = models.ForeignKey(UserProfile, verbose_name='User', null=True, blank=True)
    date = models.DateTimeField(verbose_name='Date Deleted', auto_created=True, auto_now_add=True, null=True,
                                blank=True)

    class Meta:
        verbose_name_plural = "Serial Numbers Trash"
        ordering = ['-id']

    def __str__(self):
        if self.serial_number is not None:
            return self.serial_number
        else:
            return 'No Name'

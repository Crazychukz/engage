# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


admin.site.register(UserProfile)
admin.site.register(School)
admin.site.register(Hypo)
admin.site.register(UserModules)
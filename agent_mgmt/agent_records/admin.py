from django.contrib import admin
from .models import (Agent, Team, Site, Channel, Skill, Rank, AgentAssignment, Shift, Schedule, Break, Company,
                     HiringClass, AgentScore, AgentScoreType, SkillAssignment)
from reversion.admin import VersionAdmin


@admin.register(Agent)
class AgentAdmin(VersionAdmin):
    fieldsets = [
        ('Basics', {'fields': ['first_name', 'last_name', 'email_address']}),
        ('Employment Attributes', {'fields': ['is_supervisor', 'is_active',
                                              'hire_date', 'termination_date', 'rank', 'pay_rate']}),
    ]
    list_display = ('first_name', 'last_name', 'email_address', 'rank',
                    'is_supervisor', 'is_active', 'hire_date',
                    'termination_date', 'pay_rate')


@admin.register(Team)
class TeamAdmin(VersionAdmin):
    list_display = ('full_name', 'short_name', 'supervisor', 'primary_site')


@admin.register(Site)
class SiteAdmin(VersionAdmin):
    list_display = ('common_name', 'short_name', 'city', 'state', 'country', 'site_manager')


@admin.register(Channel)
class ChannelAdmin(VersionAdmin):
    list_display = ('name', 'vendor_name')


@admin.register(Schedule)
class ScheduleAdmin(VersionAdmin):
    list_display = ('monday_shift', 'tuesday_shift', 'wednesday_shift', 'thursday_shift', 'friday_shift',
                    'saturday_shift', 'sunday_shift')


@admin.register(SkillAssignment)
class SkillAssignmentAdmin(VersionAdmin):
    list_display = ('agent', 'skill', 'level', 'assigned_date', 'expiration_date', 'is_active')


@admin.register(HiringClass)
class HiringClassAdmin(VersionAdmin):
    list_display = ('name', 'start_date', 'live_date', 'hiring_team')


model_list = [Skill, Rank, AgentAssignment, Shift, Break, Company, AgentScore, AgentScoreType]

for model in model_list:
    admin.site.register(model)

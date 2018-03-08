from django.contrib import admin

from .models import Agent, Team, Site, Channel, Skill, Rank, AgentAssignment

model_list = [Agent, Team, Site, Channel, Skill, Rank, AgentAssignment]

for model in model_list:
    admin.site.register(model)

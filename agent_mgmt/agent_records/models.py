from django.db import models
from treebeard import ns_tree


class Agent(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email_address = models.CharField(max_length=255)
    is_supervisor = models.BooleanField()
    is_active = models.BooleanField()
    hire_date = models.DateField()
    termination_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Team(ns_tree.NS_Node):
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    supervisor = models.ForeignKey(Agent,
                                   on_delete=models.PROTECT,
                                   limit_choices_to={'is_supervisor': True},
                                   )
    def __str__(self):
        return self.full_name


class Site(models.Model):
    common_name = models.CharField(max_length=35)
    short_name = models.CharField(max_length=5)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    country = models.CharField(max_length=35)
    site_manager = models.ForeignKey(Agent,
                                     on_delete=models.PROTECT,
                                     limit_choices_to={'is_supervisor': True},
                                     )

    def __str__(self):
        return self.common_name


class Channel(models.Model):
    name = models.CharField(max_length=35)
    vendor_name = models.CharField(max_length=35)

    def __str__(self):
        return self.name


class Skill(models.Model):
    full_name = models.CharField(max_length=50)
    channel = models.ForeignKey(Channel,
                                on_delete=models.PROTECT,
                                )
    has_levels = models.BooleanField()

    def __str__(self):
        return self.full_name


class Rank(models.Model):
    title = models.CharField(max_length=50)
    value = models.PositiveSmallIntegerField()
    can_supervise = models.BooleanField()

    def __str__(self):
        return self.title


class AgentAssignment(models.Model):
    agent = models.ForeignKey(Agent,
                              on_delete=models.PROTECT,
                              )
    team = models.ForeignKey(Team,
                             on_delete=models.PROTECT,
                             )

    def __str__(self):
        return self.agent + ' is assigned to ' + self.team

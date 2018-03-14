from django.db import models
#from treebeard import ns_tree


class Rank(models.Model):
    title = models.CharField(max_length=50)
    value = models.PositiveSmallIntegerField()
    can_supervise = models.BooleanField()

    def __str__(self):
        return self.title


class Agent(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email_address = models.CharField(max_length=255)
    is_supervisor = models.BooleanField()
    is_active = models.BooleanField()
    hire_date = models.DateField()
    termination_date = models.DateField(blank=True, null=True)
    pay_rate = models.DecimalField(decimal_places=2, max_digits=8,
                                   blank=True, null=True)
    rank = models.ForeignKey(Rank,
                             on_delete=models.PROTECT,
                             #null=True, #temporary so the thing doesn't yell
                             )
    hiring_class = models.ForeignKey(HiringClass,
                                     blank=True,
                                     null=True,
                                     )

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class HiringClass(models.Model):
    name = models.CharField(max_length=35)
    start_date = models.DateField()
    live_date = models.DateField()
    hiring_team = models.ForeignKey(Team,
                                    on_delete=models.PROTECT,
                                    )

    def __str__(self):
        return self.name


class Site(models.Model):
    common_name = models.CharField(max_length=35)
    short_name = models.CharField(max_length=5)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    country = models.CharField(max_length=35)
    operating_company = models.ForeignKey(Company,
                                          on_delete=models.PROTECT,
                                          )
    site_manager = models.ForeignKey(Agent,
                                     on_delete=models.PROTECT,
                                     limit_choices_to={'is_supervisor': True,
                                                       'is_active': True},
                                     )

    def __str__(self):
        return self.common_name


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Team(models.Model):
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    supervisor = models.ForeignKey(Agent,
                                   on_delete=models.PROTECT,
                                   limit_choices_to={'is_supervisor': True,
                                                     'is_active': True},
                                   )
    primary_site = models.ForeignKey(Site,
                                     on_delete=models.PROTECT,
                                     )

    parent_team = models.ForeignKey(Team,
                                    on_delete=models.PROTECT,
                                    blank=True,
                                    null=True,
                                    )


    def __str__(self):
        return self.full_name


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
    external_id = models.PositiveIntegerField(blank=True,
                                              null=True,
                                              )

    def __str__(self):
        return self.full_name


class SkillAssignment(models.Model):
    agent = models.ForeignKey(Agent,
                              on_delete=models.PROTECT,
                              )
    skill = models.ForeignKey(Skill,
                              on_delete=models.PROTECT,
                              )
    level = models.PositiveIntegerField(blank=True,
                                        null=True,
                                        )
    assigned_date = models.DateField(blank=True,
                                     null=True,
                                     )
    expiration_date = models.DateField(blank=True,
                                       null=True,
                                       )
    is_active = models.BooleanField(blank=True,
                                    null=True,
                                    )

    class Meta:
        unique_together = ('agent', 'skill')

    def __str__(self):
        return self.agent.__str__() + ' has skill ' + self.skill.__str__()


class Shift(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('start_time', 'end_time')

    def __str__(self):
        return self.start_time.__str__() + ' to ' + self.end_time.__str__()


class Break(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('start_time', 'end_time')

    def __str__(self):
        return self.start_time.__str__() + ' to ' + self.end_time.__str__()


class Schedule(models.Model):
    name = models.CharField(max_length=50)
    monday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT,
                                     related_name='2idddw+'
                                     )
    tuesday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT, related_name='jdje+'
                                     )
    wednesday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT,
                                        related_name='job23+',
                                     )
    thursday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT,
                                       related_name='2j4i+'
                                     )
    friday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT,
                                     related_name='23irij+'

                                     )
    saturday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT,
                                       related_name='ij2ijid+'
                                     )
    sunday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT,
                                     related_name=
                                     '2j409i0+'
                                     )

    class Meta:
        unique_together = ('monday_shift', 'tuesday_shift', 'wednesday_shift', 'thursday_shift', 'friday_shift',
                           'saturday_shift', 'sunday_shift')

    def __str__(self):
        return self.name


class AgentAssignment(models.Model):
    agent = models.ForeignKey(Agent,
                              on_delete=models.PROTECT,
                              )
    team = models.ForeignKey(Team,
                             on_delete=models.PROTECT,
                             )
    site = models.ForeignKey(Site,
                             on_delete=models.PROTECT,
                             )
    schedule = models.ForeignKey(Schedule,
                                 on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(blank=True,
                                null=True,
                                )
    is_active = models.BooleanField(blank=True,
                                    null=True,
                                    )

    def __str__(self):
        return self.agent.__str__() + ' is assigned to ' + self.team.__str__()


class AgentScoreType(models.Model):
    name = models.CharField(max_length=35)
    related_channel = models.ForeignKey(Channel,
                                        on_delete=models.PROTECT,
                                        blank=True,
                                        null=True,
                                        )

    def __str__(self):
        return self.name.__str__()


class AgentScore(models.Model):
    agent = models.ForeignKey(Agent,
                              on_delete=models.PROTECT,
                              )
    score = models.FloatField()

    def __str__(self):
        return self.agent.__str__() + ' has score ' + self.score.__str__()











from django.db import models


class Rank(models.Model):
    title = models.CharField(max_length=50,
                             unique=True,
                             )
    value = models.PositiveSmallIntegerField()
    can_supervise = models.BooleanField()

    def __str__(self):
        return self.title


class Agent(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email_address = models.CharField(max_length=255,
                                     unique=True,
                                     )
    is_supervisor = models.BooleanField()
    is_active = models.BooleanField()
    hire_date = models.DateField()
    termination_date = models.DateField(blank=True, null=True)
    pay_rate = models.DecimalField(decimal_places=2, max_digits=8,
                                   blank=True, null=True)
    rank = models.ForeignKey(Rank,
                             on_delete=models.PROTECT,
                             )
    hiring_class = models.ForeignKey("HiringClass",
                                     on_delete=models.PROTECT,
                                     blank=True,
                                     null=True,
                                     )

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class HiringClass(models.Model):
    name = models.CharField(max_length=35,
                            unique=True,
                            )
    start_date = models.DateField()
    live_date = models.DateField()
    hiring_team = models.ForeignKey("Team",
                                    on_delete=models.PROTECT,
                                    )

    def __str__(self):
        return self.name


class Site(models.Model):
    common_name = models.CharField(max_length=35,
                                   unique=True,
                                   )
    short_name = models.CharField(max_length=5,
                                  unique=True,
                                  )
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    country = models.CharField(max_length=35)
    operating_company = models.ForeignKey("Company",
                                          on_delete=models.PROTECT,
                                          null=True,
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
    full_name = models.CharField(max_length=100,
                                 unique=True,
                                 )
    short_name = models.CharField(max_length=20,
                                  unique=True,
                                  )
    supervisor = models.ForeignKey(Agent,
                                   on_delete=models.PROTECT,
                                   limit_choices_to={'is_supervisor': True,
                                                     'is_active': True},
                                   )
    primary_site = models.ForeignKey(Site,
                                     on_delete=models.PROTECT,
                                     )

    parent_team = models.ForeignKey("Team",
                                    on_delete=models.PROTECT,
                                    blank=True,
                                    null=True,
                                    )

    def __str__(self):
        return self.full_name


class Channel(models.Model):
    name = models.CharField(max_length=35,
                            unique=True,
                            )
    vendor_name = models.CharField(max_length=35,
                                   )

    def __str__(self):
        return self.name


class Skill(models.Model):
    full_name = models.CharField(max_length=50,
                                 unique=True,
                                 )
    channel = models.ForeignKey(Channel,
                                on_delete=models.PROTECT,
                                )
    has_levels = models.BooleanField()
    external_id = models.PositiveIntegerField(blank=True,
                                              null=True,
                                              )

    def __str__(self):
        return self.channel + ' - ' + self.full_name


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
    is_active = models.NullBooleanField(blank=True,
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
    name = models.CharField(max_length=50,
                            unique=True,
                            )
    monday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT,
                                     related_name='schedule_monday_shifts',
                                     blank=True,
                                     null=True,
                                     )
    tuesday_shift = models.ForeignKey(Shift,
                                      on_delete=models.PROTECT,
                                      related_name='schedule_tuesday_shifts',
                                      blank=True,
                                      null=True,
                                      )
    wednesday_shift = models.ForeignKey(Shift,
                                        on_delete=models.PROTECT,
                                        related_name='schedule_wednesday_shifts',
                                        blank=True,
                                        null=True,
                                        )
    thursday_shift = models.ForeignKey(Shift,
                                       on_delete=models.PROTECT,
                                       related_name='schedule_thursday_shifts',
                                       blank=True,
                                       null=True,
                                       )
    friday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT,
                                     related_name='schedule_friday_shifts',
                                     blank=True,
                                     null=True,
                                     )
    saturday_shift = models.ForeignKey(Shift,
                                       on_delete=models.PROTECT,
                                       related_name='schedule_saturday_shifts',
                                       blank=True,
                                       null=True,
                                       )
    sunday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT,
                                     related_name='schedule_sunday_shifts',
                                     blank=True,
                                     null=True,
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
    is_active = models.NullBooleanField(blank=True,
                                        )

    def __str__(self):
        return self.agent.__str__() + ' is assigned to ' + self.team.__str__()


class AgentScoreType(models.Model):
    name = models.CharField(max_length=35,
                            unique=True,
                            )
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
    score_type = models.ForeignKey(AgentScoreType,
                                   on_delete=models.PROTECT,
                                   blank=False,
                                   null=False
                                   )
    score = models.FloatField()

    def __str__(self):
        return self.agent.__str__() + ' has score ' + self.score.__str__()

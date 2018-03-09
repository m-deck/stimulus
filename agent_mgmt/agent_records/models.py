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

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Site(models.Model):
    common_name = models.CharField(max_length=35)
    short_name = models.CharField(max_length=5)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    country = models.CharField(max_length=35)
    site_manager = models.ForeignKey(Agent,
                                     on_delete=models.PROTECT,
                                     limit_choices_to={'is_supervisor': True,
                                                       'is_active': True},
                                     )

    def __str__(self):
        return self.common_name


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

    def __str__(self):        return self.agent.__str__() + ' has skill ' + self.skill.__str__()


class Shift(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.start_time.__str__() + ' to ' + self.end_time.__str__()


class Break(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.start_time.__str__() + ' to ' + self.end_time.__str__()


class Schedule(models.Model):
    monday_shift = models.ForeignKey(Shift,
                                     on_delete=models.PROTECT, related_name='2idddw+'
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
    monday_break1 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='2ijdgre+')
    monday_break2 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='ijd0sk0+')
    monday_break3 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='249-9d-us+')
    monday_break4 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='aosidnf+')
    tuesday_break1 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='0283nds+')
    tuesday_break2 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='3838gf+')
    tuesday_break3 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='2083hdd+')
    tuesday_break4 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='308h0h4+')
    wednesday_break1 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='280h0h8d+')
    wednesday_break2 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='weihd+')
    wednesday_break3 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='2sdh2jd9+')
    wednesday_break4 = models.ForeignKey(Break, on_delete=models.PROTECT, related_name='20824089dh8+')
    #thursday_break1 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #thursday_break2 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #thursday_break3 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #thursday_break4 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #friday_break1 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #friday_break2 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #friday_break3 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #friday_break4 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #saturday_break1 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #saturday_break2 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #saturday_break3 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #saturday_break4 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #sunday_break1 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #sunday_break2 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #sunday_break3 = models.ForeignKey(Break, on_delete=models.PROTECT,)
    #sunday_break4 = models.ForeignKey(Break, on_delete=models.PROTECT,)


class AgentAssignment(models.Model):
    agent = models.OneToOneField(Agent,
                                 on_delete=models.PROTECT,
                                 )
    team = models.ForeignKey(Team,
                             on_delete=models.PROTECT,
                             )
    site = models.ForeignKey(Site,
                             on_delete=models.PROTECT,
                             )
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)

    def __str__(self):
        return self.agent.__str__() + ' is assigned to ' + self.team.__str__()










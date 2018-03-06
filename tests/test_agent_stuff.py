import pytest
from .. import stimulus


def test_agent_creation():
    agent = stimulus.Agent(None) #uses None as schedule
    assert isinstance(agent.id, int) and agent.status == 'logged_off' and not agent.active_call and agent.handling_call is None and isinstance(agent.schedule, object) 


def test_agent_schedule_creation():
    a_s = stimulus.AgentSchedule()
    assert isinstance(a_s.id, int) and 0 <= a_s.regular_start <= 86400 and 0 <= a_s.regular_end <= 86400 and 0 <= a_s.regular_lunch <= 86400 and 0 <= a_s.lunch_duration <= 86400 and isinstance(a_s.tz, str) 


def test_agent_list_creation():
    agent_list = []

    schedule1 = stimulus.AgentSchedule(regular_start=10000, regular_end=20000, regular_lunch=15000, work_days=[2,3,4,5])
    schedule2 = stimulus.AgentSchedule(regular_start=12000, regular_end=22000, regular_lunch=17000, work_days=[3,4,5,6])

    schedule_list = [schedule1, schedule2]
    schedule_allocations = [4,7]

    for x, y in zip(schedule_allocations, schedule_list):
        for i in range(0,x):
            agent_list.append(stimulus.Agent(y))

    assert isinstance(agent_list[0], stimulus.Agent) and isinstance(agent_list[1], stimulus.Agent)



import pytest
from .. import stimulus


def test_agent_creation():
    agent = stimulus.Agent(None) #uses None as schedule
    assert isinstance(agent.id, int) and agent.status == 'logged_off' and not agent.active_call and agent.handling_call is None and isinstance(agent.schedule, object) 

def test_agent_schedule_creation():
    a_s = stimulus.AgentSchedule()
    assert isinstance(a_s.id, int) and 0 <= a_s.regular_start <= 86400 and 0 <= a_s.regular_end <= 86400 and 0 <= a_s.regular_lunch <= 86400 and 0 <= a_s.lunch_duration <= 86400 and isinstance(a_s.tz, str) 


from .. import stimulus
import random


def test_single_day_simulation():

    agent1_schedule = stimulus.AgentSchedule()
    agent2_schedule = stimulus.AgentSchedule(regular_start=30600, regular_end=(3600*16.5 + 1800), regular_lunch=(3600*12 + 1800))

    agent1 = stimulus.Agent(agent1_schedule)
    agent2 = stimulus.Agent(agent2_schedule)
    agent3 = stimulus.Agent(agent1_schedule)

    call_durations = random.sample(range(100,500), 200)
    arrival_times = random.sample(range(28800,32000), 200)

    calls_list = []

    for arr, dur in zip(arrival_times, call_durations):
        calls_list.append(stimulus.Call(arr,dur))

    day1 = stimulus.Day(agents=[agent1, agent2, agent3], calls=calls_list)
    aban_dist = [(1800, .999)]

    simulated_day = stimulus.simulate_day(day=day1, abandon_dist=aban_dist)

    assert 0 <= simulated_day.service_level() <= 1 and simulated_day.aht() >= 0 and isinstance(simulated_day, stimulus.Day)


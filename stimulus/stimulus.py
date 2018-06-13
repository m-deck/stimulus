import random
import time
import pandas as pd
from .utils import secs_to_time
from pprint import pprint
import copy


class Queue(object):
    """
    A generic queue object.
    """
    _ID = 0

    def __init__(self):
        self.id = self._ID
        self.__class__._ID += 1
        self.contents = []


class FIFOQueue(Queue):
    """
    A FIFO queue. Inherits from / subclass of Queue.
    """
    def __init__(self):
        super(FIFOQueue, self).__init__()
        self.priority = 1


class SearchQueue(Queue):
    """
    A search-type queue. Inherits from Queue.
    """
    def __init__(self):
        super(SearchQueue, self).__init__()


class ServiceDesk(object):
    _ID = 0

    def __init__(self, agents):
        self.id = self._ID
        self.__class__._ID += 1
        self.agents = agents
        self.previously_logged_on_agents = []


class Site(object):
    _ID = 0

    def __init__(self, name):
        self.id = self._ID
        self.__class__._ID += 1
        self.name = name
        self.tz = None


class Schedule(object):
    _ID = 0

    def __init__(self):
        self.id = self._ID
        self.__class__._ID += 1

# eventually, AgentSchedule should inherit from this class??
# the idea is to also have Schedules be possible for Queues.
# should Queues just have a regular schedule or do they need a
# QueueSchedule object??


class Agent(object):
    _ID = 0

    def __init__(self, schedule):  # maybe schedule shouldn't be required for agent to simply exist...
        self.id = self._ID; self.__class__._ID += 1
        self.schedule = schedule
        self.status = 'logged_off'
        self.last_status = 'initialized'
        self.time_in_status = 0
        self.active_call = False
        self.previously_active = False
        self.handling_call = None
        self.outbound_reserved = False
        self.previously_outbound = False
        self.skills = []

    def reset(self):
        self.status = 'logged_off'
        self.last_status = 'initialized'
        self.time_in_status = 0
        self.active_call = False
        self.previously_active = False
        self.handling_call = None
        self.outbound_reserved = False
        self.previously_outbound = False


class AgentSchedule(object):
    _ID = 0

    def __init__(self, regular_start=28800, regular_end=(3600*16.5), regular_lunch=(3600*12), lunch_duration=1800, tz='America/Chicago', work_days=[1,2,3,4,5]):
        self.id = self._ID; self.__class__._ID += 1
        self.regular_start = regular_start
        self.regular_end = regular_end
        self.regular_lunch = regular_lunch
        self.lunch_duration = lunch_duration
        self.tz = tz
        self.work_days = work_days
        self.site = None


class Interval(object):
    _ID = 0

    def __init__(self, stamp, calls):
        self.id = self._ID
        self.__class__._ID += 1
        self.stamp = stamp
        self.calls = calls
        self.sl_threshold = 20
        self.sl_target = 0.90
        self.interval = 15 * 60  # 15 minutes

        self.calls_offered = 0
        self.calls_answered = 0
        self.calls_handled = 0
        self.total_calls_aband = 0
        self.sum_handle_time = 0

        self.service_level_calls = 0
        self.service_level_calls_offered = 0
        self.service_level_aband = 0

        self.optimized = False
        self.agents_count = 50  # Agents count to start search from

        self.previously_active_calls = []

    def service_level(self):
        try:
            return 1.0 * self.service_level_calls / (self.service_level_calls_offered - self.service_level_aband)
        except ZeroDivisionError:
            return 1.0

    def print_status_line(self):
        return (' SL: {0:.2f}'.format(100*self.service_level()))


class Day(object):
    _ID = 0

    def __init__(self, arrival_rates, handle_times):
        self.id = self._ID
        self.__class__._ID += 1
        self.intervals = [
            Interval(
                stamp=stamp,
                calls=get_calls(stamp, arrival_rate, handle_times)
            ) for arrival_rate, stamp in zip(arrival_rates, [x for x in range(3600*24) if x % 900 == 0])
        ]


class Call(object):
    _ID = 0

    def __init__(self, arrival_timestamp, duration, direction='in'):
        self.id = self._ID; self.__class__._ID += 1
        self.arrival_timestamp = arrival_timestamp
        self.duration = duration
        self.status = 'pre-call'
        self.queued_at = None
        self.answered_at = None
        self.abandoned_at = None
        self.queue_elapsed = None
        self.handled_by = None
        self.queue = None
        self.sl_threshold_expired = False

    def reset(self):
        self.status = 'pre-call'
        self.queued_at = None
        self.answered_at = None
        self.queue_elapsed = None
        self.handled_by = None
        self.sl_threshold_expired = False


def simulate_one_step(timestamp, interval, service_desk, abandon_dist, skip_sleep=True, fast_mode=True, verbose_mode=False):
    i = timestamp

    c = 0
    pc = 0

    for agent in service_desk.agents[:]:
        agent = agent_logons(agent, i)
        agent = agent_logoffs(agent, i, service_desk.agents)
        agent = update_agent_status_stats(agent, i)

    for agent in service_desk.previously_logged_on_agents:
        agent = agent_logoffs(agent, i, service_desk.previously_logged_on_agents)
        agent = update_agent_status_stats(agent, i)

    for call in interval.calls:
        call = queue_calls(call, interval, i)
        call = answer_calls(call, interval, service_desk, i)
        call = hangup_calls(call, interval, i)
        call = update_queued_call_stats(call, interval, i)
        call = abandon_calls(call, interval, i, abandon_dist)
        if call.status == 'completed':
            c += 1
        elif call.status == 'pre-call':
            pc += 1

    for call in interval.previously_active_calls:
        call = hangup_calls(call, interval, i)
    
    if pc == len(interval.calls) or c == len(interval.calls):
        fast_mode = True  # enters fast mode when all calls are pre-call or done

    if not skip_sleep:
        if fast_mode:
            time.sleep(0.00001)
        else:
            time.sleep(0.05)
    
    if verbose_mode:
        print(secs_to_time(i) + interval.print_status_line())

    return interval


def simulate_interval(interval, service_desk, abandon_dist, skip_sleep=True, fast_mode=True, verbose_mode=False):
    for stamp in range(interval.stamp, interval.stamp + 900):
        interval = simulate_one_step(
            timestamp=stamp,
            interval=interval,
            service_desk=service_desk,
            abandon_dist=abandon_dist,
            skip_sleep=skip_sleep,
            fast_mode=fast_mode,
            verbose_mode=verbose_mode,
        )
    return interval


def optimize_interval(interval, service_desk, abandon_dist, skip_sleep=True, fast_mode=True, verbose_mode=False):
    hc_ranges = {'lower': 0, 'upper': 100}
    last_change = {'increase': False, 'change': 0}

    saved_interval_state = copy.deepcopy(interval)
    saved_service_desk_state = copy.deepcopy(service_desk)

    while not interval.optimized:
        for i in range(0, interval.agents_count):
            service_desk.agents.append(Agent(AgentSchedule(
                regular_start=interval.stamp,
                regular_end=interval.stamp + 899,
                regular_lunch=3600 * 24,
            )))

        for stamp in range(interval.stamp, interval.stamp + 900):
            interval = simulate_one_step(
                timestamp=stamp,
                interval=interval,
                service_desk=service_desk,
                abandon_dist=abandon_dist,
                skip_sleep=skip_sleep,
                fast_mode=fast_mode,
                verbose_mode=verbose_mode,
            )

        interval.optimized = review_and_adjust_hc(
            interval=interval,
            hc_ranges=hc_ranges,
            last_change=last_change,
        )

        if not interval.optimized:
            new_hc = interval.agents_count
            interval = copy.deepcopy(saved_interval_state)
            service_desk = copy.deepcopy(saved_service_desk_state)
            interval.agents_count = new_hc

    return interval


def simulate_day(day, service_desk, abandon_dist, skip_sleep=True, fast_mode=True, verbose_mode=False, optimization_mode=False):
    simulated_intervals = []

    previously_active_calls = []
    previously_queued_calls = []

    if optimization_mode:
        previously_logged_on_agents = []

    for interval in day.intervals:

        if optimization_mode:
            service_desk.agents = []
            if previously_logged_on_agents:
                service_desk.previously_logged_on_agents = previously_logged_on_agents

        if previously_queued_calls:
            interval.calls = previously_queued_calls + interval.calls

        if previously_active_calls:
            interval.previously_active_calls = previously_active_calls

        if optimization_mode:
            simulate = optimize_interval
        else:
            simulate = simulate_interval

        interval = simulate(
            interval=interval,
            service_desk=service_desk,
            abandon_dist=abandon_dist,
            skip_sleep=skip_sleep,
            fast_mode=fast_mode,
            verbose_mode=verbose_mode,
        )
        simulated_intervals.append(interval)

        previously_active_calls = [call for call in interval.calls if call.status == 'active']
        previously_queued_calls = [call for call in interval.calls if call.status == 'queued']

        if optimization_mode:
            previously_logged_on_agents = [agent for agent in service_desk.agents if agent.status == 'logged_on']

        print(
            'Simulated Interval: {interval}'.format(
                interval=pd.to_datetime(secs_to_time(interval.stamp)).time()
            )
        )

    day.intervals = simulated_intervals

    return day


def simulate_days(day_list, service_desk, abandon_dist, skip_sleep=True, fast_mode=True, verbose_mode=False):
    for day in day_list:
        day = simulate_day(day, service_desk, abandon_dist, skip_sleep, fast_mode, verbose_mode)
    return day_list


def simulate_days_alt(projected_volume_df, vol_dim, day_of_week_dist, handles_base,
                      agent_list, abandon_dist, outbound_list=[], outbound_reservation=0.0,
                      dials_per_reservation=0.0, reservation_length=0,
                      skip_sleep=True, fast_mode=True, verbose_mode=False):

    service_desk = ServiceDesk(agents=agent_list)

    simulated_days = []

    for i, day in projected_volume_df.iterrows():
        count_calls = day[vol_dim]
        arrival_rates = count_calls * day_of_week_dist
        day_object = Day(arrival_rates=arrival_rates, handle_times=handles_base)

        simulated_day = simulate_day(day_object, service_desk, abandon_dist)
        simulated_days.append(simulated_day)
    
    return simulated_days


def agent_logons(agent, timestamp):
    if agent.schedule.regular_start == timestamp and agent.status == 'logged_off':
        agent.status = 'logged_on'
    return agent


def agent_logoffs(agent, timestamp, agents_list):
    if agent.active_call == False and agent.status == 'logged_on' and agent.schedule.regular_end <= timestamp and agent.outbound_reserved == False:
        agent.status = 'logged_off'
        agents_list.remove(agent)

    return agent


def update_agent_status_stats(agent, timestamp):
    if agent.last_status != agent.status or agent.previously_active != agent.active_call or agent.previously_outbound != agent.outbound_reserved:
        agent.last_status = agent.status
        agent.previously_active = agent.active_call
        agent.previously_outbound = agent.outbound_reserved
        agent.time_in_status = 0
    else:
        agent.time_in_status += 1
    return agent


def queue_calls(call, interval, timestamp):
    if call.arrival_timestamp == timestamp:
        call.status = 'queued'
        call.queued_at = timestamp
        interval.calls_offered += 1
    return call


def update_queued_call_stats(call, interval, timestamp):
    if call.status == 'queued':
        call.queue_elapsed = timestamp - call.queued_at
        if (not call.sl_threshold_expired) and (call.queue_elapsed > interval.sl_threshold):
            call.sl_threshold_expired = True
            interval.service_level_calls_offered += 1
    return call


def answer_calls(call, interval, service_desk, timestamp):
    if call.status == 'queued':
        for agent in service_desk.agents:
            if agent.status == 'logged_on' and agent.active_call == False and agent.outbound_reserved == False:
                agent.active_call = True
                agent.handling_call = call.id
                call.handled_by = agent
                call.answered_at = timestamp
                call.queue_elapsed = timestamp - call.queued_at
                call.status = 'active'
                interval.calls_answered += 1
                if call.queue_elapsed <= interval.sl_threshold:
                    interval.service_level_calls += 1
                    interval.service_level_calls_offered += 1
                break
    return call


def hangup_calls(call, interval, timestamp):
    if call.status == 'active' and (call.duration + call.answered_at) <= timestamp:
        call.status = 'completed'
        call.completed_at = timestamp
        call.handled_by.active_call = False
        call.handled_by.handling_call = None
        interval.calls_handled += 1
        interval.sum_handle_time += call.duration
    return call


def abandon_calls(call, interval, timestamp, abandon_distribution):
    abandon_distribution = sorted(abandon_distribution)
    if call.status == 'queued':
        for aban_tuple in abandon_distribution:
            if aban_tuple[0] >= call.queue_elapsed:
                if random.random() >= aban_tuple[1]:
                    call.status = 'abandoned'
                    call.abandoned_at = timestamp
                    interval.total_calls_aband += 1
                    if call.queue_elapsed <= interval.sl_threshold:
                        interval.service_level_aband += 1
                        interval.service_level_calls_offered += 1
                    break
    return call


def round_down_900(stamp):
    return stamp - (stamp % 900)


def binary_search(hc, hc_range, increase=True):
    if increase:
        multiplier = 1  # defines the direction of change
        hc_range['lower'] = hc  # If target is above current HC, set new lower limit
        key = 'upper'
    else:
        multiplier = -1
        hc_range['upper'] = hc  # If target is below current HC, set new upper limit
        key = 'lower'
    difference = abs(hc - hc_range[key])
    change = max(0.5 * difference, 1) * multiplier  # Change cannot be less than 1 or negative, hence max
    change = int(change)  # rounds the change number
    hc += change
    return hc


def review_and_adjust_hc(interval, hc_ranges, last_change):
    sl_below_target = interval.service_level() < interval.sl_target
    sl_above_target = interval.service_level() > interval.sl_target
    if sl_below_target or sl_above_target:
        if sl_above_target and (interval.agents_count == 0):
            pass    # If SL is above target even with no available agents, no change needed
        else:
            increase_hc = sl_below_target   # determines the direction of change
            new_hc = binary_search(
                hc=interval.agents_count,
                hc_range=hc_ranges,
                increase=increase_hc,
            )
            last_change_was_increase = last_change['increase']
            required_drop_equals_last_increase = (interval.agents_count-new_hc == last_change['change'])
            if last_change_was_increase and required_drop_equals_last_increase:
                pass
            else:
                last_change['increase'] = increase_hc  # record direction of change
                last_change['change'] = abs(interval.agents_count-new_hc)    # record change in HC
                interval.agents_count = new_hc
                return False
    return True


def get_calls(stamp, arrival_rate, handle_times):
    arrival_threshold = float(arrival_rate) / 900
    arrival_times = []
    calls = []
    for i in range(stamp, stamp + 900):
        if random.random() < arrival_threshold:
            arrival_times.append(i)
    actual_num_calls = len(arrival_times)
    call_durations = handle_times.sample(actual_num_calls, replace=True)
    for arr, dur in zip(arrival_times, call_durations):
        calls.append(Call(arr, dur))

    return calls

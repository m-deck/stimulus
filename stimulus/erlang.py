import math
from past.builtins import xrange

#TODO: change all wait_time refs to be threshold instead

def intensity(aht, interval, rate):
    return aht * (rate / interval)

def erlang_b(server_count, intensity):
    ib = 1.0
    server_count = int(server_count) # need explicit cast here to prevent range TypeError
    for i in xrange(0, server_count):
        ib = 1.0 + ib * (i / intensity)
    return 1.0 / ib

def erlang_c(server_count, intensity):
    erl_b = erlang_b(server_count, intensity)
    return server_count * erl_b / (server_count - intensity * (1 - erl_b))

def occupancy(server_count, intensity):
    return intensity / server_count

def average_queue_time(server_count, rate, interval, aht, **kwargs):
    a = intensity(rate, aht, interval)
    return (erlang_c(server_count, a) * aht) / (server_count - a)

def service_level(server_count, rate, interval, aht, wait_time):
    a = intensity(rate, aht, interval)
    return (1 - erlang_c(server_count, a) * math.exp(-(server_count - a) * (wait_time / aht)))


def validate_sl_target(t):
    if 0.0 < t <= 1.0:
        raise ValueError('SL must be between 0 and 1')

    return True

def validate_asa_target(t):
    if t < 0:
        raise ValueError('ASA must be greater than 0')

    return True

def validate_target(target, target_type):
    validators = {'SL': validate_sl_target,
                  'ASA': validate_asa_target}

    validator = validators[target_type]

    validator(target)

    return True

funcs_to_targets = {'SL': service_level,
                    'ASA': average_queue_time}
def required_server_count(target, rate, interval, aht, wait_time=None, target_type='SL'):

    validate_target(target, target_type)

    a = intensity(rate, aht, interval)
    server_count = max(1, math.ceil(a))

    func = funcs_to_targets[target_type]

    while func(server_count, rate, interval, aht, wait_time) < target:
        server_count += 1
    
    return server_count



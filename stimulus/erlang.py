import math

#TODO: change all wait_time refs to be threshold instead

def intensity(aht, interval, rate):
    return aht * (rate / interval)

def erlang_b(server_count, intensity):
    ib = 1.0
    server_count = int(server_count) # need explicit cast here to prevent range TypeError
    for i in range(0, server_count):
        ib = 1.0 + ib * (i / intensity)
    return 1.0 / ib

def erlang_c(server_count, intensity):
    return server_count * erlang_b(server_count, intensity) / (server_count - intensity * (1 - erlang_b(server_count, intensity)))

def occupancy(server_count, intensity):
    return intensity / server_count

def average_queue_time(server_count, rate, interval, aht, **kwargs):
    a = intensity(rate, aht, interval)
    return (erlang_c(server_count, a) * aht) / (server_count - a)

def service_level(server_count, rate, interval, aht, wait_time):
    a = intensity(rate, aht, interval)
    return (1 - erlang_c(server_count, a) * math.exp(-(server_count - a) * (wait_time / aht)))

# if target is a tuple, assume SL target
# if target is a number, assume ASA target

def required_server_count(target, rate, interval, aht):
    a = intensity(rate, aht, interval)
    server_count = max(1, math.ceil(a))
    
    if type(target) is tuple:
        func = service_level
        if not 0.0 < target[0] <= 1.0:
            raise ValueError
        wait_time = target[1]
        target = target[0]
    elif type(target) is float or type(target) is int:
        func = average_queue_time
        wait_time = None
    else:
        raise TypeError

    while func(server_count, rate, interval, aht, wait_time) < target:
        server_count += 1
    
    return server_count



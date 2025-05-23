def fcfs(processes):
    # Sort by arrival time
    processes.sort(key=lambda x: x['arrival_time'])

    current_time = 0
    result = []

    for process in processes:
        pid = process['pid']
        arrival = process['arrival_time']
        burst = process['burst_time']

        start_time = max(current_time, arrival)
        completion_time = start_time + burst
        turnaround_time = completion_time - arrival
        waiting_time = turnaround_time - burst

        result.append({
            'pid': pid,
            'start_time': start_time,
            'completion_time': completion_time,
            'turnaround_time': turnaround_time,
            'waiting_time': waiting_time
        })

        current_time = completion_time  # Move to next time slot

    return result



def sjf(processes):
    processes.sort(key=lambda x: (x['arrival_time'], x['burst_time']))
    n = len(processes)
    completed = 0
    current_time = 0
    visited = [False] * n
    result = []

    while completed < n:
        idx = -1
        min_burst = float('inf')

        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and not visited[i]:
                if processes[i]['burst_time'] < min_burst:
                    min_burst = processes[i]['burst_time']
                    idx = i

        if idx == -1:
            current_time += 1
            continue

        process = processes[idx]
        start_time = current_time
        completion_time = start_time + process['burst_time']
        turnaround_time = completion_time - process['arrival_time']
        waiting_time = turnaround_time - process['burst_time']

        result.append({
            'pid': process['pid'],
            'start_time': start_time,
            'completion_time': completion_time,
            'turnaround_time': turnaround_time,
            'waiting_time': waiting_time
        })

        current_time = completion_time
        visited[idx] = True
        completed += 1

    return result

def priority(processes):
    processes.sort(key=lambda x: (x['arrival_time'], x['priority']))
    n = len(processes)
    completed = 0
    current_time = 0
    visited = [False] * n
    result = []

    while completed < n:
        idx = -1
        min_priority = float('inf')

        for i in range(n):
            if processes[i]['arrival_time'] <= current_time and not visited[i]:
                if processes[i]['priority'] < min_priority:
                    min_priority = processes[i]['priority']
                    idx = i

        if idx == -1:
            current_time += 1
            continue

        process = processes[idx]
        start_time = current_time
        completion_time = start_time + process['burst_time']
        turnaround_time = completion_time - process['arrival_time']
        waiting_time = turnaround_time - process['burst_time']

        result.append({
            'pid': process['pid'],
            'start_time': start_time,
            'completion_time': completion_time,
            'turnaround_time': turnaround_time,
            'waiting_time': waiting_time
        })

        current_time = completion_time
        visited[idx] = True
        completed += 1

    return result

def round_robin(processes, time_quantum):
    from collections import deque

    queue = deque()
    current_time = 0
    result = []
    remaining_burst = {p['pid']: p['burst_time'] for p in processes}
    arrived = []
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    n = len(processes)
    completed = 0
    in_queue = set()

    while completed < n:
        for p in processes:
            if p['arrival_time'] <= current_time and p['pid'] not in in_queue and p['pid'] not in [item['pid'] for item in result]:
                queue.append(p)
                in_queue.add(p['pid'])

        if not queue:
            current_time += 1
            continue

        process = queue.popleft()
        pid = process['pid']
        start_time = current_time
        burst_time = remaining_burst[pid]

        if burst_time <= time_quantum:
            current_time += burst_time
            completion_time = current_time
            turnaround_time = completion_time - process['arrival_time']
            waiting_time = turnaround_time - process['burst_time']
            result.append({
                'pid': pid,
                'start_time': start_time,
                'completion_time': completion_time,
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time
            })
            remaining_burst[pid] = 0
            completed += 1
        else:
            current_time += time_quantum
            remaining_burst[pid] -= time_quantum
            # Recheck for newly arrived processes
            for p in processes:
                if p['arrival_time'] <= current_time and p['pid'] not in in_queue and p['pid'] not in [item['pid'] for item in result]:
                    queue.append(p)
                    in_queue.add(p['pid'])
            queue.append(process)  # Re-queue the current process

    return result

def srtf(processes):
    n = len(processes)
    remaining_time = [p['burst_time'] for p in processes]
    complete = 0
    t = 0
    shortest = None
    minm = float('inf')
    check = False
    finish_time = 0

    result = []
    is_completed = [False] * n
    start_time = [-1] * n
    process_map = {p['pid']: i for i, p in enumerate(processes)}

    while complete != n:
        for j in range(n):
            if (processes[j]['arrival_time'] <= t and
                    remaining_time[j] < minm and remaining_time[j] > 0):
                minm = remaining_time[j]
                shortest = j
                check = True

        if not check:
            t += 1
            continue

        # Record first start time
        if start_time[shortest] == -1:
            start_time[shortest] = t

        remaining_time[shortest] -= 1
        minm = remaining_time[shortest] if remaining_time[shortest] > 0 else float('inf')

        if remaining_time[shortest] == 0:
            complete += 1
            check = False
            finish_time = t + 1

            arrival = processes[shortest]['arrival_time']
            burst = processes[shortest]['burst_time']
            turnaround_time = finish_time - arrival
            waiting_time = turnaround_time - burst

            result.append({
                'pid': processes[shortest]['pid'],
                'start_time': start_time[shortest],
                'completion_time': finish_time,
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time
            })

        t += 1

    return result


def multilevel_queue(processes):
    # Queue 1: Priority (lower value = higher priority)
    # Queue 2: FCFS for all others
    queue1 = [p for p in processes if p['priority'] <= 2]
    queue2 = [p for p in processes if p['priority'] > 2]

    result = []

    if queue1:
        result += priority(queue1)
    if queue2:
        result += fcfs(queue2)

    return sorted(result, key=lambda x: x['start_time'])
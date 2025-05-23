def recommend(processes):
    if not processes:
        return "FCFS"

    arrival_times = [p['arrival_time'] for p in processes]
    burst_times = [p['burst_time'] for p in processes]
    priorities = [p.get('priority', 0) for p in processes]
    queues = [p.get('queue', 0) for p in processes]

    all_zero_arrival = all(at == 0 for at in arrival_times)
    same_priority = len(set(priorities)) == 1
    same_queue = len(set(queues)) == 1
    scattered_arrival = len(set(arrival_times)) > 1
    burst_variance = max(burst_times) - min(burst_times)

    # If processes belong to multiple queues
    if len(set(queues)) > 1:
        return "Multilevel Queue"

    if all_zero_arrival:
        if same_priority:
            return "SJF"
        else:
            return "Priority"

    if same_priority and scattered_arrival and burst_variance <= 2:
        return "Round Robin"

    if same_priority and scattered_arrival and burst_variance > 2:
        return "SRTF"

    if not same_priority:
        return "Priority"

    return "FCFS"

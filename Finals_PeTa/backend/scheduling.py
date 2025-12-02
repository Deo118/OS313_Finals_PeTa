# CPU Scheduling Algorithms
from copy import deepcopy
from collections import deque

class Process:
    # Holds all process-related data
    def __init__(self, pid, at, bt, priority=0):
        self.pid = pid
        self.at = int(at)
        self.bt = int(bt)
        self.priority = int(priority)
        self.wt = 0
        self.tat = 0

    def to_dict(self):
        return {
            "pid": self.pid,
            "arrival": self.at,
            "burst": self.bt,
            "priority": self.priority,
            "wait": self.wt,
            "tat": self.tat,
        }


class CPUScheduler:
    # Unified response formatting
    @staticmethod
    def _make_response(processes, timeline):
        table = [p.to_dict() for p in processes]
        n = len(processes)
        avg_wt = sum(p.wt for p in processes) / n if n else 0
        avg_tat = sum(p.tat for p in processes) / n if n else 0

        gantt = [
            {"pid": pid, "start": st, "finish": ft} for (pid, st, ft) in timeline
        ]
        return {
            "table": table,
            "timeline": gantt,
            "avg_wt": avg_wt,
            "avg_tat": avg_tat,
        }

    # FCFS
    @staticmethod
    def fcfs(processes):
        procs = deepcopy(processes)
        procs.sort(key=lambda p: p.at)
        time = 0
        timeline = []
        for p in procs:
            if time < p.at:
                time = p.at
            start = time
            p.wt = start - p.at
            time += p.bt
            finish = time
            p.tat = p.wt + p.bt
            timeline.append((p.pid, start, finish))
        return CPUScheduler._make_response(procs, timeline)

    # SJF Non-preemptive
    @staticmethod
    def sjf(processes):
        procs = deepcopy(processes)
        n = len(procs)
        time = 0
        done = [False] * n
        completed = 0
        timeline = []

        while completed < n:
            ready = [
                i for i, p in enumerate(procs) if p.at <= time and not done[i]
            ]
            if not ready:
                time += 1
                continue

            idx = min(ready, key=lambda i: procs[i].bt)
            p = procs[idx]
            start = time
            p.wt = start - p.at
            time += p.bt
            finish = time
            p.tat = p.wt + p.bt
            done[idx] = True
            completed += 1
            timeline.append((p.pid, start, finish))

        return CPUScheduler._make_response(procs, timeline)

    # SJF Preemptive
    @staticmethod
    def sjf_preemptive(processes):
        procs = deepcopy(processes)
        n = len(procs)
        remaining = [p.bt for p in procs]
        time = 0
        completed = 0
        last = None
        start_t = 0
        timeline = []

        while completed < n:
            ready = [
                i for i, p in enumerate(procs)
                if p.at <= time and remaining[i] > 0
            ]
            if not ready:
                time += 1
                continue

            idx = min(ready, key=lambda i: remaining[i])
            p = procs[idx]

            if last != p.pid:
                if last is not None:
                    timeline.append((last, start_t, time))
                last = p.pid
                start_t = time

            remaining[idx] -= 1
            time += 1

            if remaining[idx] == 0:
                completed += 1
                p.tat = time - p.at
                p.wt = p.tat - p.bt

        if last is not None:
            timeline.append((last, start_t, time))

        return CPUScheduler._make_response(procs, timeline)

    # Priority Non-preemptive
    @staticmethod
    def priority(processes):
        procs = deepcopy(processes)
        n = len(procs)
        time = 0
        done = [False] * n
        completed = 0
        timeline = []

        while completed < n:
            ready = [
                i for i, p in enumerate(procs)
                if p.at <= time and not done[i]
            ]
            if not ready:
                time += 1
                continue

            idx = min(ready, key=lambda i: procs[i].priority)
            p = procs[idx]
            start = time
            p.wt = start - p.at
            time += p.bt
            finish = time
            p.tat = p.wt + p.bt
            done[idx] = True
            completed += 1
            timeline.append((p.pid, start, finish))

        return CPUScheduler._make_response(procs, timeline)

    # Priority Preemptive
    @staticmethod
    def priority_preemptive(processes):
        procs = deepcopy(processes)
        n = len(procs)
        remaining = [p.bt for p in procs]
        time = 0
        completed = 0
        last = None
        st = 0
        timeline = []

        while completed < n:
            ready = [
                i for i, p in enumerate(procs)
                if p.at <= time and remaining[i] > 0
            ]
            if not ready:
                time += 1
                continue

            idx = min(ready, key=lambda i: procs[i].priority)
            p = procs[idx]

            if last != p.pid:
                if last is not None:
                    timeline.append((last, st, time))
                last = p.pid
                st = time

            remaining[idx] -= 1
            time += 1

            if remaining[idx] == 0:
                completed += 1
                p.tat = time - p.at
                p.wt = p.tat - p.bt

        if last is not None:
            timeline.append((last, st, time))

        return CPUScheduler._make_response(procs, timeline)

    # Round Robin
    @staticmethod
    def round_robin(processes, quantum):
        procs = deepcopy(processes)
        procs.sort(key=lambda p: p.at)
        n = len(procs)

        time = 0
        remaining = [p.bt for p in procs]
        tat = [0] * n
        wt = [0] * n
        completed = [False] * n
        queue = deque()
        timeline = []
        i = 0

        while i < n and procs[i].at <= time:
            queue.append(i)
            i += 1

        if not queue and i < n:
            time = procs[i].at
            queue.append(i)
            i += 1

        while queue:
            idx = queue.popleft()
            p = procs[idx]
            start = time

            if remaining[idx] > quantum:
                time += quantum
                remaining[idx] -= quantum
            else:
                time += remaining[idx]
                tat[idx] = time - p.at
                wt[idx] = tat[idx] - p.bt
                remaining[idx] = 0
                completed[idx] = True

            timeline.append((p.pid, start, time))

            while i < n and procs[i].at <= time:
                queue.append(i)
                i += 1

            if not completed[idx]:
                queue.append(idx)

            if not queue and i < n:
                time = procs[i].at
                queue.append(i)
                i += 1

        for j in range(n):
            procs[j].wt = wt[j]
            procs[j].tat = tat[j]

        return CPUScheduler._make_response(procs, timeline)

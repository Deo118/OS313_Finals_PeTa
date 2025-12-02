# Banker's Algorithm (1 resource type)

class Banker:
    @staticmethod
    def is_safe(allocation, maximum, available):
        n = len(allocation)
        if n == 0:
            return [], False, []

        for row in allocation:
            if len(row) != 1:
                raise ValueError("Allocation must contain 1 resource per process.")
        for row in maximum:
            if len(row) != 1:
                raise ValueError("Maximum must contain 1 resource per process.")
        if len(available) != 1:
            raise ValueError("Available must be a list of length 1.")

        need = [[maximum[i][0] - allocation[i][0]] for i in range(n)]
        work = [available[0]]
        finished = [False] * n
        steps = []
        sequence = []

        changed = True
        while changed:
            changed = False
            for i in range(n):
                if finished[i]:
                    continue

                before = work[0]
                can = need[i][0] <= work[0]

                entry = {
                    "process": i,
                    "need": need[i],
                    "available_before": [before],
                    "can_run": can,
                    "allocation": allocation[i],
                }

                if can:
                    work[0] += allocation[i][0]
                    entry["work_after"] = [work[0]]
                    finished[i] = True
                    sequence.append(i)
                    changed = True

                steps.append(entry)

        safe = all(finished)
        return steps, safe, sequence

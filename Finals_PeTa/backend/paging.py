# Page Replacement Algorithms (FIFO, LRU, Optimal)
from collections import deque


class PageReplacement:
    @staticmethod
    def _validate(rs, frames):
        if not isinstance(rs, (list, tuple)):
            raise ValueError("reference_string must be a list")
        if frames <= 0:
            raise ValueError("num_frames must be > 0")

    @staticmethod
    def simulate(refs, frames, algo):
        PageReplacement._validate(refs, frames)
        algo = algo.upper()
        if algo == "FIFO":
            return PageReplacement.fifo(refs, frames)
        if algo == "LRU":
            return PageReplacement.lru(refs, frames)
        if algo == "OPTIMAL":
            return PageReplacement.optimal(refs, frames)
        raise ValueError("Unknown algorithm.")
    #FIFO
    @staticmethod
    def fifo(refs, f):
        frames = [-1] * f
        queue = deque()
        steps = []
        faults = 0
        hits = 0

        for t, page in enumerate(refs):
            if page in frames:
                hits += 1
                steps.append({"ref": page, "time": t, "frames": list(frames), "page_fault": False})
            else:
                faults += 1
                if -1 in frames:
                    idx = frames.index(-1)
                    frames[idx] = page
                    queue.append(idx)
                else:
                    idx = queue.popleft()
                    frames[idx] = page
                    queue.append(idx)

                steps.append({"ref": page, "time": t, "frames": list(frames), "page_fault": True})

        return {
            "algorithm": "FIFO",
            "references": refs,
            "frames": f,
            "steps": steps,
            "page_faults": faults,
            "page_hits": hits,
        }
    #LRU
    @staticmethod
    def lru(refs, f):
        frames = [-1] * f
        last = {}
        steps = []
        faults = 0
        hits = 0

        for t, page in enumerate(refs):
            if page in frames:
                hits += 1
                last[page] = t
                steps.append({"ref": page, "time": t, "frames": list(frames), "page_fault": False})
            else:
                faults += 1
                if -1 in frames:
                    idx = frames.index(-1)
                    frames[idx] = page
                    last[page] = t
                else:
                    lru_page = None
                    lru_time = None
                    lru_idx = None
                    for idx, p in enumerate(frames):
                        lu = last.get(p, -1)
                        if lru_time is None or lu < lru_time:
                            lru_time = lu
                            lru_page = p
                            lru_idx = idx
                    frames[lru_idx] = page
                    last.pop(lru_page, None)
                    last[page] = t

                steps.append({"ref": page, "time": t, "frames": list(frames), "page_fault": True})

        return {
            "algorithm": "LRU",
            "references": refs,
            "frames": f,
            "steps": steps,
            "page_faults": faults,
            "page_hits": hits,
        }
    #Optimal
    @staticmethod
    def optimal(refs, f):
        frames = [-1] * f
        steps = []
        faults = 0
        hits = 0
        n = len(refs)

        for t, page in enumerate(refs):
            if page in frames:
                hits += 1
                steps.append({"ref": page, "time": t, "frames": list(frames), "page_fault": False})
                continue

            faults += 1
            if -1 in frames:
                idx = frames.index(-1)
                frames[idx] = page
            else:
                farthest = -1
                replace_idx = None
                for idx, p in enumerate(frames):
                    nxt = None
                    for k in range(t + 1, n):
                        if refs[k] == p:
                            nxt = k
                            break
                    if nxt is None:
                        replace_idx = idx
                        break
                    if nxt > farthest:
                        farthest = nxt
                        replace_idx = idx
                frames[replace_idx] = page

            steps.append({"ref": page, "time": t, "frames": list(frames), "page_fault": True})

        return {
            "algorithm": "OPTIMAL",
            "references": refs,
            "frames": f,
            "steps": steps,
            "page_faults": faults,
            "page_hits": hits,
        }

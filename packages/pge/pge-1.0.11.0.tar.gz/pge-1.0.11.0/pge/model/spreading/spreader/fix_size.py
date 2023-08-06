import numpy as np

from pge.model.spreading.spreader.basic import SpreadingModel


class FixSpreadModel(SpreadingModel):
    def __init__(self, graph, in_direct=False):
        super().__init__(graph)
        self.ids = self.graph.get_ids(stable=True)
        self.in_direct = in_direct

    def init(self):
        self.received = {
            k: self.initial_status[k].copy() for k in self.initial_status.keys()
        }
        self.update(0)

    def iteration_bunch_comm(self, num_iter, tick, rs):
        res = []
        self.rs = np.max(rs)
        rs = np.array(rs)

        for _ in np.arange(num_iter):
            n = 1
            self.init()

            count = 0
            while self.rs > np.min([time[1] for time in self.times]):
                if n > tick:
                    break

                self.iteration()
                self.update(n)
                n += 1

                if np.sum(rs[count:] == np.min([time[1] for time in self.times])) > 0:
                    res = np.append(res, [time.copy() for time in self.times])
                    count += 1
                    print(n)

            res = np.append(res, [time.copy() for time in self.times])
        res = np.reshape(res, (res.size // 3, 3))
        return res

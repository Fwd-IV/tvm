import cpuinfo
import numpy as np
from multiprocessing import Process

class BaseAggressor(object):
    """Aggressor base class with local cpu info"""
    def __init__(self):
        self.cpu_info = cpuinfo.get_cpu_info()
        self.cpu_sockets = 2 # mandatory
        self.logic_core_cnt = \
            int(self.cpu_info["count"])
        self.physical_core_cnt = self.logic_core_cnt // self.cpu_sockets
        self.llc_cache_size = \
            int(self.cpu_info["l3_cache_size"].split(" ")[0]) * 1024 * 2
        self.l2_cache_size = \
            int(self.cpu_info["l2_cache_size"].split(" ")[0]) * 1024 * self.physical_core_cnt
        self.l1d_cache_size = \
            int(self.cpu_info["l1_data_cache_size"].split(" ")[0]) * 1024 * self.physical_core_cnt
        self.l1i_cache_size = \
            int(self.cpu_info["l1_instruction_cache_size"].split(" ")[0]) * 1024 * self.physical_core_cnt
    

    def timed_run(self, ttl=0):
        p = Process(target=self.run, args=())
        p.start()
        if ttl > 0:
            print("waiting to join")
            p.join(ttl)
            if p.is_alive():
                p.terminate()
        else:
            p.join()


    def run(self):
        print("Not implemented")
        pass


class L2Aggressor(BaseAggressor):
    """L2 Aggressor task"""

    def __init__(self, ratio=1.0):
        super(L2Aggressor, self).__init__()
        self.l2_cache_size = int(ratio * self.l2_cache_size * 2)
        self.data = np.random.rand(self.l2_cache_size // 4).astype(np.float32)

    def run(self):
        while True:
            self.data = self.data + 1.0


class LlcAggressor(BaseAggressor):
    """LLC Aggressor task"""

    def __init__(self, ratio=1.0):
        super(LlcAggressor, self).__init__()
        self.llc_cache_size = int(ratio * self.llc_cache_size * 2)
        self.data = np.random.rand(self.llc_cache_size // 4).astype(np.float32)

    def run(self):
        while True:
            self.data = self.data + 1.0


if __name__ == "__main__":
    llc_aggressor = LlcAggressor(0.5)
    llc_aggressor.timed_run(20)
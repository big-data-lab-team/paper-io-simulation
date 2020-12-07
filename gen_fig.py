import os
import sys
sys.path.append(os.path.abspath("result/single/"))
sys.path.append(os.path.abspath("result/multi/"))

os.chdir("result/single")
import result.single.plot_memprof as plot_memprof
import result.single.plot_error as plot_error
import result.single.plot_cache as plot_cache
plot_memprof.compare_plot([20, 100], [200, 1300])
plot_error.plot_error()
plot_cache.plot_cache_v2()

os.chdir("../multi")
import result.multi.process_result as multi_result
multi_result.result_local(rep_no=5)
multi_result.result_nfs(rep_no=5)
import os
import sys
sys.path.append(os.path.abspath("result/single/"))
sys.path.append(os.path.abspath("result/multi/"))


# ======== Single-threaded experiment results ==========
os.chdir("result/single")
import result.single.plot_memprof as plot_memprof
import result.single.plot_error as plot_error
import result.single.plot_cache as plot_cache

# Generate memory profiling comparision between 20GB and 100GB inputs.
# xmax is set to 200 and 1300
plot_memprof.compare_plot([20, 100], [200, 1300])
# Generate simulation errors with 20GB and 100GB inputs
plot_error.plot_error()
# Generate amount of cached data with 20GB and 100GB inputs
plot_cache.plot_cache_v2()

# ======== Multi-threaded experiment results ==========
os.chdir("../multi")
import result.multi.process_result as multi_result
# Generate figures of experiment with local file system
multi_result.result_local(rep_no=5)
# Generate figures of experiment with NFS
multi_result.result_nfs(rep_no=5)
# Generate figures of simulation time
multi_result.run_time()

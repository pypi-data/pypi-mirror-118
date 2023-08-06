
import multiprocessing
from multiprocessing.pool import ThreadPool

import dask
import numcodecs
from arbol import aprint
from napari.utils.dask_utils import create_dask_cache
from numcodecs import blosc

def config_dask_and_blosc():
    # Configure multithreading for Dask:
    _cpu_count = multiprocessing.cpu_count() // 2
    # aprint(f"Number of cores on system: {_cpu_count}")
    _nb_threads = max(1, _cpu_count)

    aprint(f"Number of threads used by BLOSC and DASK: {blosc.get_nthreads()}")

    dask.config.set(scheduler='threads')
    dask.config.set(pool=ThreadPool(_nb_threads))

    # Configure multithreading for Blosc:
    blosc.set_nthreads(_nb_threads)

    # same for numcodecs:
    numcodecs.blosc.use_threads = True
    numcodecs.blosc.set_nthreads(_nb_threads)

    #Config Dask cache using napari:
    try:
        create_dask_cache(mem_fraction=0.95)
    except Exception as e:
        aprint("Warning: Setting Dask caching failed.")
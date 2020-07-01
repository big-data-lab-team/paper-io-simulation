class File:
    """
    File class.
    """

    def __init__(self, name, size=0, disk=0, cache=0, dirty=0, active=0, inactive=0):
        """
        :param name: filename
        :param size: size in MB
        :param disk: data on disk in MB
        :param cache: data in cache in MB
        :param dirty: dirty data in MB
        :param active: data in active list in MB
        :param inactive: data in inactive list in MB
        """
        self.name = name
        self.size = size
        # self.disk = disk
        # self.dirty = dirty
        # self.active = active
        # self.inactive = inactive


class Block:
    """Data block of a File"""

    def __init__(self, filename, size=0, dirty=False, last_access=0.0):
        self.filename = filename
        self.size = size
        self.dirty = dirty
        self.last_access = last_access


class MemoryManager:
    def __init__(self, size=0, free=0, cache=0, dirty=0, read_bw=0, write_bw=0, dirty_expire=30):
        """
        LRU list: list of tuples, the first value is filename, the 2nd value is timestamp, the 3rd value amount of data

        :param size: total memory in MB
        :param free: free memory in MB
        :param cache: cache used in MB
        :param dirty: dirty data in MB
        :param read_bw: read bandwidth in MBps
        :param write_bw: write bandwidth in MBps
        """
        self.size = size
        self.free = free
        self.cache = cache
        self.dirty = dirty
        self.read_bw = read_bw
        self.active = []
        self.inactive = []
        self.write_bw = write_bw
        self.dirty_expire = dirty_expire
        # self.active_list = []
        # self.inactive_list = []
        self.log = {
            "total": [self.size],
            "free": [self.free],
            "cache": [self.cache],
            "dirty": [self.dirty],
            "used": [self.size - self.free],
            "time": [0]
        }

    def get_data_in_cache(self, filename):
        """
        Return the amount of data cached
        :param filename:
        :return:
        """
        amount = 0
        for block in self.inactive:
            if block.filename == filename:
                amount += block.size

        for block in self.active:
            if block.filename == filename:
                amount += block.size

        return amount

    def get_available_memory(self):
        return self.free + self.cache - self.dirty

    def get_evictable_memory(self):
        return sum([block.size for block in self.inactive if not block.dirty])

    def read_from_cache(self, filename, time):
        """
        Read data from cache. All data in cache is active
        :param filename:
        :param time:
        :return:
        """

        dirty = 0
        not_dirty = 0
        for block in self.inactive[:]:
            if block.filename == filename:
                if block.dirty:
                    dirty += block.size
                else:
                    not_dirty += block.size
                self.inactive.remove(block)

        for block in self.active[:]:
            if block.filename == filename:
                if block.dirty:
                    dirty += block.size
                else:
                    not_dirty += block.size
                self.active.remove(block)

        # Update all accessed data as active
        dirty_block = Block(filename, dirty, dirty=True, last_access=time)
        not_dirty_block = Block(filename, not_dirty, dirty=False, last_access=time)
        self.active.append(dirty_block)
        self.active.append(not_dirty_block)

        self.update_lru_lists()

    def read_from_disk(self, amount, filename, time):
        """
        Read data not cached from disk. Add new read block to inactive list.
        :param amount:
        :param filename:
        :param time:
        :return:
        """

        self.cache += amount
        self.free -= amount

        block = Block(filename=filename, size=amount, dirty=False, last_access=time)
        self.inactive.append(block)
        self.update_lru_lists()

    def pdflush(self, current_time, max_flushed=0):

        flushed = 0
        for block in self.inactive:
            if block.dirty and current_time - block.last_access > self.dirty_expire:
                if 0 < max_flushed < flushed + block.size:
                    flushed += max_flushed - flushed
                    # split the block, new clean block is created
                    new_blk = Block(block.filename, max_flushed - flushed, dirty=False,
                                    last_access=block.last_access)
                    self.inactive.append(new_blk)
                    block.size = block.size + flushed - max_flushed
                else:
                    block.dirty = False
                    flushed += block.size

        for block in self.active:
            if block.dirty and current_time - block.last_access > self.dirty_expire:
                if 0 < max_flushed < flushed + block.size:
                    flushed += max_flushed - flushed
                    # split the block, new clean block is created
                    new_blk = Block(block.filename, max_flushed - flushed, dirty=False,
                                    last_access=block.last_access)
                    self.inactive.append(new_blk)
                    block.size = block.size + flushed - max_flushed
                else:
                    block.dirty = False
                    flushed += block.size

        self.dirty -= flushed

        return flushed

    def evict(self, amount):

        if amount <= 0:
            return 0

        evicted = 0
        for block in self.inactive[:]:

            if block.dirty:
                continue

            if evicted >= amount:
                break
            elif evicted < amount < evicted + block.size:
                block_evicted = amount - evicted
                block.size -= block_evicted
                evicted += block_evicted
                break
            else:
                evicted += block.size
                self.inactive.remove(block)

        self.free += evicted
        self.cache -= evicted

        return evicted

    def write(self, filename, amount, time):
        """
        Write a file to disk through cache. The written file is not in cache. Thus, all data is in inactive list
        :param filename: filename
        :param amount: total amount of data to write
        :param max_cache: maximum cache
        :param new_dirty: amount of dirty data
        :param time:
        :return:
        """

        # self.inactive.append(Block(filename, amount, dirty=True, last_access=time))

        # if self.cache + amount > max_cache:
        #     self.cache = max_cache
        #     self.free = 0
        # else:
        #     self.cache += amount
        #     self.free -= amount

        self.cache += amount
        self.free -= amount
        self.dirty += amount
        self.inactive.append(Block(filename, amount, dirty=True, last_access=time))

        self.update_lru_lists()

    def flush(self, amount):
        if amount <= 0:
            return 0

        flushed = 0

        self.inactive.reverse()
        for block in self.inactive:
            if block.dirty:
                if flushed + block.size <= amount:
                    block.dirty = False
                    self.dirty -= block.size
                    flushed += block.size
                elif flushed < amount < flushed + block.size:
                    blk_flushed = amount - flushed
                    flushed += blk_flushed
                    block.size -= blk_flushed
                    self.dirty -= blk_flushed
                    new_block = Block(block.filename, blk_flushed, dirty=False, last_access=block.last_access)
                    self.inactive.append(new_block)
                else:
                    break

        if flushed < amount:
            self.active.reverse()
            for block in self.active:
                if block.dirty:
                    if flushed + block.size <= amount:
                        block.dirty = False
                        self.dirty -= block.size
                        flushed += block.size
                    elif flushed < amount < flushed + block.size:
                        blk_flushed = amount - flushed
                        flushed += blk_flushed
                        block.size -= blk_flushed
                        self.dirty -= blk_flushed
                        new_block = Block(block.filename, blk_flushed, dirty=False, last_access=block.last_access)
                        self.active.append(new_block)
                    else:
                        break

        self.update_lru_lists()

        return flushed

    def update_lru_lists(self):
        self.inactive = sorted(self.inactive, key=lambda block: block.last_access)
        self.active = sorted(self.active, key=lambda block: block.last_access)

        inactive_size = sum([block.size for block in self.inactive])
        active_size = sum([block.size for block in self.active])

        # move old data from active to inactive list
        if active_size >= 2 * inactive_size:
            avg = (active_size + inactive_size) / 2
            for block in self.active[:]:
                if active_size - block.size < avg:
                    block.size -= active_size - avg
                    new_block = Block(block.filename, active_size - avg, dirty=block.dirty,
                                      last_access=block.last_access)
                    self.inactive.append(new_block)
                    break
                else:
                    self.inactive.append(block)
                    self.active.remove(block)

        self.inactive = sorted(self.inactive, key=lambda block: block.last_access)

    def add_log(self, time):
        self.log["time"].append(time)
        self.log["total"].append(self.size)
        self.log["free"].append(self.free)
        self.log["used"].append(self.size - self.free)
        self.log["cache"].append(self.cache)
        self.log["dirty"].append(self.dirty)

    def get_log(self):
        return self.log

    def print(self):
        print("Memory status:")
        print("\t Total: %.2f" % self.size)
        print("\t Free: %.2f" % self.free)
        print("\t Cache: %.2f" % self.cache)
        print("\t Dirty: %.2f" % self.dirty)

    def print_cached_dirty(self):
        print("\nInactive:")
        total_inactive = 0
        for block in self.inactive:
            total_inactive += block.size
            print("%s, %d MB, dirty=%r, %f" % (block.filename, block.size, block.dirty, block.last_access))
        print("Total: %d MB" % total_inactive)

        total_active = 0
        print("\nActive:")
        for block in self.active:
            total_active += block.size
            print("%s, %d MB, dirty=%r, %f" % (block.filename, block.size, block.dirty, block.last_access))
        print("Total: %d MB\n" % total_active)

    def print_file_total_cached(self):
        inactive = {}
        active = {}

        for block in self.inactive:
            if block.filename in inactive.keys():
                inactive[block.filename] += block.size
            else:
                inactive[block.filename] = block.size

        for block in self.active:
            if block.filename in active.keys():
                active[block.filename] += block.size
            else:
                active[block.filename] = block.size

        print("\nInactive:")
        print(inactive)
        print("Active:")
        print(active)
        print("\n")


class Storage:
    def __init__(self, size=0, read_bw=0, write_bw=0):
        """

        :param size: total capacity in MB
        :param read_bw: read bandwidth in MBps
        :param write_bw: write bandwidth in MBps
        """
        self.size = size
        self.read_bw = read_bw
        self.write_bw = write_bw

    def read(self, amount):
        return amount / self.read_bw

    def write(self, amount):
        return amount / self.write_bw


class IOManager:
    def __init__(self, memory_, storage_, dirty_ratio=0.2, dirty_bg_ratio=0.1,
                 pdflush_interval=5, start_time=0):
        self.memory = memory_
        self.storage = storage_
        self.dirty_ratio = dirty_ratio
        self.dirty_bg_ratio = dirty_bg_ratio
        self.last_pdflush = start_time
        self.pdflush_interval = pdflush_interval

    def read(self, file, run_time=0):
        self.memory.add_log(run_time)
        print("%.2f Start reading %s" % (run_time, file.name))

        cached_amt = self.memory.get_data_in_cache(file.name)
        from_disk = file.size - cached_amt

        # ============= FORCED FLUSHING - EVICTION ==========
        # Memory required to accommodate file on top of available memory
        # memory required for the file: 2 * file.size - cached_amt
        # memory immediately available:  free + evictable
        # calculate the amount to flush if needed
        flush_time = self.flush(2 * file.size - cached_amt - self.memory.free - self.memory.get_evictable_memory())
        run_time += flush_time
        print("\tPre-flush in %.2f sec" % flush_time)
        # then evict old pages if needed
        self.evict(2 * file.size - cached_amt - self.memory.free)

        self.memory.add_log(run_time)

        # ===================== START READING =====================
        # if part of file is cached, access pages in cache again to update LRU lists
        if cached_amt > 0:
            # Re-access cache data
            self.memory.read_from_cache(file.name, run_time)

            # bcz cache read and periodical flushing are concurrent, take the longer
            mem_read_time = cached_amt / self.memory.read_bw

            # concurrent periodical flushing if there is still dirty old data after forced flushing
            # periodical flushing duration is limited to cache read time
            self.period_flush(run_time, mem_read_time)
            run_time += mem_read_time

            # application occupies memory to store read data
            self.memory.free -= cached_amt

            self.memory.add_log(run_time)
            print("\tRead %d MB from cache in %.2f sec" % (cached_amt, mem_read_time))

        if from_disk > 0:
            # periodical flushing if there is still dirty old data
            # This periodical flushing can be called after a forced flushing or a cache read
            # disk read and periodical flushing are time shared
            pdflush_time = self.period_flush(run_time)
            run_time += pdflush_time
            self.memory.add_log(run_time)
            print("\tpdflush in %.2f sec" % pdflush_time)

            # add to inactive list
            self.memory.read_from_disk(from_disk, file.name, run_time)
            # mem used by application
            self.memory.free -= from_disk

            # time to read from disk
            disk_read_time = self.storage.read(from_disk)
            run_time += disk_read_time
            self.memory.add_log(run_time)

            print("\tRead %d MB from disk in %.2f sec" % (from_disk, disk_read_time))

        return run_time

    def write(self, file, run_time=0):
        print("%.2f Start writing %s " % (run_time, file.name))
        self.memory.add_log(run_time)

        # ============= WRITE WITH MEMORY BW ===============
        # Write data before dirty_data is reached
        remaining_dirty = self.dirty_ratio * self.memory.get_available_memory() - self.memory.dirty

        mem_bw_amt = 0
        if remaining_dirty > 0:
            # Amount of data that makes dirty data reach dirty_ratio
            # Before this point, data is written to cache with memory bw
            # and dirty data is flushed to disk concurrently
            # max_free_amt = remaining_dirty * self.memory.write_bw / (self.memory.write_bw - self.storage.write_bw)
            max_free_amt = remaining_dirty

            # data written to cache with memory bandwidth
            mem_bw_amt = min(file.size, max_free_amt)
            self.evict(mem_bw_amt - self.memory.free)
            mem_bw_write_time = mem_bw_amt / self.memory.write_bw

            # periodically flush during cache write with memory bandwidth
            self.period_flush(run_time, mem_bw_write_time)

            self.memory.write(file.name, amount=mem_bw_amt, time=run_time)
            run_time += mem_bw_write_time

            self.memory.add_log(run_time)
            print("\tWrite to cache %d MB in %.2f sec" % (mem_bw_amt, mem_bw_write_time))

        disk_bw_amt = file.size - mem_bw_amt

        # ============= WRITE WITH DISK BW =============
        # Write dirty data after dirty_ratio is reached
        if disk_bw_amt > 0:
            # flush as much as we can because dirty data is full now
            # because now flushing and cache write can be concurrent,
            # it does not take time
            self.flush(disk_bw_amt)

            # evict as much as we can to get more free memory for written file
            self.memory.evict(disk_bw_amt - self.memory.free)

            # amount of data written and remained in cache after all remaining data is written
            # In case free memory is less than remaining amount, data is written, flushed and evicted right away
            # to accommodate unwritten data
            to_cache_amt = min(self.memory.free, disk_bw_amt)
            # to_disk_amt = throttled_amt - to_cache_amt

            disk_bw_write_time = self.storage.write(disk_bw_amt)
            # disk_write_time = to_disk_amt / self.storage.write_bw

            run_time += disk_bw_write_time
            self.memory.write(file.name, amount=to_cache_amt, time=run_time)

            self.memory.add_log(run_time)

            print("\tWrote with disk bw %d MB in %.2f sec" % (disk_bw_amt, disk_bw_write_time))

        print("%.2f File %s is written " % (run_time, file.name))

        return run_time

    def flush(self, amount):
        flushed_amt = self.memory.flush(amount=amount)
        return self.storage.write(flushed_amt)

    def period_flush(self, current_time, duration=0):
        """
        Periodical flushing
        :param duration:
        :param current_time: current simulated time
        :return: flushing time
        """
        flushed_amt = 0
        if current_time - self.last_pdflush > self.pdflush_interval:
            # update last flushing time
            self.last_pdflush += int((current_time - self.last_pdflush) / self.pdflush_interval) * self.pdflush_interval
            flushed_amt = self.memory.pdflush(self.last_pdflush, duration * self.storage.write_bw)

        return self.storage.write(flushed_amt)

    def evict(self, amount):
        if amount > 0:
            return self.memory.evict(amount)
        return 0

    def release(self, file):
        self.memory.free += file.size

    def compute(self, start_time, cpu_time=0):
        self.period_flush(start_time + cpu_time, cpu_time)
        return start_time + cpu_time

    def get_dirty_threshold(self):
        return self.memory.get_available_memory() * self.dirty_ratio

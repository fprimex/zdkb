## Client Side Expiration

The Couchbase Server caching layer is based upon memcached, and therefore
inherits many of the same capabilities and features of that technology.
One of these is support for expiration, otherwise known as time to live (TTL).

When writing data into memcached or Couchbase Server, the application can
optionally supply a time value that is used to determine how long a
particular item will be available for. That value can be supplied in
one of two ways. A value from 1-2592000 (seconds up to 30 days) will be
treated as a "relative" time. i.e., "write this item with TTL of 5"
will make the item unavailable in 5 seconds from the time it is written. 

Any value above 2592000 will be treated as a Unix timestamp. i.e., 
"write this item with TTL of 1357020000" will make the item unavailable 
on January 1st of 2013. Be aware that when a relative time is used, the item 
will be stored in memcached and Couchbase Server with the absolute time.

This is important to take into consideration from a backup and restore
perspective as any "relativeness" will be lost. See the documentation
for your particular client library at http://docs.couchbase.com/
for the best practices on using and setting TTLs within your application.

## Server Side Expiration

Within the standard memcached (and "memcached" buckets in Couchbase
Server), when the expiration time passes for a particular item, nothing
actually happens. The amount of CPU overhead would be far too great to
keep track of the potentially billions of items and each of their
expiration times. If nothing else happens, the item will remain within
memory.

There are two situations where it will be removed. If any access is generated
to the item (usually a 'get'), the TTL is first checked and if expired, a 
response of "NOT_FOUND" is sent back to the application as if the item never
existed in the first place.

The item is then removed from memory. This is known as "lazy expiration".
Secondly, as memory fills up within memcached, items will automatically
be evicted from memory. This will automatically remove both expired and
non-expired items based upon the incoming load.

In Couchbase buckets, the behavior is similar but slightly different as
well. Items are set with a TTL in the same manner, and the TTLs are
stored in the same manner. Additionally, any access to an already
expired item is treated the same "lazy" way. However, because there is
no eviction of data within Couchbase Server (because it is a database), we
cannot rely on memory pressure to clear out these items.

Thus, we have added an process that runs once-an-hour by default to purge 
these items from both RAM and disk. It performs a fast scan through the
memory space, deleting items from RAM and asynchronously removing them from
disk. This will not cause any performance impact. Additionally, it
runs on each node independently, so the process will be staggered
throughout the Couchbase Server cluster. Even before this process has run,
any items that have already expired will not be available to the application
due to the lazy expiration described above.

One other point to keep in mind is that even after an item has expired,
it is still counted within the server for item count and memory space
until it is actually removed (either lazily, via eviction for memcached
buckets or the hourly purger in Couchbase buckets).

On a Couchbase bucket, this expiration behavior can be monitored by
using our `cbstats` tool against a particular bucket on a particular node:

```
/opt/couchbase/bin/cbstats localhost:11210 all -b default | grep expir
ep_expired: 0
ep_item_flush_expired: 0
ep_num_expiry_pager_runs: 0
```

* The first stat (`ep_expired`) is how many items have been removed
  due to expiry through any process.
* The second (`ep_item_flush_expired`) describes how many items were
  removed due to expiry as they were being written to disk
* The last stat (`ep_num_expiry_pager_runs`) describes how many times
  the hourly pruger process has run

**Note**: These stats are up-to-date as of version 1.8.1 and there may
be additions in later version.

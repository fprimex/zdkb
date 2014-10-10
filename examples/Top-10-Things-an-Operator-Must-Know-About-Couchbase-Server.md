The bottom line for any sysadmin is to keep the database and in case of
Couchbase,**keeping the cluster up and running 24x7**. With demanding
app requirements, your cluster needs to be properly configured, sized
and monitored. This can be quite challenging as things can fail anytime
without any prior warning. As an operator, everyday is different - full
of surprises and challenges.

But, there are a few things every Couchbase Server operator must know.
We hope that the following 10 things will come in handy and make your
job easier:

### 1.  Keep your client libraries up-to-date

Always use the latest version of the client libraries compatible with
the server. By using the latest client libraries, you can get the most
out of your Couchbase cluster – recently tested code and the latest
features surfaced through the client.

### 2.  Monitor, monitor and monitor

By using the admin dashboard or the REST API’s, you can monitor how your
Couchbase cluster is doing. It is a good practice to monitor the
following system metrics - cache hit ratio, disk reads, resident item
ratio and disk write queue.

-   **Cache miss ratio**should be**low**. This means that document
    keys are cached in memory making reads and writes faster.
-   **Resident item ratio**shows the total number of active documents
    that reside in memory. Typically you want your working set (actively
    accessed documents) to be in memory for low latencies and an awesome
    user experience.
-   The**number of disk reads**will give you an idea of your disk I/O.
    It is good to keep this number**low**so that most reads are
    serviced out of RAM, which is faster.
-   The**disk write queue**will give you an idea of the number of
    items that need to be written to disk and the rate at which they are
    getting drained. If your disk writes queues are very high (millions
    of items) your cluster may not be sized accurately.

Here’s a[link to our REST
API.](http://www.couchbase.com/docs/couchbase-manual-2.0/couchbase-admin-restapi.html)

### 3.  Split data and index files across separate disk devices

For optimum performance, separate out data and index files on different
storage devices. By doing so, you would have sufficient disk I/O
bandwidth for performance intensive operations such as compaction
without any significant performance degradation.

Compaction is an important process that runs all the time to reclaim
space given the append-only architecture in Couchbase. It can also be
scheduled. Learn more about
compaction[here](http://blog.couchbase.com/compaction-magic-couchbase-server-20).

### 4.  Oh no! Rebalance failed?

[Rebalancing](http://blog.couchbase.com/rebalancing-couchbase-part-i)a
Couchbase cluster is a complicated operation. There are several reasons
why rebalance can be slow or fail. We have worked hard to make this
process more robust but if rebalance still fails – wait for around 5
minutes and restart the process again. There should be no impact to the
application since the cluster-map on the client is automatically updated
during rebalance.

Remember, not to click the rebalance button many times in a row - it
just restarts the process over again, wastes useful work that was done,
and sometimes can cause havoc.

### 5.  Remember that swap rebalance is better than regular rebalance

[Swap
Rebalance](http://www.couchbase.com/docs/couchbase-manual-2.0/couchbase-admin-tasks-addremove-rebalance-swap.html)optimizes
the movement of data when you are adding and removing the same number of
nodes in the same operation. Data is moved directly from the nodes
being removed to the nodes being added. This is more efficient than
standard rebalancing which would normally move data across the entire
cluster.

### 6.  Monitor the health of your system and integrate Couchbase with your ecosystem

If you’re already using an external monitoring system such as nagios to
monitor your infrastructure, you can plug-in your existing monitoring
system with Couchbase via the REST API. Couchbase Server can notify and
alert you so that you can check to ensure the health of your Couchbase
Server cluster . Some of them include:

* **IP Address Changes**If the IP address of a Couchbase Server in
  your cluster changes, you will be warned that the address is no
  longer available. You should check the IP address on the server, and
  update your clients or server configuration.

* **Metadata Overhead**Indicates that a bucket is now using more than
  50% of the allocated RAM for storing metadata and keys, reducing the
  amount of RAM available for data values. This is a helpful indicator
  that you may need to add nodes to your cluster.

* **Disk Usage**Indicates that the available disk space used for
  persistent storage has reached at least 90% of capacity. This is a
  signal that you may need to add more disks to your cluster.

Couchbase also has a rich ecosystem of adapters such as a[Hadoop
connector](http://www.couchbase.com/develop/connectors/hadoop)and
a[plug-in for
ElasticSearch](http://www.couchbase.com/elasticsearch-plug-in).

### 7.  Size your cluster appropriately for RAM, Disk and CPU

Prior to production, it is very[important to size your cluster and test
it
adequately](http://blog.couchbase.com/how-many-nodes-part-1-introduction-sizing-couchbase-server-20-cluster).
The sizing of your Couchbase cluster is going to be critical to its
stability and performance. For high-performance, your application will
want as many reads as possible coming out of cache, and the system to
have enough IO capacity to handle its writes. There needs to be enough
capacity in all the various areas to support everything else the system
is doing while maintaining the required level of performance.

### 8.  Data is replicated throughout the cluster. Optionally, indexes can be replicated as well.

Documents in Couchbase can be replicated to upto 3 times within a
cluster. The number of replicas (up to 3) can be configured through the
admin UI. Mutations of documents in-memory are replicated from the
active to the replica nodes. To query for a document, you can use
document ID and Couchbase will lookup the document using the primary
index. To query a subset of the data, you can use secondary indexes.
Replication of indexes in Couchbase is optional and can be configured
through the admin UI.

### 9.  Cross data center replication can be used for disaster recovery

 Couchbase XDCR allows you to replicate data across clusters.
Data access across clusters is eventually consistent. Make sure you
remember to size your clusters for XDCR as you will need double the
disk and I/O capacity as well as some more CPU.

### 10.  Tune indexing

When dealing with a large number of documents, there are couple of ways
you can index them. The first is to index all the documents from
scratch, which is a time consuming process. The other is to only update
the index for documents that have changed, which is an incremental
process. In Couchbase, indexes are built using incremental mapreduce
making the index update or build process efficient. As an admin, you can
tune the[number of indexes that can be built in
parallel](http://www.couchbase.com/docs/couchbase-manual-2.0/couchbase-admin-restapi-settings-maxparallelindexers.html),
or the tune the[time / interval between index
builds](http://www.couchbase.com/docs/couchbase-manual-2.0/couchbase-views-operation-autoupdate.html).
Try to group more views together in fewer number of design documents for
better performance. Some more[view best
practices](http://www.couchbase.com/docs/couchbase-manual-2.0/couchbase-views-writing-bestpractice.html)can
be found here.

**Just 10 things?**No, of course not! Couchbase is a NoSQL database
system and after you try it you will find that there’s a lot more you
will learn. If you feel that I missed something important that should be
added in the top 10 list, feel free to add them using the comments
below. Finally, if you haven’t read the best practice guidelines for
Couchbase Server 2.0, don’t forget to check them
out[here](http://www.couchbase.com/docs/couchbase-manual-2.0/couchbase-bestpractice.html).


Enjoy!

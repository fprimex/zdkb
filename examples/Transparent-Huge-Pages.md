Beginning with Red Hat Enterprise Linux (RHEL) version 6, a new method
of managing large amounts of memory called *huge pages* was implemented
in the operating system, along with an abstraction for automation and
management of huge pages called [*Transparent Huge Pages*
(THP)[1].](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Performance_Tuning_Guide/s-memory-transhuge.html)

Couchbase Engineering has determined that under some conditions,
**Couchbase Server can be negatively impacted by severe page allocation
delays when THP is enabled.** Couchbase therefore recommends that THP be
disabled on all Couchbase Server nodes per the Couchbase Server version
2.1.0 [release
notes[2]](http://www.couchbase.com/docs/couchbase-manual-2.1.0/couchbase-server-rn_2-1-0a.html).

## Check Status

You can check the current status of THP with the following command:


    cat /sys/kernel/mm/*transparent_hugepage/enabled

Output will resemble the following, with the current status marked in
[brackets]:

    [always] madvise never

*Always* indicates that THP will be used for all allocations, and
Couchbase recommends disabling THP in this instance.Note: Older kernels
may only show the *always* and*never* options.

You can check the current status of THP defrag with the following
command:

    cat /sys/kernel/mm/*transparent_hugepage/defrag

Output will resemble the following, where *always* is specified, meaning
that THP defrag is always enabled:


    [always] never


*Note: some distributions name the flag `transparent_hugepage`, others
`redhat_transparent_hugepage`, hence the wildcard).*

## Disabling THP

To permanently disable both THP and THP defrag, the preferred method is
to add the following to /etc/rc.local:


    for i in /sys/kernel/mm/*transparent_hugepage/enabled; do echo never > $i; done
    for i in /sys/kernel/mm/*transparent_hugepage/defrag; do echo never > $i; done


Alternatively, you can append the statement `transparent_hugepage=never`
to the kernel boot line in `/etc/grub.conf`, and this will disabled THP
but not THP defrag. This method can be used when it is not desirable to
maintain an `/etc/rc.local` file.

Either method will require a restart of the operating system.

You can also effect immediate disabling of THP and THP defrag with the
following commands, executed as root:


    for i in /sys/kernel/mm/*transparent_hugepage/enabled; do echo never > $i; done


For the above method, be aware that it only affects future processes,
however with THP disabled the OS will no longer allocate any new huge
pages and this will typically resolve most issues with Couchbase server.
**However we recommend you restart Couchbase Server afterwards to ensure
no huge pages are in use.** The safest manner to accomplish this is to
failover the node, make the changes to THP configuration, add the node
back to the cluster, and rebalance.

The above 2 commands only affect an immediate change to THP
configuration. You'll still need to use one of the previously mentioned
methods (using `rc.local` additions or adding statement to kernel boot
line in `/etc/grub.conf`) to persist the changes across reboots.

Once you've made the changes to disable THP and THP defrag, verify again
after the node is restarted that they are actually disabled:

    cat /sys/kernel/mm/*transparent_hugepage/enabled
    cat /sys/kernel/mm/*transparent_hugepage/defrag

The output from both commands should now reflect that THP and THP defrag
have been disabled by showing the selection of *never*:

    always madvise [never]

For more detailed information on THP, see [Transparent Hugepage
Support[3]](https://www.kernel.org/doc/Documentation/vm/transhuge.txt).

## Amazon AWS EC2

If you are deploying to Amazon AWS EC2 instances, keep in mind that
there are two types of instances with respect to their underlying
virtualization mechanisms, Hardware Virtualized Machine (HVM) and Para
Virtualized Machine (PVM). THP is only available on the following HVM
based EC2 instances:

* m3.xlarge
* m3.2xlarge
* cc2.8xlarge
* cr1.8xlarge
* hi1.4xlarge
* hs1.8xlarge
* cg1.4xlarge

If you are deploying Couchbase Server to any of the above instance
types, you should ensure that THP is disabled.

## References

1.  https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Performance_Tuning_Guide/s-memory-transhuge.html
2.  http://www.couchbase.com/docs/couchbase-manual-2.1.0/couchbase-server-rn_2-1-0a.html
3.  https://www.kernel.org/doc/Documentation/vm/transhuge.txt

History
-------

2014-02-12: Updated to cover `redhat_transparent_hugepage` variant.

2014-02-25 Updated to add note about EC2 instance types

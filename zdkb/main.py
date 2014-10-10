"""
zdkb: manage zendesk knowledgbases
"""

from __future__ import print_function

import os
import sys
import textwrap
import base64

import zdeskcfg
from zdesk import Zendesk

@zdeskcfg.configure(
    verbose=('verbose output', 'flag', 'v'),
    kb_dir=('directory containing the kb to upload',
                      'option', 'k', None, None, 'KB_DIR'),
    )
def zdkb(verbose=False,
        kb_dir=os.path.join(os.path.expanduser('~'), 'zdkb')):
    "Manage Zendesk knowledgbases"

    cfg = zdkb.getconfig()

    if cfg['zdesk_url'] and cfg['zdesk_email'] and cfg['zdesk_password']:
        if verbose:
            print('Configuring Zendesk with:\n'
                  '  url: {}\n'
                  '  email: {}\n'
                  '  token: {}\n'
                  '  password: (hidden)\n'.format( cfg['zdesk_url'],
                                                   cfg['zdesk_email'],
                                                   repr(cfg['zdesk_token']) ))
        zd = Zendesk(**cfg)
    else:
        msg = textwrap.dedent("""\
            Error: Need Zendesk config to continue.

            Config file (~/.zdeskcfg) should be something like:
            [zdesk]
            url = https://example.zendesk.com
            email = you@example.com
            password = dneib393fwEF3ifbsEXAMPLEdhb93dw343
            token = 1

            [kb]
            kb_dir = /path/to/kb_dir
            """)
        print(msg)
        return 1

    # Log the cfg
    if verbose:
        print('Running with zdkb config:\n'
              ' verbose: {}\n'
              ' kb_dir: {}\n'.format(verbose, kb_dir))

    # Save the current directory so we can go back once done
    start_dir = os.getcwd()

    # Normalize all of the given paths to absolute paths
    kb_dir = os.path.abspath(kb_dir)

    # Check for and create working directory
    if not os.path.isdir(work_dir):
        print('kb_dir does not exist: {}'.format(kb_dir))
        return None

    return None

    # Change to working directory to begin file output
    #os.chdir(kb_dir)

#    if tickets:
#        # tickets given, query for those
#        q = ' '.join(['ticket_id:' + s for s in map(str,tickets)])
#    else:
#        # List of tickets not given. Get all of the attachments for all of this
#        # user's open tickets.
#        q = 'status<solved assignee:{}'.format(agent)
#
#    if verbose:
#        print('Retrieving tickets page 1')
#
#    response = zd.search(query=q)
#
#    if response['count'] == 0:
#        # No tickets from which to get attachments
#        print("No tickets provided for attachment retrieval.")
#        return {}
#
#    results = response['results']
#    page = 1
#    while response['next_page'] != None:
#        page += 1
#
#        if verbose:
#            print('Retrieving tickets page {}'.format(page))
#
#        response = zd.search(query=q, page=page)
#        results.extend(response['results'])
#
#    # Fix up some headers to use for downloading the attachments.
#    # We're going to borrow the zdesk object's httplib client.
#    headers = {}
#    if zd.zdesk_email is not None and zd.zdesk_password is not None:
#        headers["Authorization"] = "Basic {}".format(
#            base64.b64encode(zd.zdesk_email.encode('ascii') + b':' +
#                             zd.zdesk_password.encode('ascii')))
#
#    # Get the attachments from the given zendesk tickets
#    for ticket in results:
#        if ticket['result_type'] != 'ticket':
#            # This is not actually a ticket. Weird. Skip it.
#            continue
#
#        if verbose:
#            print('Ticket {}'.format(ticket['id']))
#
#        ticket_dir = os.path.join(work_dir, str(ticket['id']))
#        ticket_com_dir = os.path.join(ticket_dir, 'comments')
#        comment_num = 0
#
#        if verbose:
#            print('Retrieving audits page {}'.format(page))
#
#        response = zd.ticket_audits(ticket_id=ticket['id'])
#        audits = response['audits']
#        page = 1
#        while response['next_page'] != None:
#            page += 1
#
#            if verbose:
#                print('Retrieving audits page {}'.format(page))
#
#            response = zd.ticket_audits(ticket_id=ticket['id'], page=page)
#            audits.extend(response['audits'])
#
#        for audit in audits:
#            for event in audit['events']:
#                if event['type'] != 'Comment':
#                    # This event isn't a comment. Skip it.
#                    continue
#
#                comment_num += 1
#                comment_dir = os.path.join(ticket_com_dir, str(comment_num))
#
#                if verbose and event['attachments']:
#                    print('Comment {}'.format(comment_num))
#
#                for attachment in event['attachments']:
#                    name = attachment['file_name']
#                    if os.path.isfile(os.path.join(comment_dir, name)):
#                        if verbose:
#                            print('Attachment {} already present'.format(name))
#                        continue
#
#                    # Get this attachment
#                    if verbose:
#                        print('Attachment {}'.format(name))
#
#                    # Check for and create the download directory
#                    if not os.path.isdir(comment_dir):
#                        os.makedirs(comment_dir)
#
#                    os.chdir(comment_dir)
#                    response, content = zd.client.request(attachment['content_url'], headers=headers)
#                    if response['status'] != '200':
#                        print('Error downloading {}'.format(attachment['content_url']))
#                        continue
#
#                    with open(name, 'wb') as f:
#                        f.write(content)
#
#                    # Check for and create the grabs entry to return
#                    if ticket_dir not in grabs:
#                        grabs[ticket_dir] = []
#
#                    grabs[ticket_dir].append(
#                        os.path.join('comments', str(comment_num), name) )
#
#                    # Let's try to extract this if it's compressed
#                    zdsplode(name, verbose=verbose)

#    os.chdir(start_dir)
#    return grabs


def main(argv=None):
    zdeskcfg.call(zdkb, section='zdkb')
    return 0


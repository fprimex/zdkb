"""
zdkb: manage zendesk knowledgbases
"""

from __future__ import print_function

import os
import sys
import textwrap
import simplejson as json

import zdeskcfg
from zdesk import Zendesk

@zdeskcfg.configure(
    verbose=('verbose output', 'flag', 'v'),
    listing=('print listing of a forum. use "all" to list everything',
                      'option', 'l', None, None, '(FORUM_ID|all)'),
    fetch=('download the Zendesk KB to KB_DIR', 'flag', 'f'),
    kb_dir=('directory containing the kb to upload',
                      'option', 'k', None, None, 'KB_DIR'),
    )
def zdkb(verbose=False,
        listing=None,
        fetch=False,
        kb_dir=os.path.join(os.path.expanduser('~'), 'zdkb')):
    "Manage Zendesk knowledgbases"

    cfg = zdkb.getconfig()

    # Log the cfg
    if verbose:
        print('Running with zdkb config:\n'
              ' verbose: {}\n'
              ' listing: {}\n'
              ' kb_dir: {}\n'.format(verbose, listing, kb_dir))

    #if state['categories'] or state['topics'] or state['forums'] or state['list_zdf']:
    if listing or fetch:
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

                Config file (e.g. ~/.zdf2pdf.cfg) should be something like:
                [zdf2pdf]
                url = https://example.zendesk.com
                mail = you@example.com
                password = dneib393fwEF3ifbsEXAMPLEdhb93dw343
                is_token = 1
                """)
            print(msg)
            msg = textwrap.dedent("""\
                Error: Need Zendesk config for requested operation.

                Config file (~/.zdeskcfg) should be something like:
                [zdesk]
                url = https://example.zendesk.com
                email = you@example.com
                password = dneib393fwEF3ifbsEXAMPLEdhb93dw343
                token = 1

                [zdkb]
                kb_dir = /path/to/kb_dir
                """)
            print(msg)
            return 1

    # If any listing was requested we will do that and exit, regardless of
    # any other supplied options.
    if listing == 'all':
        # List available zendesk forums with their IDs and titles and exit.
        # Listing is formatted like for following:
        # 12345 Category 1 name
        #     09876 Forum 1 name
        #     54321 Forum 2 name
        # 67890 Category 2 name
        if verbose:
            print('Listing all forums')

        response = zd.forums_list(get_all_pages=True)
        forums = response['forums']
        cat_ids = set(f['category_id'] for f in forums)

        categories = zd.categories_list(get_all_pages=True)

        for cat_id in cat_ids:
            if cat_id:
                try:
                    cat_name = next(c['name'] for c in categories
                                                if c['id'] == cat_id)
                except StopIteration:
                    cat_name = 'None'
            else:
                cat_id = 'None'
                cat_name = 'None'
            print('{} ({})'.format(cat_name, cat_id))

            for forum in forums:
                if repr(forum['category_id']) == cat_id:
                    print('    {} ({})'.format(forum['name'], forum['id']))
        return 0

    elif listing:
        if verbose:
            print('Listing all entries in forum {}'.format(listing))

        # List a zendesk forum's entries with their titles and IDs and exit
        try:
            forum_id = int(listing)
        except ValueError:
            print('Error: Could not convert to integer: {}'.format(listing))
            return 1

        entries = zd.forum_topics(id=listing, get_all_pages=True)
        for entry in entries['topics']:
            print('{} ({})'.format(entry['title'], entry['id']))
        return 0

    # Save the current directory so we can go back once done
    start_dir = os.getcwd()

    # Normalize all of the given paths to absolute paths
    kb_dir = os.path.abspath(kb_dir)

    # Check for and create working directory
    if not os.path.isdir(kb_dir):
        print('kb_dir does not exist: {}'.format(kb_dir))
        return 1

    if fetch:
        # Change to working directory to begin file output
        os.chdir(kb_dir)

        response = zd.forums_list(get_all_pages=True)
        forums = response['forums']

        response = zd.categories_list(get_all_pages=True)
        categories = response['categories']

        response = zd.topics_list(get_all_pages=True)
        topics = response['topics']

        with open('categories', 'w') as cat_file:
            json.dump(categories, cat_file)

        for forum in forums:
            forum_name = forum['name'].replace('/', '-')

            if not os.path.isdir(forum_name):
                os.mkdir(forum_name)

            os.chdir(forum_name)

            with open(forum_name + '.json', 'w') as forum_json:
                json.dump(forum, forum_json)

            os.chdir(kb_dir)

        for topic in topics:
            try:
                forum_name = next(f['name'] for f in forums
                                            if f['id'] == topic['forum_id'])
            except StopIteration:
                forum_name = 'None'

            forum_name = forum_name.replace('/', '-')

            if not os.path.isdir(forum_name):
                os.mkdir(forum_name)

            os.chdir(forum_name)

            topic_filename = topic['title'].replace('/', '-')

            with open(topic_filename + '.html', 'w') as topic_html:
                topic_html.write(topic['body'])

            with open(topic_filename + '.json', 'w') as topic_json:
                del topic['body']
                json.dump(topic, topic_json)

            os.chdir(kb_dir)

        return 0
    return 0


def main(argv=None):
    zdeskcfg.call(zdkb, section='zdkb')
    return 0


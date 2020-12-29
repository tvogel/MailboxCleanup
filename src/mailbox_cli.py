#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module to download and to detach/strip/remove attachments
from e-mails on IMAP servers.
"""

from __future__ import print_function

import argparse
import logging
import os

from src.mailbox_imap import MailboxCleanerIMAP


__author__ = "Alexander Willner"
__copyright__ = "Copyright 2020, Alexander Willner"
__credits__ = ["github.com/guido4000",
               "github.com/halteproblem", "github.com/jamesridgway"]
__license__ = "MIT"
__version__ = "1.0.2"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"


def handle_arguments() -> argparse.ArgumentParser:
    """Provide CLI handler for application."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all",
                        help="iterate over all folders",
                        action='store_true')
    parser.add_argument("-d", "--detach",
                        help="remove attachments",
                        action='store_true')
    parser.add_argument("-k", "--skip-download",
                        help="don't download attachments",
                        action='store_true')
    parser.add_argument("-c", "--reset-cache",
                        help="reset cache",
                        action='store_true')
    parser.add_argument("-r", "--read-only",
                        help="read-only mode for the imap server",
                        action='store_true')
    parser.add_argument("-m", "--min-size",
                        help="min attachment size in KB",
                        default=200, type=int)
    parser.add_argument("-f", "--folder",
                        help="imap folder to process", default="Inbox")
    parser.add_argument("-l", "--upload",
                        help="local folder with messages to upload")
    parser.add_argument("-t", "--target",
                        help="download attachments to this local folder",
                        default="attachments")
    parser.add_argument("-s", "--server", help="imap server", required=True)
    parser.add_argument("-u", "--user", help="imap user", required=True)
    parser.add_argument("-o", "--port", help="imap port", required=False,
                        type=int)
    parser.add_argument("-p", "--password", help="imap user", required=True)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbosity",
        help="be more verbose (-v, -vv)")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING - args.verbosity * 10,
                        format="%(message)s")

    return args


def main():
    """Setup and run remover."""

    args = handle_arguments()
    args.target = os.path.expanduser(
        args.target) if args.target is not None else None
    args.upload = os.path.expanduser(
        args.upload) if args.upload is not None else None
    imap = MailboxCleanerIMAP(args)

    # todo: repeat here a couple of times  pylint: disable=W0511
    try:
        imap.login()
        logging.warning('Server\t\t: %s@%s', args.user, args.server)
        logging.warning('Read Only\t: %s', args.read_only)
        logging.warning('Detach\t\t: %s', args.detach)
        logging.warning('Cache Enabled\t: %s', not args.reset_cache)
        logging.warning('Download\t: %s', not args.skip_download)
        logging.warning('Min Size\t: %s KB', args.min_size)
        logging.warning('Target\t\t: %s', args.target)
        logging.warning('Upload\t\t: %s', args.upload)
        logging.warning('All Folders\t: %s', args.all)

        if args.upload:
            imap.process_directory()
        else:
            imap.process_folders()
    except KeyboardInterrupt as error:
        raise SystemExit('\nCancelling...') from error
    finally:
        imap.cleanup()
        imap.logout()


if __name__ == '__main__':
    main()

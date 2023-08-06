# -*- coding: utf-8 -*-
import os
import argparse
from labelci import Dataset
from argparse import RawTextHelpFormatter
import configparser

from labelci.bin.utils import print_


def label_cli():
    parser = argparse.ArgumentParser(description="labelci", formatter_class=RawTextHelpFormatter)
    parser.add_argument("command", help="""project    Project Information
task    Task Information， '--project' is a required parameter
data    Data version Information, '--project' is a required parameter
""")
    parser.add_argument("--data-version", help="Get data version by project id")

    parser.add_argument("--url", help="Label hub url")
    parser.add_argument("--token", help="Label hub access token")

    parser.add_argument("--id", help="""list    Get a data list that you"ve created, input "list"
id    Get data by id, input id, example 1023. 
""")

    parser.add_argument("--checkout", help="Switch to a version of the project by data version")
    parser.add_argument("--project", help="The project ID field is required to get the Task/Data Version List")
    args = parser.parse_args()

    url = None
    token = None

    if os.path.exists('config.ini'):
        conf = configparser.ConfigParser()
        conf.read("config.ini")
        url = conf.get('client', 'url')
        token = conf.get('client', 'token')
    url = args.url if args.url else url
    token = args.token if args.token else token
    if not url or not token:
        return "labelci: error: the following arguments are required: --url, --token"

    if args.command == "project":
        id_ = args.id if args.id else "list"
        if id_ == "list":
            dataset = Dataset(url, token).list()
        else:
            if args.checkout:
                dataset = Dataset(url, token).show_tasks(id_, args.checkout)
            dataset = Dataset(url, token).show_tasks(id_)
        print_(dataset)
        return

    elif args.command == "task":
        id_ = args.id if args.id else "list"
        if id_ == "list":
            if not args.project:
                return "labelci: error: the following arguments are required: --project"
            dataset = Dataset(url, token).show_tasks(args.project)
        else:
            dataset = Dataset(url, token).detail_tasks(id_)
        print_(dataset)
        return

    elif args.command == "data":
        if not args.project:
            return "labelci: error: the following arguments are required: --project"
        data = Dataset(url, token).data_version(args.project)
        print_(data)
        return

    # elif args.command == "data-version":
    #     pass
    #     # dataset


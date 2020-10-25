import argparse

from actions import VersionCreator, ConfigReader, RepositoryCreator
from repo import Repo
from utils import ConfigParser
from version import Version, VersionError


def run_tag_creator(args: argparse.Namespace):
    print(">>> Reading config file...")
    if args.conf is None:
        args.conf = ConfigParser.parse()
    print(">>> Config file read : {}".format(args.conf))

    print(">>> Configuring repository...")
    if args.repo is None:
        args.repo = Repo(args.conf["repo"]["path"])
    print(">>> Repository configured : {}".format(args.repo))

    if args.environment is None:
        args.environment = args.conf["default"]["environment"]
    elif args.environment not in args.conf["environment"]:
        print(">>> Environment couldn't be found on config : {}".format(args.environment))
        exit(-1)
    print(">>> Environment configured : {}".format(args.environment))

    if args.branch is None:
        args.branch = args.conf["environment"][args.environment]["branch"]

    if args.commit:
        print(">>> Checking out to {}...".format(args.commit))
        if args.repo.checkout(commit=args.commit):
            print(">>> Check out completed!")
        else:
            exit(-1)
    else:
        print(">>> Checking out to {}...".format(args.branch))
        if args.repo.checkout(branch=args.branch):
            print(">>> Check out completed!")
        else:
            exit(-1)

    if args.fetch:
        print(">>> Fetching...")
        if args.repo.fetch():
            print(">>> Fetch completed!")
        else:
            exit(-1)
    else:
        print(">>> Fetch not set, skipping fetch!")

    if args.pull:
        print(">>> Pulling...")
        if args.repo.pull(branch=args.branch):
            print(">>> Pull completed!")
        else:
            exit(-1)
    else:
        print(">>> Pull not set, skipping pull!")

    if args.tag:
        new_tag = args.tag
    else:
        tag_config = args.conf["environment"][args.environment]["tag"]
        print(">>> Environment configuration read for tag limits : {}".format(tag_config))
        prefix, *_ = tag_config.values()
        max_values = {k: v for k, v in tag_config.items() if k.startswith("max")}
        base_ver = Version(**max_values)
        tags = []
        print(">>> Reading existing tags for environment...")
        for tag in args.repo.tags():
            if tag.startswith(prefix):
                try:
                    tags.append(base_ver.parse(tag))
                except VersionError as err:
                    print(">>> Tag exceeds configured environment tag limits({}) : {}".format(base_ver.maximum(), tag))
                    print(err)
        new_tag = max(tags).next()
    print(">>> New tag : {}".format(new_tag))
    if args.repo.create_tag(tag_name=str(new_tag), commit=args.commit):
        print(">>> Tag created : {}".format(str(new_tag)))
    else:
        print(">>> Tag couldn't be created!")
        exit(-1)

    if args.push:
        print(">>> Pushing...")
        if args.repo.push(branch=args.branch):
            print(">>> Push completed!")
        else:
            exit(-1)
    else:
        print(">>> Push not set, skipping push!")


def initialize():
    parser = argparse.ArgumentParser(prog="crtag", description="TAG CREATOR", epilog="Makes it easy to create tags.")
    parser.add_argument("-r", "--repo", help="git repository", action=RepositoryCreator)
    parser.add_argument("-t", "--tag", help="tag name to create (default: next tag for branch)", action=VersionCreator)
    parser.add_argument("-cf", "--conf", help="config file for creating tag", action=ConfigReader)
    parser.add_argument("-pl", "--pull", help="pull branch before creating tag", action=argparse.BooleanOptionalAction,
                        default=True)
    parser.add_argument("-ps", "--push", help="push branch after creating tag", action=argparse.BooleanOptionalAction,
                        default=True)
    parser.add_argument("-f", "--fetch", help="fetch all tags", action=argparse.BooleanOptionalAction,
                        default=True)
    parser.add_argument("-c", "--commit", help="commit hash to create tag on")
    parser.add_argument("-b", "--branch", help="branch to create tag")
    parser.add_argument("-env", "--environment", help="environment to create tag")
    return parser.parse_args()


if __name__ == "__main__":
    args = initialize()
    run_tag_creator(args)

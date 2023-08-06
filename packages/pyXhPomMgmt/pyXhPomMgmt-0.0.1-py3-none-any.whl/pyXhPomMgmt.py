# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
from POMREPOS import POMRepos
import ScanDir

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Maven POM management utility')
    parser.add_argument('--pom-paths', dest="pom_paths", type=str, nargs="+", const=None, default=None)
    parser.add_argument('--filter', dest="filter", type=str, const=None, default=None)
    parser.add_argument('--skip-path-with', dest="skip_path_with", nargs="+", type=str, const=None, default=None)

    # o = parser.parse_args(r"--pom-paths C:\Users\01731363\Documents --filter abc --skip-path-with target".split())
    o = parser.parse_args()

    if o.pom_paths is None or o.filter is None:
        if o.pom_paths is None:
            raise Exception("Missing --pom-paths")
        elif o.filter is None:
            raise Exception("Missing --filter")

    # print(
    #     o
    # )
    repos = POMRepos()
    for path in o.pom_paths:
        ScanDir.scan(path, repos, o.skip_path_with)

    for item in repos.pom_dict:
        print(repos.pom_dict[item].to_dep().full_name())


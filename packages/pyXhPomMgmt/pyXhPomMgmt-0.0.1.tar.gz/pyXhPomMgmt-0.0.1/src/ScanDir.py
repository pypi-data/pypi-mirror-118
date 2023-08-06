import os
from POM import POM
from POMREPOS import POMRepos


def scanMultiple(base_pom_paths: [str], repos: POMRepos = POMRepos(), skip_path_with: [str] = []) -> POMRepos:
    for path in base_pom_paths:
        scan(path, repos, skip_path_with)
    return repos


def scan(base_pom_path: str, repos: POMRepos = POMRepos(), skip_path_with: [str] = []) -> POMRepos:
    pom_xml_list = []

    def contain(test: str):
        for word in skip_path_with:
            if word in test:
                return True
            continue
        return False

    for root, dirs, files in os.walk(base_pom_path):
        if contain(root):
            continue
        for file in files:
            if file == "pom.xml":
                pom_xml_list.append(os.path.join(root, file))

    list_of_pom_instances = list(map(lambda a: POM(a), pom_xml_list))

    for pom in list_of_pom_instances:
        if not repos.has_pom(pom):
            if not repos.add_pom(pom):
                raise Exception("fail to add repo: " + pom.to_dep().full_name())

    return repos

from POM import POM


class POMRepos:
    pom_dict: dict[POM]

    def __init__(self):
        self.pom_dict = {}

    def __str__(self) -> str:
        return "\n".join([str(self.pom_dict[index].to_dep().full_name()) for index in self.pom_dict])

    def __repr__(self) -> str:
        return self.__str__()

    def has_pom(self, pom: POM):
        return True if str(pom) in self.pom_dict else False

    def add_pom(self, pom: POM) -> bool:
        if self.has_pom(pom):
            return False
        else:
            self.pom_dict[pom.to_dep().simple_name()] = pom
            return True

    def get_pom_list(self):
        return list(map(lambda pom_name: self.pom_dict[pom_name], self.pom_dict))

    def find_dep(self, dep: str) -> []:
        # print("finding: %s"%dep)
        result = []
        dep_found_list = list(filter(lambda pom: self.pom_dict[pom].to_dep().simple_name() == dep, self.pom_dict))
        if len(dep_found_list) == 0:
            return []

        dep_found = self.pom_dict[dep_found_list[0]]
        if dep_found.has_parent:
            result += self.find_dep(dep_found.parent)

        for d in dep_found.dependencies:
            result += self.find_dep(dep_found.dependencies[d].simple_name())

        result += [dep_found]

        return result

import xml.etree.ElementTree as ET

from Dependency import Dependency

ns: str = "{http://maven.apache.org/POM/4.0.0}"


class POM:
    # path: str
    # artifact_id: str
    # group_id: str
    # version: str
    # has_parent: bool
    # props = {}
    # dependencies = {}
    # parent: Dependency
    # root: ET

    def __init__(self, path: str):
        self.path = path
        self.root = ET.parse(path)
        self.artifact_id: str
        self.group_id: str
        self.version: str
        self.has_parent: bool
        self.props: dict = {}
        self.dependencies: dict = {}
        self.parent: Dependency

        self.extract_parent()
        self.extract_props()
        self.extract_dependencies()

        if self.root.find(ns + "groupId") is None and not self.has_parent:
            raise Exception("[%s] group id can't be found" % path)
        elif self.root.find(ns + "groupId") is not None:
            self.group_id = self.root.find(ns + "groupId").text

        if self.root.find(ns + "artifactId") is None:
            raise Exception("[%s] artifact id can't be found" % path)
        self.artifact_id = self.root.find(ns + "artifactId").text
        if self.root.find(ns + "version") is None and self.has_parent == False:
            raise Exception("[%s] version can't be found" % path)
        elif self.root.find(ns + "version") is not None:
            self.version = self.root.find(ns + "version").text

    def extract_parent(self):
        if self.root.find(ns + "parent") is None:
            self.has_parent = False
        else:
            self.has_parent = True
            self.group_id = self.root.find(ns + "parent").find(ns + "groupId").text
            artifact_id = self.root.find(ns + "parent").find(ns + "artifactId").text
            self.version = self.root.find(ns + "parent").find(ns + "version").text
            self.parent = Dependency(self.group_id, artifact_id, self.version, 'compile')

    def extract_props(self):
        property_entries = self.root.find(ns + "properties")
        if property_entries is not None:
            for child in property_entries:
                self.props[child.tag.replace(ns, "")] = child.text

    def extract_dependencies(self):
        dependencies_entries = self.root.find(ns + "dependencies")
        if dependencies_entries is not None:
            for child in dependencies_entries:
                if child.find(ns + 'groupId') is not None:
                    group_id = child.find(ns + 'groupId').text
                else:
                    group_id = None
                if child.find(ns + 'artifactId') is not None:
                    artifact_id = child.find(ns + 'artifactId').text
                else:
                    artifact_id = None
                if child.find(ns + 'version') is not None:
                    version = child.find(ns + 'version').text
                else:
                    version = None
                if child.find(ns + 'scope') is not None:
                    scope = child.find(ns + 'scope').text
                else:
                    scope = 'compile'
                dep = Dependency(group_id, artifact_id, version, scope)
                self.dependencies[str(dep)] = dep

    def to_dep(self) -> Dependency:
        return Dependency(self.group_id, self.artifact_id, self.version, "compile")

    def full_description(self) -> str:
        props = "\n  properties:\n" + "\n".join(["    %s:%s " % (index, self.props[index]) for index in self.props])
        deps = "\n dependencies:\n" + "\n".join(
            ["    %s" % self.dependencies[index].full_name() for index in self.dependencies])
        return "%s:%s:%s" % (self.group_id, self.artifact_id, self.version) + props + deps

    def __str__(self) -> str:
        return str(self.to_dep().full_name())

    def __repr__(self) -> str:
        return self.__str__()

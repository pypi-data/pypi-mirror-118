class Dependency:
    group_id: str
    artifact: str
    version: str
    scope: str

    def __init__(self, group_id, artifact, version, scope):
        self.group_id = group_id
        self.artifact = artifact
        self.version = version
        self.scope = scope

    def simple_name(self):
        return "%s:%s" % (self.group_id, self.artifact)

    def full_name(self):
        return "%s:%s:%s" % (self.group_id, self.artifact, self.version if self.version is not None else "[Unknown]")

    def __str__(self) -> str:
        return self.simple_name()

    def __repr__(self) -> str:
        return self.__str__()

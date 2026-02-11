from uuid import UUID


class DomainException(Exception):
    pass


class ProjectNotFound(DomainException):
    def __init__(self, project_id: UUID) -> None:
        self.project_id = project_id
        super().__init__(f"Project not found: project_id={project_id}")


class AlreadyGenerated(DomainException):
    def __init__(self, project_id: UUID) -> None:
        self.project_id = project_id
        super().__init__(f"Project already generated: project_id={project_id}")


class NotYetGenerated(DomainException):
    def __init__(self, project_id: UUID) -> None:
        self.project_id = project_id
        super().__init__(f"Project not yet generated: project_id={project_id}")

from typing import List

from sqlalchemy.orm import Session

from paretos.database.enums import ProjectStatusEnum

from .database_factory import DatabaseFactory


class ProjectMapper:
    """
    Maps SQLite data structure to dashboard API project response.

    Ignores the SQLAlchemy data model and it's relations for performance reasons.
    """

    def __init__(self, database_factory: DatabaseFactory):
        self.__database_factory = database_factory

    def load_project_data(self) -> List[dict]:
        database = self.__database_factory.get_connection()

        query = """
        SELECT
            project.id AS id,
            project.name AS name,
            project_status.name AS status,
            COUNT(DISTINCT simulation.id) AS nr_pareto
        FROM project
        LEFT JOIN simulation
            ON project.id = simulation.project_id AND simulation.is_pareto IS TRUE
        LEFT JOIN project_parameters
            ON project.id = project_parameters.project_id
        LEFT JOIN `parameter`
            ON `parameter`.id = project_parameters.parameter_id
        LEFT JOIN parameter_type
            ON parameter_type.id = `parameter`.parameter_type_id
        LEFT JOIN project_status
            ON project.statusCodeId = project_status.id
        WHERE parameter_type.name = 'kpi'
        GROUP BY project.id
        ORDER BY project.time_created DESC
        """

        session = database.begin()

        db_response = session.execute(query)

        targets_by_project_ids = self.__get_kpi_names_by_project_ids(session=session)

        project_data = []

        for row in db_response:
            project_id = row["id"]
            name = row["name"]
            targets = []

            if project_id in targets_by_project_ids:
                targets = targets_by_project_ids[project_id]
                targets.sort()

            uuid = row["id"]
            nr_pareto = row["nr_pareto"]
            status = 100.0 if row["status"] == ProjectStatusEnum.set.value else 0.0

            project_item = {
                "id": uuid,
                "description": None,
                "name": name,
                "targets": targets,
                "status": status,
                "number_pareto": nr_pareto,
            }

            project_data.append(project_item)

        session.close()

        return project_data

    def __get_kpi_names_by_project_ids(self, session: Session):

        query = """
        SELECT
            project_parameters.project_id AS project_id,
            `parameter`.name AS parameter_name
        FROM project_parameters
        LEFT JOIN `parameter`
            ON project_parameters.parameter_id = `parameter`.id
        LEFT JOIN parameter_type
            ON parameter_type.id = `parameter`.parameter_type_id
        WHERE parameter_type.name = 'kpi'
        """

        db_response = session.execute(query)

        result = {}

        for row in db_response:
            project_id = row["project_id"]
            parameter_name = row["parameter_name"]

            if project_id not in result:
                result[project_id] = []

            result[project_id].append(parameter_name)

        return result

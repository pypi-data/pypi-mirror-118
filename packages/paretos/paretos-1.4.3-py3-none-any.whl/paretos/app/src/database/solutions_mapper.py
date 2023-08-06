from typing import List

from ....database.enums import ParameterTypes
from .database_factory import DatabaseFactory


class SolutionsMapper:
    """
    Maps SQLite data structure to dashboard API solutions response.

    Ignores the SQLAlchemy data model and it's relations for performance reasons.
    """

    def __init__(self, database_factory: DatabaseFactory):
        self.__database_factory = database_factory

    def load_solutions(self, project_id: str, only_pareto=False) -> List[dict]:
        database = self.__database_factory.get_connection()

        query = """
        SELECT
            simulation_values.simulation_id AS simulation_id,
            parameter_value.parameter_id AS parameter_id,
            parameter_type.name AS parameter_type,
            parameter_value.number_value AS parameter_value,
        FROM simulation_values
        LEFT JOIN simulation
            ON simulation_values.simulation_id = simulation.id
        LEFT JOIN parameter_value
            ON parameter_value.id = simulation_values.parameter_value_id
        LEFT JOIN `parameter`
            ON `parameter`.id = parameter_value.parameter_id
        LEFT JOIN parameter_type
            ON parameter_type.id = `parameter`.parameter_type_id
        WHERE simulation.project_id = :project_id
        ORDER BY simulation.time_created ASC
        """

        if only_pareto:
            query = """
            SELECT
                simulation_values.simulation_id AS simulation_id,
                parameter_value.parameter_id AS parameter_id,
                parameter_type.name AS parameter_type,
                parameter_value.number_value AS parameter_value,
                simulation.is_pareto AS is_pareto
            FROM simulation_values
            LEFT JOIN simulation
                ON simulation_values.simulation_id = simulation.id
            LEFT JOIN parameter_value
                ON parameter_value.id = simulation_values.parameter_value_id
            LEFT JOIN `parameter`
                ON `parameter`.id = parameter_value.parameter_id
            LEFT JOIN parameter_type
                ON parameter_type.id = `parameter`.parameter_type_id
            WHERE simulation.project_id = :project_id
                AND simulation.is_pareto IS TRUE
            ORDER BY simulation.time_created ASC
            """

        session = database.begin()

        db_response = session.execute(query, {"project_id": project_id})

        evaluation_id_order = []
        evaluations = {}

        for row in db_response:
            simulation_id = row["simulation_id"]
            parameter_id = row["parameter_id"]
            parameter_type = row["parameter_type"]
            parameter_value = row["parameter_value"]

            # We need to raise exceptions because we can not trust the database
            # and want the error to be traceable and understandable.

            if simulation_id not in evaluations:
                evaluation_id_order.append(simulation_id)
                evaluations[simulation_id] = {
                    "id": simulation_id,
                    "design": [],
                    "kpis": [],
                }

            if parameter_type == ParameterTypes.design.value:
                evaluations[simulation_id]["design"].append(
                    {"id": parameter_id, "value": parameter_value}
                )
            elif parameter_type == ParameterTypes.kpi.value:
                evaluations[simulation_id]["kpis"].append(
                    {"id": parameter_id, "value": parameter_value}
                )
            else:
                raise ValueError("Unexpected parameter type in database.")

        response_evaluations = []

        for evaluation_id in evaluation_id_order:
            response_evaluations.append(evaluations[evaluation_id])

        session.close()

        return response_evaluations

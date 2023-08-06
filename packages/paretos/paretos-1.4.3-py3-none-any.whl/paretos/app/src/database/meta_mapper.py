from sqlalchemy.orm import Session

from ....database.enums import ContinuityOptions, ParameterOptions, ParameterTypes
from .database_factory import DatabaseFactory


class MetaMapper:
    """
    Maps SQLite data structure to dashboard API meta response.

    Ignores the SQLAlchemy data model and it's relations for performance reasons.
    """

    def __init__(self, database_factory: DatabaseFactory):
        self.__database_factory = database_factory

    def load_meta(self, project_id: str) -> dict:
        database = self.__database_factory.get_connection()

        query = """
        SELECT
            `parameter`.id AS parameter_id,
            `parameter`.name AS parameter_name,
            parameter_type.name AS parameter_type
        FROM
            project_parameters
        LEFT JOIN `parameter`
            ON project_parameters.parameter_id = `parameter`.id
        LEFT JOIN parameter_type
            ON parameter_type.id = `parameter`.parameter_type_id
        WHERE project_id = :project_id
        ORDER BY `parameter`.name ASC
        """

        session = database.begin()

        options = self.__load_options(project_id=project_id, session=session)

        db_response = session.execute(query, {"project_id": project_id})

        design_parameter_definitions = []
        kpi_parameter_definitions = []

        for row in db_response:
            parameter_id = row["parameter_id"]
            parameter_name = row["parameter_name"]
            parameter_type = row["parameter_type"]

            item = {"id": parameter_id, "name": parameter_name}

            # We need to raise exceptions because we can not trust the database
            # and want the error to be traceable and understandable.

            if parameter_id not in options:
                raise ValueError(
                    "Unexpected database error. Missing option data for parameter."
                )

            parameter_options = options[parameter_id]

            if parameter_type == ParameterTypes.design.value:
                if ParameterOptions.minimum.value not in parameter_options:
                    raise ValueError(
                        "Unexpected database error. Missing minimum value for design parameter."
                    )

                if ParameterOptions.maximum.value not in parameter_options:
                    raise ValueError(
                        "Unexpected database error. Missing maximum value for design parameter."
                    )

                if ParameterOptions.continuity.value not in parameter_options:
                    raise ValueError(
                        "Unexpected database error. Missing continuity value for design parameter."
                    )

                minimum = parameter_options[ParameterOptions.minimum.value][
                    "number_value"
                ]
                maximum = parameter_options[ParameterOptions.maximum.value][
                    "number_value"
                ]
                continuity = parameter_options[ParameterOptions.continuity.value][
                    "string_value"
                ]

                item["minimum"] = minimum
                item["maximum"] = maximum

                if continuity == ContinuityOptions.continuous.value:
                    mapped_continuity = "continuous"
                elif continuity == ContinuityOptions.discrete.value:
                    mapped_continuity = "discrete"
                else:
                    raise ValueError("Unexpected continuity type in database.")

                item["continuity"] = mapped_continuity

                design_parameter_definitions.append(item)

            elif parameter_type == ParameterTypes.kpi.value:
                if ParameterOptions.goal.value not in parameter_options:
                    raise ValueError(
                        "Unexpected database error. Missing goal for kpi parameter."
                    )

                goal = parameter_options[ParameterOptions.goal.value]["string_value"]

                if goal == ParameterOptions.minimum.value:
                    mapped_goal = "minimize"
                elif goal == ParameterOptions.maximum.value:
                    mapped_goal = "maximize"
                else:
                    raise ValueError("Unexpected goal type in database.")

                item["goal"] = mapped_goal

                kpi_parameter_definitions.append(item)

        session.close()

        return {
            "design": design_parameter_definitions,
            "kpis": kpi_parameter_definitions,
        }

    def __load_options(self, project_id: str, session: Session) -> dict:
        query = """
        SELECT
            parameter_option.parameter_id AS parameter_id,
            parameter_option_type.name AS option_name,
            parameter_option.number_value AS number_value,
            parameter_option.string_value AS string_value
        FROM parameter_option
        LEFT JOIN parameter_option_type
            ON parameter_option_type.id = parameter_option.parameter_option_type_id
        LEFT JOIN project_parameters
            ON project_parameters.parameter_id = parameter_option.parameter_id
        WHERE project_parameters.project_id = :project_id
        """

        db_response = session.execute(query, {"project_id": project_id})

        data = {}

        for row in db_response:
            parameter_id = row["parameter_id"]
            option_name = row["option_name"]
            number_value = row["number_value"]
            string_value = row["string_value"]

            if parameter_id not in data:
                data[parameter_id] = {}

            data[parameter_id][option_name] = {
                "number_value": number_value,
                "string_value": string_value,
            }

        return data

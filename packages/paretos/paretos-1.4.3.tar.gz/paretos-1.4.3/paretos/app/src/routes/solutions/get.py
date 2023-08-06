from typing import Union

from ...command_handler.command_handler import CommandHandler
from ...command_handler.outcome.not_found_failure import NotFoundFailure
from ...command_handler.outcome.outcome import Outcome
from ...database.solutions_mapper import SolutionsMapper
from ...service.logger import Logger


class Get(CommandHandler):
    _methods = ["POST"]
    _schema = {
        "type": "object",
        "properties": {
            "project": {"type": "string"},
            "only_paretos": {"type": "boolean"},
        },
        "required": ["project"],
    }

    def __init__(self, logger: Logger, solutions_mapper: SolutionsMapper):
        self.__logger = logger
        self.__solutions_mapper = solutions_mapper

    def process(self, request_data: dict) -> Union[dict, Outcome]:

        only_paretos = True

        if "only_paretos" in request_data.keys():
            only_paretos = request_data["only_paretos"]

        self.__logger.info(
            "getting project solutions",
            solutions_input={
                "project": request_data["project"],
                "only_paretos": only_paretos,
            },
        )

        evaluations = self.__solutions_mapper.load_solutions(
            request_data["project"], only_pareto=only_paretos
        )

        return {"evaluations": evaluations}

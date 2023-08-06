from typing import Union

from ...command_handler.command_handler import CommandHandler
from ...command_handler.outcome.not_found_failure import NotFoundFailure
from ...command_handler.outcome.outcome import Outcome
from ...database.meta_mapper import MetaMapper
from ...service.logger import Logger


class Get(CommandHandler):
    _methods = ["POST"]
    _schema = {
        "type": "object",
        "properties": {"project": {"type": "string"}},
        "required": ["project"],
    }

    def __init__(self, logger: Logger, meta_mapper: MetaMapper):
        self.__logger = logger
        self.__meta_mapper = meta_mapper

    def process(self, request_data: dict) -> Union[dict, Outcome]:
        self.__logger.info(
            "getting project meta",
            project_meta_input={"project": request_data["project"]},
        )

        result = self.__meta_mapper.load_meta(request_data["project"])

        if len(result["design"]) == 0:
            return NotFoundFailure()

        return result

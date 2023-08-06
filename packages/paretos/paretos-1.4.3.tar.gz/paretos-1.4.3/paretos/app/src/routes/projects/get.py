from typing import Union

from ...command_handler.command_handler import CommandHandler
from ...command_handler.outcome.outcome import Outcome
from ...database.project_mapper import ProjectMapper
from ...service.logger import Logger


class Get(CommandHandler):
    _methods = ["POST"]

    def __init__(self, logger: Logger, project_mapper: ProjectMapper):
        self.__logger = logger
        self.__project_mapper = project_mapper

    def process(self, request_data: dict) -> Union[dict, Outcome]:
        self.__logger.info("Fetching projects.")

        projects = self.__project_mapper.load_project_data()

        return {"projects": projects}

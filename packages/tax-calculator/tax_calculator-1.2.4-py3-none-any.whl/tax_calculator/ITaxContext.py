import abc
import logging
from typing import Dict

import inspect
import typing
import stringcase
from datetime import datetime, timedelta

import arrow
from arrow import Arrow

from tax_calculator.IMoney import IMoney


class ITaxContext(abc.ABC):
    """
    Input of the tax calculator
    """

    @abc.abstractmethod
    def time_to_consider(self) -> Arrow:
        pass

    @abc.abstractmethod
    def start_date(self) -> Arrow:
        """
        Date when the analysis of your taxes start
        """
        pass

    @abc.abstractmethod
    def end_date(self) -> Arrow:
        """
        Date when the analysis of your taxes ends
        """
        pass

    def months_passed(self) -> int:
        """
        Number of months between start date and end date. We consider the whole months only if we are in the latter part of the month: in other words,
        if you are in the 16 of august, we will consider the end of august as the tax period
        """
        if self.start_date.day >= 16:
            s = self.start_date.month + 1
        else:
            s = self.start_date.month

        if self.end_date.day >= 16:
            e = self.end_date.month
        else:
            e = self.end_date.month - 1

        if e == s:
            return 0
        else:
            return e - s + 1



    def duration_to_consider(self) -> timedelta:
        """
        Difference betwen start date and end date
        """
        return self.end_date() - self.start_date()

    def get_help_of(self, name: str) -> str:
        return getattr(self, f"help_{stringcase.snakecase(name)}")()

    def get_tax_variables(self) -> Dict[str, any]:
        return self.__dict__

    def check(self):
        for key in self.__dict__:
            if self.__dict__[key] is None:
                logging.info(f"value \"{key}\" is set to None. Skipping it")
                continue
            value = self.__dict__[key]
            if key.endswith("percentage"):
                if not isinstance(value, float):
                    raise TypeError(f"required float, got {type(value)}")
                if not (0 <= value <= 1):
                    raise ValueError(f"required percentage, got {value}")
            elif key.endswith("money"):
                if issubclass(type(value), IMoney):
                    continue
                if type(value) in [float, int]:
                    continue
                raise TypeError(f"required number, got {type(value)}")
            else:
                # no additional check is required
                pass


class StandardTaxContext(ITaxContext):

    @property
    def start_date(self) -> Arrow:
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def end_date(self) -> Arrow:
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    @property
    def time_to_consider(self) -> Arrow:
        return self._time_to_consider

    @time_to_consider.setter
    def time_to_consider(self, value):
        self._time_to_consider = value

    def __init__(self, time_to_consider: Arrow, start_date: Arrow, end_date: Arrow):
        self._time_to_consider: Arrow = time_to_consider
        self._start_date: Arrow = start_date
        self._end_date: Arrow = end_date

    def help_start_date(self) -> str:
        return """A date marking the beginning of the period of tax calculation.
        """

    def help_end_date(self) -> str:
        return """A date marking the ending of the period of tax calculation.
        """

    def help_time_to_consider(self) -> str:
        return """
        The timestamp when the tax calculation shoud be focus.
        E.g., we would like to want to compute at the 31st of May 2021, regardless 
        of the fact that now it is that time. 
        """

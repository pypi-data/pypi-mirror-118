from typing import Iterable, List, Tuple, Union

from stimpy.stim import StimulusData


class Scene:
    """Class for grouping multiple stimuli.

    :param color: Color of background as (r, g, b) tuple.
    :param units: Defines the default units of stimuli drawn.
    """

    def __init__(self, color: Tuple[int, int, int], units: str):
        self.__color = color
        self.__units = units
        self.__stimulus_data: List[StimulusData] = []
        self.__begin: List[float] = []
        self.__dur: List[float] = []

    def __iter__(self):
        return zip(self.__stimulus_data, self.__begin, self.__dur)

    @property
    def color(self):
        return self.__color

    @property
    def units(self):
        return self.__units

    def add(
        self,
        stimulus_data: Union[StimulusData, Iterable[StimulusData]],
        begin: float,
        dur: float,
    ):
        if isinstance(stimulus_data, StimulusData):
            stimulus_data_list = [stimulus_data]
        else:
            stimulus_data_list = stimulus_data

        for i in stimulus_data_list:
            self.__stimulus_data.append(i)
            self.__begin.append(begin)
            self.__dur.append(dur)

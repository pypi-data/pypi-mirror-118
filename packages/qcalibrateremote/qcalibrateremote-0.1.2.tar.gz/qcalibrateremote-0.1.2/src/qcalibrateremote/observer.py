from dataclasses import dataclass
from typing import Dict, List

from .fom import Pulse


@dataclass
class IterationResult:
    iteration: int
    parameters: Dict[str, float]
    pulses: Dict[str, Pulse]
    figure_of_merit: float
    data: str


@dataclass
class PulseMeta:
    """Pulse meta parameter"""
    index: int
    """ordinal of a pulse in pulse meta list"""
    name: str
    """name of the pulse"""
    configuration: str
    """JSON serilized pulse optimization meta-parameters like basis, sampling, initial quess and boundaries"""


@dataclass
class ParameterMeta:
    """Parameter optimization meta"""
    index: int
    """ordinal of a parameter in a parametzer list"""
    name: int
    """name of a parameter"""
    configuration: str
    """parameter optimization configuration, like boandaries and initial guess"""


@dataclass
class RunMetaParameters:
    """run attributes"""
    run_id: str
    """database ID"""
    configuration: str
    """JSON serialized optimization parameters"""
    parameter_metas: List[ParameterMeta]
    """List of optimizable parameters"""
    pulse_metas: List[PulseMeta]
    """List of optimizable pulses"""


class OptimizationObserver:
    """Base optimization observer
        don't do anything
    """

    def on_start(
        self,
        run_id,
        configuration: str,
        parameter_metas,
        pulse_metas, **
        kwargs): ...

    def on_iteration(
        self,
        iteration: int,
        parameters: Dict[str, float],
        pulses: Dict[str, Pulse],
        figure_of_merit: float,
        data: str,
        **kwargs): ...

    def on_end(self): ...

    def on_error(self, exception: Exception): ...


class OptimizationResultCollector(OptimizationObserver):
    """Storing optimization observer
    accumulates intermediate iteration results

    Parameters
    ----------
    OptimizationObserver : [type]
        basic type
    """

    def __init__(self) -> None:
        super().__init__()
        self._parameters: RunMetaParameters = None
        self._iterations: List[IterationResult] = []
        self._exception: Exception = None
        self._top: List[IterationResult] = []


    def on_start(self, run_id, configuration: str, parameter_metas, pulse_metas, **kwargs):
        self._parameters = RunMetaParameters(
            run_id=run_id,
            configuration=configuration,
            parameter_metas=parameter_metas,
            pulse_metas=pulse_metas)

    def on_iteration(self,
                     iteration: int,
                     parameters: Dict[str, float],
                     pulses: Dict[str, Pulse],
                     figure_of_merit: float,
                     data: str,
                     **kwargs):
        iteration_result = IterationResult(
            iteration=iteration,
            parameters=parameters,
            pulses=pulses,
            figure_of_merit=figure_of_merit,
            data=data)

        self._iterations.append(iteration_result)

        if len(self._top) == 0:
            self._top.append(iteration_result)            
        else:
            # TODO: implement parametrisable multiple top
            if self._top[0].figure_of_merit > iteration_result.figure_of_merit:
                self._top[0] = iteration_result

    def on_error(self, exception: Exception):
        self._exception = exception

    @property
    def parameters(self):
        """Run parameters"""
        return self._parameters

    @property
    def iterations(self):
        """iteration"""
        return self._iterations

    @property
    def exception(self):
        """exeption in case of error"""
        return self.exception

    @property
    def top(self):
        """best fits, the best first"""
        return self._top

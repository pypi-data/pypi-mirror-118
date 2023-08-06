
# import sys

# if sys.version_info[:2] >= (3, 8):
#     # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
#     from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
# else:
#     from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

# try:
#     # Change here if project is renamed and does not equal the package name
#     dist_name = __name__
#     __version__ = version(dist_name)
# except PackageNotFoundError:  # pragma: no cover
#     __version__ = "unknown"
# finally:
#     del version, PackageNotFoundError


from .client import QOptimizerClient, create_optimizer_client
from .endpoint import Endpoint, EndpointSecureKey
from .fom import (EvaluateFigureOfMerit, EvaluateFigureOfMeritFactory,
                  FigureOfMerit, Pulse)
from .observer import (IterationResult, OptimizationObserver,
                       RunMetaParameters, ParameterMeta, PulseMeta, OptimizationResultCollector)

from .browser import BrowserPresenter

__all__ = [
    create_optimizer_client,
    BrowserPresenter,
    Endpoint,
    EndpointSecureKey,
    EvaluateFigureOfMerit,
    EvaluateFigureOfMeritFactory,
    FigureOfMerit,
    IterationResult,
    OptimizationObserver, 
    RunMetaParameters,
    ParameterMeta,
    Pulse,
    PulseMeta,
    QOptimizerClient,
    OptimizationResultCollector,
]

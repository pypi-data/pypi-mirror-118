================
qcalibrateremote
================


A client library for runnig a custom optimisation with qcalibrate software


Description
===========

Example simple parameter parametrisation

.. code-block:: py
    :name: parameter-optimizaton.py
    
    # import dependencies
    from typing import Dict

    from qcalibrateremote import (
        EvaluateFigureOfMerit,
        FigureOfMerit,
        create_optimizer_client,
    )

    # setup client connection (copy form web UI: https://www.qcalibrate.staging.optimal-control.net:31603)
    experiment_id="0xabcd"
    token=("ey...")

    optimizer_client = create_optimizer_client(
        host="grpc.qcalibrate.staging.optimal-control.net", port=31603, token=token)

    # define infidelity evaluation class
    class DistanceFom(EvaluateFigureOfMerit):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__()

        def infidelity(self, param1, param2) -> float:
            return (param1 - 0.55)**2 + (param2 - 0.33)**2

        def evaluate(self, parameters: Dict[str, float], **kwargs) -> FigureOfMerit:
            """Abstract method for figure of merit evaluation"""
            # print(parameters)
            return FigureOfMerit(self.infidelity(**parameters), '')

    # run optimisation
    optimisation_result = optimizer_client.run(experiment_id=experiment_id, evaluate_fom_class=DistanceFom)

    # best fiting parameters
    optimisation_result.top[0].parameters

Note
====

The API is experimental and subject to change without a prior notice

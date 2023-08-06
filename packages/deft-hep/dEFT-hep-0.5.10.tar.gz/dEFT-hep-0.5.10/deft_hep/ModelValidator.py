import copy
from pathlib import Path
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt

from .ConfigReader import ConfigReader
from .PredictionBuilder import PredictionBuilder
from .MCMCFitter import MCMCFitter


class ModelValidator:
    """
    Allows for a model to be validated against dataset with known operator paramters (like MC signal). The model must be defined using `PredictionBuilder` class.
    """

    def __init__(self, pb: PredictionBuilder):
        self.nOps = pb.nOps
        self.pb = pb

    def validate(self, config_test: ConfigReader):
        """ Generate predictions for the test samples in the test configuration using the model from the PredictionBuilder """

        test_samples = config_test.samples
        test_preds = config_test.predictions
        assert self.nOps == len(
            config_test.params["config"]["model"]["prior_limits"]
        ), f"Operator mismatch ({self.nOps} : {len(config_test.params['config']['model']['prior_limits'])}). Make sure the supplied ConfigReader has the correct number of operators for the model"

        print(
            "##############################################################\n"
            "###############  VALIDATION OF MORPHING MODEL  ###############\n"
            "##############################################################\n"
            "\n"
            f"Validation Run Name: {config_test.run_name}\n"
            f"Number of operators: {self.nOps}\n"
            f"Number of validation cases: {len(test_samples)}"
        )

        for prediction, sample in zip(test_preds, test_samples):
            config = copy.deepcopy(config_test)
            config.data = prediction
            fitter = MCMCFitter(config, self.pb, verbose=False)
            print(f"\nValidation for sample: {sample}")
            print(f"Index\tStatus\tValue\tLower\tUpper")
            agreement = (fitter.coefficients - fitter.lower_err < sample[1:]) & (
                sample[1:] < fitter.coefficients + fitter.higher_err
            )
            for i, (coeff, lower, upper, does_agree) in enumerate(
                zip(fitter.coefficients, fitter.lower_err, fitter.higher_err, agreement)
            ):
                print(
                    "{}\t{}\t{}\t-{}\t+{}".format(
                        i + 1, "GOOD" if does_agree else "BAD", coeff, lower, upper
                    )
                )

    def validation_predictions(
        self, config_test: ConfigReader
    ) -> Tuple[np.ndarray, List[np.ndarray]]:
        test_samples = config_test.samples
        test_preds = config_test.predictions

        # Generate predictions using model
        model_preds = [np.array([])] * len(test_samples)
        for i, sample in enumerate(test_samples):
            model_preds[i] = self.pb.make_prediction(sample[1:])
        assert len(model_preds[0]) == len(test_preds[0])

        return test_samples, model_preds

    def comparison_plot(
        self,
        config: ConfigReader,
        model_predictions: List[np.ndarray],
        filepath: str = None,
        use_pdf: bool = False,
    ):
        """ Produces a comparison plots for each test case at a specified filepath or at `./results/{config.run_name}_validation`. The supplied ConfigReader should be related to the validation configuration."""
        run_name = config.run_name
        results_path = (
            Path("results") / f"{run_name}_validation"
            if not filepath
            else Path(filepath)
        )
        results_path.mkdir(parents=True, exist_ok=True)

        # Plot comparison between the model and the monte carlo generated plots
        for i, (m_pred, t_pred) in enumerate(
            zip(model_predictions, config.predictions)
        ):
            plt.scatter(config.x_vals, m_pred, label="Model")
            plt.scatter(config.x_vals, t_pred, label="MC")
            plt.xlabel(f"{config.observable}")
            plt.legend()
            plt.savefig(
                results_path / f"model_comparison_{i}.{'pdf' if use_pdf else 'png'}"
            )
            plt.close()

"""Module to perform analysis on a batch of participants."""
import itertools
import logging
from pathlib import Path
import mvpa.util
import mvpa.single_subj
import mvpa.model
import mvpa.masking
import mvpa.results

log = logging.getLogger(__name__)


def run_analysis(config, base_dir):
    """Run main analysis loop."""
    participant_dirs = get_participant_dirs(base_dir)
    participants = map(mvpa.single_subj.Participant, participant_dirs,
                       itertools.repeat(config))
    masker = mvpa.masking.MVPAMasker()
    for participant in participants:
        log.info("Analyzing participant: %s", participant.name)

        for model_name, model_cfg in config["models"].items():
            log.info("Running model: %s", model_name)
            model = mvpa.model.construct_model(
                estimator_name=model_cfg["model_class"],
                hyperparameters=model_cfg["hyperparameters"],
                standardize=model_cfg["standardize_features"])

            for roi in config["rois"]:
                log.info("Using ROI: %s", roi)

                for timepoint in config["timepoints"]:
                    log.info("Timepoint: %s", timepoint)
                    score, permutation_scores, p_value = mvpa.model.fit_model(
                        model,
                        masker.apply_mask(participant.propergate_missings(
                            participant.features[timepoint],
                            participant.labels[model_name]),
                            roi),
                        participant.labels[model_name],
                        participant.propergate_missings(
                            participant.blocks,
                            participant.labels[model_name]),
                        model_cfg["scoring"],
                        model_cfg["n_permutations"])
                    mvpa.results.save_results(score, permutation_scores,
                                              p_value, participant.name,
                                              model_name, roi, timepoint)


def get_participant_dirs(base_dir):
    """Return dict with participant data directories."""
    base_dir = Path(base_dir)
    return mvpa.util.convert_path_objects_to_path_strings(
        tuple(base_dir.glob("VP*")))

"""Module to perform analysis on a batch of participants."""
import mvpa.util
import mvpa.single_subj
import mvpa.model
import mvpa.masking
import mvpa.results
import itertools
import logging
from pathlib import Path

log = logging.getLogger(__name__)


def run_analysis(config, base_dir):
    """Run main analysis loop."""
    participant_dirs = get_participant_dirs(base_dir)
    participants = map(mvpa.single_subj.Participant, participant_dirs,
                       itertools.repeat(config))
    masker = mvpa.masking.MVPAMasker()
    for participant in participants:
        log.info(f'Analyzing participant: {participant.name}')

        for model_name, model_cfg in config["models"].items():
            log.info(f'Running model: {model_name}')
            model = mvpa.model.construct_model(
                estimator_name=model_cfg["model_class"],
                hyperparameters=model_cfg["hyperparameters"],
                standardize=model_cfg["standardize_features"])

            for roi in config["rois"]:
                log.info(f'Using ROI: {roi}')

                for timepoint in config["timepoints"]:
                    log.info(f'Timepoint: {timepoint}')
                    score, permutation_scores, p = mvpa.model.fit_model(
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
                    mvpa.results.save_results(score, permutation_scores, p,
                                              participant.name, model_name,
                                              roi, timepoint)


def get_participant_dirs(base_dir):
    """Return dict with participant names and their data directories."""
    base_dir = Path(base_dir)
    return mvpa.util.convert_path_objects_to_path_strings(
        tuple(base_dir.glob("VP*")))

"""Module to handle results of MVPA."""
from pathlib import Path
import pandas as pd


def save_results(score, permutation_scores, p_value, participant_name,
                 model_name, roi, timepoint):
    """Save results of MVPA as csv."""
    df = construct_df(score, permutation_scores, p_value, participant_name,
                      model_name, roi, timepoint)
    target_path = construct_target_path(participant_name, model_name, roi)
    Path(target_path).mkdir(parents=True, exist_ok=True)
    df.to_csv(target_path / f"result_timepoint_{timepoint}.csv", index=False)


def construct_df(score, permutation_scores, p_value, participant_name,
                 model_name, roi, timepoint):
    """Construct result data frame for given results."""
    df = pd.DataFrame({"subj": participant_name,
                       "model": model_name,
                       "roi": roi,
                       "timepoint": timepoint,
                       "score": score,
                       "permutation_score": permutation_scores,
                       "p": p_value})
    return df


def construct_target_path(participant_name, model_name, roi):
    """Construct path to save results to."""
    project_root = Path(__file__).parents[1]
    return project_root / "results" / participant_name / f"model_{model_name}"\
        / f"roi_{roi}"

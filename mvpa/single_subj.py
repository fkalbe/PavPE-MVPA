"""Dealing with single participants."""
from pathlib import Path
import pandas as pd
import mvpa.util


class Participant:
    """Class that handles storing and preparing a single participants' data."""

    def __init__(self, subj_path, config):
        self.path = Path(subj_path)
        self.name = self.extract_name_from_path(self.path)
        self.config = config
        self.labels, self.blocks = self.read_labels_and_blocks()
        self.features = self.read_features()

    def read_labels_and_blocks(self):
        """Read the labels for each specified model."""
        result_dir = self.path / "behavioral"
        result_file = tuple(result_dir.glob("RECOG_JOINED_*_day_1*.csv"))
        self.validate_number_of_files(result_file, 1)

        results = pd.read_csv(result_file[0], sep=",")
        labels = {}

        for model in self.config["models"]:
            labels[model] = results[self.config["models"][model]["label_name"]]

        blocks = results["block"]
        return labels, blocks

    def read_features(self):
        """Read the features for each timepoint as lists of 3D t-maps."""
        t_map_dir = self.path / "mvpa"
        features = {}
        for timepoint in self.config["timepoints"]:
            t_map_timepoint_dir = t_map_dir / ('sec_' + timepoint)
            features[timepoint] = pd.Series(
                mvpa.util.convert_path_objects_to_path_strings(
                    tuple(t_map_timepoint_dir.glob("spmT*.nii"))))

        return features

    @staticmethod
    def validate_number_of_files(t_files, expected_len):
        """Ensure that tuple from blob has expected number of files."""
        if len(t_files) != expected_len:
            raise RuntimeError(
                f"Expected {expected_len} file(s), but found {len(t_files)}.")

    @staticmethod
    def propergate_missings(target, reference):
        """Remove elements from target vector where reference has NA values."""
        return target[reference.notna()]

    @staticmethod
    def extract_name_from_path(path):
        """Extract participant name from associated path."""
        return str(path).rsplit("\\", maxsplit=1)[-1]

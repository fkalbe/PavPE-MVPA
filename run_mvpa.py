"""Module to run MVPA analysis from command line."""
import logging
import sys
import argparse
from pathlib import Path
from mvpa.analyze import run_analysis
from mvpa.config import get_config


# setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y/%m/%d %H:%M:%S',
    handlers=[
        logging.FileHandler("logs/logfile.log"),
        logging.StreamHandler(sys.stdout)
    ])

log = logging.getLogger(__name__)


def main():
    """Parse command line, load confing and run analysis."""
    parser = argparse.ArgumentParser(
        description=("Runs Multivariate Pattern Analysis (MVPA) on "
                     "preprocessed fMRI data."))
    parser.add_argument('--config', '-c',
                        type=argparse.FileType('r', encoding='UTF-8'),
                        default=None,
                        help=("Custom config file. Will use /config.yaml if "
                              "not set."))

    args = parser.parse_args()

    # load config
    config = get_config(args.config)

    log.info('Starting analysis.')
    # run analysis
    run_analysis(config, base_dir=Path(__file__).parent / "data")
    log.info('Finished analysis.')


if __name__ == "__main__":
    main()

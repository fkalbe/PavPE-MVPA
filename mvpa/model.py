"""Model and evaluate."""
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut, permutation_test_score
from sklearn.svm import SVC, SVR, LinearSVC, LinearSVR


def fit_model(model, X, y, runs, scoring, n_permutations=100):
    """Fit model using leave-one-run-out CV and permutation testing."""
    logo = LeaveOneGroupOut()
    splits = logo.split(X, y, runs)

    score, permutation_scores, p_value = permutation_test_score(
        model, X, y, groups=runs, cv=splits, scoring=scoring,
        n_permutations=n_permutations, n_jobs=-1)

    print(f"CV score real data: {score}")
    print(f"Mean CV score scrambled data: {np.mean(permutation_scores)}")
    print(f"P-value = {p_value}")

    return(score, permutation_scores, p_value)


def construct_model(estimator_name, hyperparameters, standardize):
    """Instantiate model from estimator name and set hyperparameters."""
    scaler = StandardScaler()
    estimator = get_estimator(estimator_name)
    set_hyperparameters(estimator, hyperparameters)

    if standardize:
        pipe = [
            ('preproc', scaler),
            ('estimator', estimator)
        ]
    else:
        pipe = [
            ('estimator', estimator)
        ]

    return Pipeline(pipe)


def get_estimator(name):
    """Import and return specified estimator class."""
    if name == "SVC":
        return SVC()
    if name == "SVR":
        return SVR()
    if name == "LinearSVC":
        return LinearSVC()
    if name == "LinearSVR":
        return LinearSVR()
    raise ValueError(f"Option {name} is not implemented.")


def set_hyperparameters(model, hyperparameters):
    """Set set of hyperparamters to the specified model."""
    model.set_params(**hyperparameters)

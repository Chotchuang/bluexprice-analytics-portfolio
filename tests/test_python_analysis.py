from __future__ import annotations

from python_analysis.run_analysis import (
    FEATURE_COLUMNS,
    build_features,
    evaluate_models,
    load_inputs,
    validate_inputs,
)


def test_python_inputs_pass_quality_checks() -> None:
    daily, monthly_portfolio, _ = load_inputs()
    assert sum(validate_inputs(daily, monthly_portfolio).values()) == 0


def test_features_use_prior_observations_and_are_complete() -> None:
    daily, _, _ = load_inputs()
    features = build_features(daily)
    assert not features[FEATURE_COLUMNS].isna().any().any()
    assert features["observation_date"].min() > daily["observation_date"].min()


def test_model_evaluation_uses_chronological_holdout() -> None:
    daily, _, _ = load_inputs()
    model_results, feature_importance = evaluate_models(build_features(daily))
    assert set(model_results["model"]) == {
        "Majority baseline",
        "Logistic regression",
        "Random forest",
    }
    assert (model_results["test_rows"] > 0).all()
    assert model_results["f1_score"].between(0, 1).all()
    assert model_results["balanced_accuracy"].between(0, 1).all()
    assert set(feature_importance["feature"]) == set(FEATURE_COLUMNS)

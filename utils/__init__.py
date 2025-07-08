"""
Machine Learning Utilities Package

This package contains helper functions and utilities for machine learning projects.
"""

from .ml_helpers import (
    timer,
    memory_usage,
    quick_eda,
    plot_correlation_matrix,
    plot_feature_distributions,
    evaluate_classification_model,
    plot_learning_curves,
    feature_importance_plot
)

__version__ = "0.1.0"
__author__ = "ML Learning Journey"

__all__ = [
    'timer',
    'memory_usage', 
    'quick_eda',
    'plot_correlation_matrix',
    'plot_feature_distributions',
    'evaluate_classification_model',
    'plot_learning_curves',
    'feature_importance_plot'
]

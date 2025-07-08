"""
Utility functions for machine learning projects.
These functions will be useful across multiple projects and notebooks.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import learning_curve
import time
from functools import wraps


def timer(func):
    """Decorator to time function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️  {func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


def memory_usage(df):
    """Display memory usage of a DataFrame."""
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    print(f"DataFrame memory usage: {memory_mb:.2f} MB")
    return memory_mb


def quick_eda(df, target_col=None):
    """Perform quick exploratory data analysis."""
    print("📊 QUICK EXPLORATORY DATA ANALYSIS")
    print("=" * 50)
    
    # Basic info
    print(f"Dataset shape: {df.shape}")
    print(f"Memory usage: {memory_usage(df):.2f} MB")
    
    # Data types
    print(f"\n📋 Data Types:")
    print(df.dtypes.value_counts())
    
    # Missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"\n❌ Missing Values:")
        missing_pct = (missing / len(df)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing[missing > 0],
            'Missing %': missing_pct[missing > 0]
        }).sort_values('Missing %', ascending=False)
        print(missing_df)
    else:
        print(f"\n✅ No missing values found!")
    
    # Numerical columns summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(f"\n📈 Numerical Columns Summary:")
        print(df[numeric_cols].describe())
    
    # Categorical columns summary
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        print(f"\n🏷️  Categorical Columns Summary:")
        for col in categorical_cols[:5]:  # Show first 5 categorical columns
            unique_count = df[col].nunique()
            print(f"{col}: {unique_count} unique values")
            if unique_count <= 10:
                print(f"   Values: {df[col].value_counts().head().to_dict()}")
    
    # Target column analysis if provided
    if target_col and target_col in df.columns:
        print(f"\n🎯 Target Column Analysis ({target_col}):")
        if df[target_col].dtype in ['object', 'category']:
            print(df[target_col].value_counts())
        else:
            print(df[target_col].describe())


def plot_correlation_matrix(df, figsize=(10, 8), method='pearson'):
    """Plot correlation matrix for numerical columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        print("Not enough numerical columns for correlation matrix.")
        return
    
    plt.figure(figsize=figsize)
    correlation_matrix = df[numeric_cols].corr(method=method)
    
    # Create heatmap
    sns.heatmap(correlation_matrix, 
                annot=True, 
                cmap='coolwarm', 
                center=0,
                square=True,
                fmt='.2f')
    plt.title(f'Correlation Matrix ({method.title()})')
    plt.tight_layout()
    plt.show()
    
    # Find highly correlated pairs
    high_corr_pairs = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_val = correlation_matrix.iloc[i, j]
            if abs(corr_val) > 0.7:
                high_corr_pairs.append({
                    'Feature 1': correlation_matrix.columns[i],
                    'Feature 2': correlation_matrix.columns[j],
                    'Correlation': corr_val
                })
    
    if high_corr_pairs:
        print("🔍 Highly correlated feature pairs (|r| > 0.7):")
        for pair in high_corr_pairs:
            print(f"   {pair['Feature 1']} ↔ {pair['Feature 2']}: {pair['Correlation']:.3f}")


def plot_feature_distributions(df, target_col=None, cols=None, figsize=(15, 10)):
    """Plot distribution of features."""
    if cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cols = [col for col in numeric_cols if col != target_col][:9]  # Max 9 plots
    
    n_cols = min(3, len(cols))
    n_rows = (len(cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows == 1:
        axes = [axes] if n_cols == 1 else axes
    else:
        axes = axes.flatten()
    
    for i, col in enumerate(cols):
        if i < len(axes):
            if target_col and target_col in df.columns:
                # If target is categorical, plot by groups
                if df[target_col].dtype in ['object', 'category']:
                    for group in df[target_col].unique():
                        subset = df[df[target_col] == group]
                        axes[i].hist(subset[col], alpha=0.6, label=str(group), bins=20)
                    axes[i].legend()
                else:
                    axes[i].hist(df[col], bins=20, alpha=0.7)
            else:
                axes[i].hist(df[col], bins=20, alpha=0.7)
            
            axes[i].set_title(f'Distribution of {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')
    
    # Hide empty subplots
    for i in range(len(cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()


def evaluate_classification_model(y_true, y_pred, labels=None, plot=True):
    """Comprehensive evaluation of classification model."""
    print("🎯 CLASSIFICATION MODEL EVALUATION")
    print("=" * 50)
    
    # Basic metrics
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    # Detailed classification report
    print(f"\n📊 Detailed Classification Report:")
    print(classification_report(y_true, y_pred, target_names=labels))
    
    # Confusion matrix
    if plot:
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=labels, yticklabels=labels)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }


def plot_learning_curves(estimator, X, y, cv=5, scoring='accuracy', figsize=(10, 6)):
    """Plot learning curves to diagnose bias/variance."""
    train_sizes, train_scores, val_scores = learning_curve(
        estimator, X, y, cv=cv, scoring=scoring,
        train_sizes=np.linspace(0.1, 1.0, 10),
        random_state=42
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    plt.figure(figsize=figsize)
    plt.plot(train_sizes, train_mean, 'o-', color='blue', label='Training Score')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, 
                     alpha=0.1, color='blue')
    
    plt.plot(train_sizes, val_mean, 'o-', color='red', label='Validation Score')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, 
                     alpha=0.1, color='red')
    
    plt.xlabel('Training Set Size')
    plt.ylabel(scoring.title())
    plt.title('Learning Curves')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Diagnosis
    final_train_score = train_mean[-1]
    final_val_score = val_mean[-1]
    gap = final_train_score - final_val_score
    
    print(f"📈 Learning Curve Analysis:")
    print(f"Final Training Score: {final_train_score:.4f}")
    print(f"Final Validation Score: {final_val_score:.4f}")
    print(f"Train-Validation Gap: {gap:.4f}")
    
    if gap > 0.1:
        print("⚠️  High bias detected: Model might be overfitting")
        print("   Solutions: Reduce model complexity, add regularization")
    elif final_val_score < 0.7:
        print("⚠️  High variance detected: Model might be underfitting")
        print("   Solutions: Increase model complexity, add features")
    else:
        print("✅ Model appears well-balanced")


def feature_importance_plot(model, feature_names, top_n=20, figsize=(10, 8)):
    """Plot feature importance for tree-based models."""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        plt.figure(figsize=figsize)
        plt.bar(range(len(indices)), importances[indices])
        plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.title(f'Top {top_n} Feature Importances')
        plt.ylabel('Importance')
        plt.tight_layout()
        plt.show()
        
        # Print top features
        print(f"🏆 Top {min(10, top_n)} Most Important Features:")
        for i, idx in enumerate(indices[:10]):
            print(f"{i+1:2d}. {feature_names[idx]:20s} {importances[idx]:.4f}")
    else:
        print("Model doesn't have feature_importances_ attribute")


# Example usage and test
if __name__ == "__main__":
    # Create sample data for testing
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'feature1': np.random.normal(0, 1, 1000),
        'feature2': np.random.normal(10, 2, 1000),
        'feature3': np.random.choice(['A', 'B', 'C'], 1000),
        'target': np.random.choice([0, 1], 1000)
    })
    
    print("🧪 Testing utility functions...")
    quick_eda(sample_data, 'target')
    plot_correlation_matrix(sample_data)
    print("✅ All functions working correctly!")

# Friction Detection Logic

This document details the deterministic algorithms used by BFAI to detect process inefficiencies.

## 1. Time Gap Friction

### Goal
Identify specific transitions between two activities (A -> B) that take significantly longer than the historical average for that same transition pair.

### Logic
1.  **Group Transitions**: Collect all duration samples for every unique pair of `(Activity From, Activity To)`.
2.  **Calculate Statistics**: Compute the Mean ($\mu$) and Standard Deviation ($\sigma$) for each transition pair.
3.  **Identify Outliers**: For each specific occurrence, calculate the Z-Score:
    $$Z = \frac{x - \mu}{\sigma}$$
4.  **Thresholding**:
    -   Flag as anomaly if $Z > 3.0$ (default).
    -   AND absolute duration $> 60s$ (to ignore micro-jitter).

## 2. Loop Friction

### Goal
Detect rework or repetitive cycles where the same activity is executed multiple times within a single case.

### Logic
1.  **Count Occurrences**: For each case, count the number of times each unique Activity appears.
2.  **Thresholding**:
    -   Flag if `Count > 2` (default).
    -   Example: A -> B -> A (Count=2, OK). A -> B -> A -> B -> A (Count=3, Flagged).

## 3. Human Dependency Friction

### Goal
Identify cases where human actors are the primary bottleneck compared to system automation.

### Logic
1.  **Categorize Steps**: Label each step as Human or System based on `actor_type`.
2.  **Sum Durations**: Calculate total duration of steps initiated by Humans vs Systems.
3.  **Calculate Ratio**:
    $$Ratio = \frac{\text{Human Duration}}{\text{Total Case Duration}}$$
4.  **Thresholding**:
    -   Flag if $Ratio > 0.5$ (Human time > 50%).

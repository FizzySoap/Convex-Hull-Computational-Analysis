# **Convex-Hull-Computational-Analysis**
A Comparative Study of Geometric Algorithms and Time Complexities
Project Overview

<p align="center">
  <img src="https://github.com/user-attachments/assets/798ebcaf-e771-441c-ab5d-4f4dd453ba96" alt="Graham Scan Visualization">
</p>
                                                *Step-by-step construction of the convex hull using Graham Scan. Points that break convexity are removed during the process.*

This repository contains a comprehensive computational analysis of the Convex Hull problem—finding the smallest convex polygon that encloses a given set of points. The project implements and evaluates three distinct algorithmic approaches, comparing their mathematical foundations and execution performance.
Data Input & Setup

To ensure the scripts run correctly across different environments, the project uses a standardized file structure and a flexible Regex-based parsing system.
File Location

The scripts are configured to look for input data in the parent directory of the source code.

    Required Path: ../data_points.txt (This file must sit in the root folder, outside of src/).

## **Data Format & Parsing**

The scripts are designed to parse coordinate data formatted as a series of parenthesized tuples separated by commas and spaces:
Plaintext

(120.6, 873.2), (487.5, 965.4), (936.3, 286.7),
(824.1, 755.5), (642.9, 213.8), (951.7, 848.9)

Regex Logic: The system uses import re to scan the file for the (x, y) pattern. It extracts the numerical values regardless of line breaks or extra spaces, converting them into float tuples for processing. This makes it easy to copy-paste raw coordinate blocks directly from research notes or
datasets.

## **Algorithms Implemented**
1. Graham Scan

    Complexity: Guaranteed O(nlogn).

    Mechanism: Utilizes a stack-based approach and polar angle sorting relative to an anchor point.

    Analysis: Identified as the most reliable performer for large-scale datasets due to its iterative nature and optimal worst-case complexity.

2. QuickHull

    Complexity: Average O(nlogn) | Worst-case O(n2).

    Mechanism: A divide-and-conquer strategy that recursively partitions points based on their distance from a baseline.

    Analysis: While highly efficient on average, it is susceptible to performance degradation on specific point distributions.

3. Brute Force

    Complexity: O(n3).

    Mechanism: Checks every unique triplet of points to verify edge validity.

    Analysis: Serves as a baseline for performance benchmarking to demonstrate the necessity of optimized geometric algorithms.

## **Empirical Results (Google Colab)**

Performance was verified in a standardized Google Colab environment to ensure reproducibility.
Algorithm	Complexity	Execution Time
Graham Scan	O(nlogn)	0.0010 seconds
QuickHull	O(nlogn)	0.0035 seconds
Brute Force	O(n3)	0.01458 seconds

## **Visualization & Execution**

Each script generates a real-time animation of the hull-building process using matplotlib and networkx.

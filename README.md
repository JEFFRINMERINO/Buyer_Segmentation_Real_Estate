# Machine Learning Based Buyer Segmentation and Investment Profiling for Real Estate Market Intelligence

An end-to-end machine learning project that segments real estate buyers using clustering algorithms and provides investment intelligence through an interactive Streamlit dashboard.

## Project overview

This project was developed as part of the **Unified Mentor internship** for **Parcl Co. Limited**.

The objective is to identify hidden buyer segments based on demographic characteristics, investment behavior, financing patterns, and property portfolio information.

The system enables:

* Buyer segmentation
* Investment profiling
* Geographic investment analysis
* Financing behavior analysis
* Executive decision support
* New buyer segment prediction

## Business problem

Traditional real estate marketing treats buyers as a single group despite significant differences in:

* investment motivation
* financing dependency
* geographic preferences
* property portfolio size
* customer satisfaction

This project applies unsupervised machine learning to discover meaningful buyer segments that support targeted marketing and investment strategies.

## Machine learning workflow

Raw data

↓

Data cleaning and preprocessing

↓

Feature engineering

↓

K-Means clustering

↓

Hierarchical clustering

↓

PCA visualization

↓

Buyer segment profiling

↓

Business intelligence analysis

↓

Streamlit dashboard

↓

New buyer segment prediction

## Project structure

Buyer_Segmentation_Real_Estate/

├── data/

│ ├── raw/

│ └── processed/

├── notebooks/

├── src/

├── streamlit_app/

├── models/

├── reports/

├── docs/

├── requirements.txt

└── README.md

## Technologies used

### Programming

* Python

### Data analysis

* Pandas
* NumPy

### Machine learning

* Scikit-learn
* SciPy

### Visualization

* Plotly
* Matplotlib

### Dashboard

* Streamlit

### Model persistence

* Joblib

## Data preprocessing

The preprocessing pipeline includes:

* duplicate removal
* missing value treatment
* categorical standardization
* age feature creation
* buyer-level aggregation
* investment feature engineering
* feature scaling

## Feature engineering

Key engineered features:

* total properties owned
* total investment value
* average property value
* average floor area
* investment intensity
* portfolio size score
* investment density
* engagement score

## Clustering methodology

### K-Means clustering

Used for primary buyer segmentation.

### Hierarchical clustering

Used for cluster validation and relationship analysis.

### Cluster evaluation

The model is evaluated using:

* Silhouette Score
* Davies–Bouldin Index
* Calinski–Harabasz Score

## Buyer segments

The clustering model identifies strategic buyer groups such as:

* First-Time Buyers
* Corporate Investors
* Global Investors
* Luxury Investors
* Diversified Investors

## Streamlit dashboard

The dashboard contains five interactive pages.

### Home

* Executive KPIs
* Segment distribution
* Executive summary

### Buyer segmentation

* PCA visualization
* Segment comparison
* Investment distribution

### Investor behavior

* Financing analysis
* Acquisition purpose
* Referral channel effectiveness

### Geographic analysis

* Regional investment patterns
* Country distribution
* Geographic concentration

### Segment insights

* Cluster profiles
* Strategic recommendations
* Downloadable reports

### Predict buyer segment

Allows prediction of the buyer segment for a new customer profile using the trained clustering model.

## Key business insights

The analysis reveals:

* high-value investor segments
* loan-dependent buyer groups
* regional investment hotspots
* premium property demand patterns
* customer satisfaction differences across segments

## Installation

```bash
git clone https://github.com/JEFFRINMERINO/Buyer_Segmentation_Real_Estate.git

cd Buyer_Segmentation_Real_Estate

conda create -n realestate_ai python=3.11

conda activate realestate_ai

pip install -r requirements.txt
```

## Run the dashboard

```bash
cd streamlit_app

streamlit run Home.py
```

## Future enhancements

* real-time buyer scoring
* automated investment recommendations
* geospatial property intelligence
* market trend forecasting
* customer lifetime value prediction

## Author

**Jeffrin Merino J**

B.Tech Artificial Intelligence and Data Science

Unified Mentor Internship Project

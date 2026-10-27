# 🇲🇦 Maroc Immobilier — Real Estate Data Analysis

##Project Overview

**Maroc Immobilier** is a Python-based project designed to collect, clean, and analyze real estate listing data in Morocco.

The goal is to explore the Moroccan real estate market, identify price trends across cities, and prepare structured data for further analysis and machine learning applications.

##  Objectives

- Collect real estate listing data using web scraping.
- Clean and preprocess collected data.
- Explore property prices and market trends.
- Compare real estate prices across Moroccan cities.
- Prepare a dataset for future machine learning applications.

##  Technologies

- **Python** — Core programming language
- **Requests & BeautifulSoup** — Web scraping
- **Pandas** — Data manipulation and cleaning
- **Jupyter Notebook** — Exploratory data analysis
- **Matplotlib / Seaborn** — Data visualization, if used in the notebooks

##  Project Structure

```text
maroc-immobilier/
├── app.py
├── scraper.py
├── clean_data.py
├── notebooks/
├── data/
├── requirements.txt
└── README.md
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/aymane-qa/maroc-immobilier.git
cd maroc-immobilier
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the project

Run the scraper:

```bash
python scraper.py
```

Run the data-cleaning script:

```bash
python clean_data.py
```

Run the application:

```bash
python app.py
```

*Note: Adjust commands and file paths if your actual implementation differs.*

## 
Future Improvements

- Add interactive visualizations of real estate prices.
- Develop a machine learning model for property price prediction.
- Add city-based price comparisons.
- Improve data validation and handling of missing values.
- Explore scalable data-processing tools such as PySpark.

##  Author

**Aymane Qasid**

GitHub: [@aymane-qa](https://github.com/aymane-qa)

---

*An ongoing project exploring data engineering, analytics, and artificial intelligence in the Moroccan real estate market.*

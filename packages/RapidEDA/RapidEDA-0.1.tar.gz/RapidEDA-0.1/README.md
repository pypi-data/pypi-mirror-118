# Rapid_EDA
A Python package for Automated Exploratory Data Analysis for Machine Learning in python.

### Automated EDA for Machine Learning
It gives shape,summary, number of categorical and numerical features, description of the dataset, and also the information about the number of null values.

### Installation
```sh
pip install RapidEDA
```
### Get Started
Load the module
```sh
from RapidEDA.eda import eda, eda_report
```
### Automated Report Generation for Machine Learning
Report contains sample of data, shape, number of numerical and categorical features, data uniqueness information, description of data, and null information.

```sh
df = sns.load_dataset('tips')
report = eda_report(df)
```

## License

MIT

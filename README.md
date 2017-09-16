opal-analytics-statstest
=========================

# Overview

This Opal contains a variety of statistical tests taken from both python and R stats packages.  Below is a list of
currently available packages:

* Wilcoxon signed-rank (paired)
* Wilcoxon rank sums (unpaired)

## Installation

`pip install git+https://github.com/Bedrock-py/opal-analytics-statstests.git`

## Parameters Spec for Wilcoxon

```
self.parameters_spec = [
    { "name" : "x_column", "attrname" : "x_column", "value" : "x.column_name", "type" : "input" },
    { "name" : "y_column", "attrname" : "y_column", "value" : "y.column_name", "type" : "input" },
    { "name" : "paired", "attrname" : "paired" , "value" : "False", "type" : "input"}
]
```

* `x_column` The reference to the column to be used for the x data Format is `x.column_name` or `y.column_name`
* `y_column` The reference to the column to be used for the y data Format is `x.column_name` or `y.column_name`
* `paired` True to use the signed-rank test, False to use the rank-sums test

Note that x_column or y_column can come from either input matrix.  Prefix the column name with `x.` or `y.` to
specify which column it refers to

## Requires either two matrices or one matrix with both samples (The columns are selected from the parameters)

* `x_data.csv` The matrix with x data (Uses the matrix.csv from the input)
* `x_features.txt` A list of column names for the matrix (one name per row)
* `y_data.csv` The matrix with y data (Pass empty string "" or empty object "{}" if not required) (Uses the matrix.csv from the input)
* `y_features.txt` A list of column names for the matrix (one name per row) (Pass empty string "" if not required)

## Outputs the following files

`matrix.csv` The Output of the wilcoxon test

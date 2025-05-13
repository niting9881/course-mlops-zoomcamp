mlops-zoomcamp Module1 

Linear Regression

Q1: What is Linear Regression?

Linear regression is a statistical method used to model the relationship between a dependent variable and one or more independent variables. It works by fitting a linear equation to the observed data. Learn more from this StatQuest explanation.

Q2: When should I use Linear Regression?
Use it when you want to predict a continuous numeric value, and you believe there's a linear relationship between predictors and the target variable.

Q3: What are the key assumptions of Linear Regression?
•	Linearity: The relationship between variables is linear.
•	Independence: Observations are independent of each other.
•	Homoscedasticity: Constant variance of errors.
•	Normality of Residuals: Errors should be normally distributed.
•	No Multicollinearity: Predictors should not be highly correlated.

Further Reading:

•	Scikit-learn Linear Regression Docs
    https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
    
•	Towards Data Science Guide
    https://towardsdatascience.com/tag/linear-regression/
    

    
________________________________________
One-Hot Encoding

Q1: What is One-Hot Encoding?
One-hot encoding is a feature engineering technique used to convert categorical data into a binary numerical format suitable for machine learning models.

Q2: Why is One-Hot Encoding important?
Most ML models can't interpret non-numeric data. One-hot encoding helps by creating a new binary column for each category so models can differentiate between them. Example: "Color" → Red, Blue, Green → three columns with 0s and 1s.

Q3: When should I avoid One-Hot Encoding?
Avoid it when your categorical feature has too many unique values, as it increases dimensionality. In those cases, use target encoding or feature hashing.

Further Reading:

•	Scikit-learn Encoding Docs
    https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
•	Feature Engineering Book
    https://www.manning.com/books/feature-engineering-bookcamp
•	Intro to One-Hot Encoding 
    https://www.geeksforgeeks.org/ml-one-hot-encoding/
________________________________________
RMSE (Root Mean Squared Error)

Q1: What is RMSE?
RMSE stands for Root Mean Squared Error. It is a regression metric that measures the average magnitude of the error between predicted and actual values. It’s always non-negative, and lower values indicate better fit.

Q2: How is RMSE calculated?
RMSE is the square root of the average of squared differences between predicted and actual values: 

Q3: Why use RMSE?
It’s a widely used and easy-to-interpret metric that gives more weight to large errors. It's especially useful when large prediction mistakes are more problematic.

Further Reading:

•	Understanding RMSE (Medium)
    https://koshurai.medium.com/demystifying-rmse-your-guide-to-understanding-root-mean-squared-error-379e41dccfd9
    
•	Statistics by Jim
    https://statisticsbyjim.com/

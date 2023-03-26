# Dempster-Shafer-Species-Classification-ML-Model

What do the libraries do? 
numpy: Can organize data into arrays, sets, etc.
pandas: Lets you run a multitude of calculations on your dataset. It is the best for dataset manipulation.
matplotlib.pyplot and seaborn: Create visualizations for your data; has many customizable features.

Who wrote it? 
Me :)

Why does it exist?
The program can take a dataset and make predictions on what class a certain value (penguin) belongs to.

What is it doing?
The program works best with species based classifications. It uses a Dempster-Shafer model to 
develop weighted hypothesis, and then make predictions based on the highest weighted hypothesis.

What data should I use? Who am I giving credit to?
The contents of the data can be broad, but as aforementioned, use a data set that is compatible
with species and values that are numeric.

You can run the Jupyter book file or the Penguins.py file. 

Here is a little insight into the results:

A brief explanation as to why most of our indeterminate cases are incorrect.

1) Indeterminate Case:
In essence an indeterminate case is inherently incorrect and therefore, it isn’t surprising
that most cases eventually do end up being predicted incorrectly.
Ideally we would have a function that evaluates multiple case scenarios (where we can have set {A, B})
and determine which class, in said set, is a valid prediction. 

2) Our Data:
Our data is limited in that it doesn’t have enough values. While enough is subjective, in cases
where we are classifying a species (like penguins), approximately 344 data values are not enough.
We can see a direct effect of this in calculating FSV. First, it is important to note that all our
indeterminate cases are set{Adelie, Chinstrap}, therefore whatever I am about to say holds true (for our dataset).
Intuitively, and even if we look at the visuals, Adelie and Chinstrap have the least overlap for
culmen_length_mm. But when we run the FSV classifier function, culmen_depth_mm is selected. 
This discrepancy can be explained by the fact that culmen_length_mm’s graph has higher standard deviation
because there is too little data. Assuming that the attributes follow normal distribution,
if we were to add more data values, the SD (standard deviation) of culmen_length_mm would decrease.
And thus, the culmen_length_mm FSV for Adelie and Chinstrap would eventually decrease past the culmen_depth_mm FSV
for Adelie and Chinstrap. If we manually set our attr variable to “culmen_length_mm” we can see the following:

We had  327 correct classifications
We had  15 incorrect classifications
We had  0 indeterminate classifications
We had an 95.6140350877193% accuracy

However manual setting isn’t portable and mathematically incorrect. Therefore one of the
sacrifices that comes with a small dataset is getting a less ideal FSV classified attribute.

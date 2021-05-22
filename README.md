# rakesh_varma_portfolio
Rakesh's ML and data science project portfolio

### Image Descriptions Generation & Evaluation using RNN and LSTM Methods. Dataset: Microsoft COCO
This work is roughly based on the paper "Show, Attend and Tell: Neural Image Caption Generation with Visual Attention" by Xu et al. (ICML2015). Image description generation brings together recent advances in computer vision and NLP. This work uses two CNN models VGG16 and Res-net50 along with the RNN-LSTM. These models are evaluated using matrices such as BLEU (all four), METEOR, ROUGE, SPICE, and CIDEr.
The model architecture overview:
* Model 1: This model consists of a VGG-16 CNN architecture combined with RNN-LSTM. It is trained, tested and validated on complete MS COCO dataset. This model hence does not make any distinction between images that contain people and images that do not.
* Model 2: This version uses a ResNet50 CNN architecture combined with RNN-LSTM. It is trained, tested and validated on the complete MS COCO dataset. This model hence does not make any distinction between images that contain people and images that do not.
* Model 3: It comprises a VGG-16 CNN architecture combined with RNN-LSTM. This model fine-tunes the VGG-16 CNN created in Model 1 by being trained with a subset of the COCO dataset that has images containing only people. This ensures that the image features are general, but the language model is focused on people's descriptions.
* Model 4: It comprises a ResNet50 CNN architecture combined with RNN-LSTM. This model fine-tunes the Model 2 ResNet50 CNN with the subset of only images containing people and its training and testing is restrict-ed to the COCO people subset. This ensures that the image and the language models are both focused on people's characteristics and descriptions.


### Perform sentiment analysis using Multinomial Naive Bayes algorithm on Python-Flask framework. 
Deploy application on AWS infrastructure using components such as AWS Elastic Beanstalk, Amazon RDS, AWS API Gateway, AWS Lambda, AWS S3 Bucket, AWS Cloud Watch.
* This prediction operation is performed by a machine learning model. The machine learning model is created by running multinomial naïve bayes on the data set, which is obtained from the Stanford website.
* The input data is also run through Google Natural Language API to perform the sentiment analysis. Any inconsistencies in the result between google NLP API and our machine learning model is stored in the database.
* We pick up these records from this database periodically, through a batch that runs every twenty-four hours, is then used to train and fine-tune the machine learning model further.


### Multinomial Naive Bayes algorithm and 10-fold cross validation from scratch.
Implemented Multinomial Naive Bayes algorithm from scratch. To make 'fail-safe' probability used Laplace smoothing so that the posterior probabilities don't suddenly drop to zero. Evaluate it with a k-fold cross validation on the datasets from the UCI-Machine Learning Repository i.e Breast Cancer Dataset, Car Evaluation Dataset and Hayes-Roth Dataset. After that compare your accuracy with Naïve Bayes from Weka.
 
 
### Income Classification using Census Data (supervised learning). Dataset: USA Census data
Clean the data set and run the decision tree algorithm (CART model) determine which factors had the largest impact on that response variable. Do the classification using Information Gain and GINI index. Also, use Naïve Bayes for classification. Create confusion matrix, precision, recall, F1 score, and ROC curve.


### Weather data analysis(unsupervised learning) using the k-means clustering. Dataset: Texas weather data.
Pre-process the data. Do clustering using for (Y1) with random k points. Use metrics Euclidean and Pearson correlation coefficient. Compare the clusters using Jaccard coefficient. Repeat the above for Y1 and Y2.Also, analyze changes for (Y1, Y2), (Y2, Y3), and (Y1, Y2, Y3) and Visualize stations belonging to the same cluster.


### Association Rule Mining: association rule mining on a real-world data. Dataset: IMDb database
For data set, for each min_sup value, plot how the candidate itemset and frequent itemset change over iterations. Generate rules for each specified min_conf. Plot the number of rules generated with min_sup on X-axis and min_conf on Y-axis. Filter 5 rules each for lift > 1, lift < 1 and lift = 1.


### Predicting Ships Crew Size using ML model. Dataset: cruise_ship_info.csv dataset
Built a simple model using the cruise_ship_info.csv data set for predicting a ship's crew size. This project is organized as
follows: (a) data preprocessing and variable selection; (b) basic regression model; (c) hyper-parameters tuning; and (d) techniques for dimensionality reduction Principal Component Analysis (PCA), We observe that by increasing the number of principal components from 1 to 4, the train and test scores improve. This is because with less components, there is high bias error in the model, since model is overly simplified. As we increase the number of principal components, the bias error will reduce, but complexity in the model increases.


### Creating Customer Segments. Dataset: UCI Machine Learning Repository wholesale customers dataset
Analyze a dataset containing data on various customers' annual spending amounts (reported in monetary units) of diverse product categories for internal structure. One goal of this project is to best describe the variation in the different types of customers that a wholesale distributor interacts with. Doing so would equip the distributor with insight into how to best structure their delivery service to meet the needs of each customer. For the purposes of this project, the features 'Channel' and 'Region' were excluded in the analysis with focus instead on the six product categories recorded for customers

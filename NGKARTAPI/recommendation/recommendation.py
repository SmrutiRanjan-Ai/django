import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from product.models import Product

product_objects = Product.objects.all()
product_descriptions = pd.DataFrame(product_objects.values_list("ProductName", flat=True), \
                                            columns =['product_description'])
print(product_descriptions)
product_descriptions.shape

# checking Missing values and extracting top 500 descriptions
product_descriptions = product_descriptions.dropna().head(min(500, len(product_objects)))

#Feature extraction from product descriptions

#Converting the text in product description into numerical data for analysis
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(product_descriptions["product_description"])

# Fitting K-Means to the dataset as Visualizing product clusters in subset of data
kmeans = KMeans(n_clusters = 10, init = 'k-means++')
y_kmeans = kmeans.fit_predict(X)
plt.plot(y_kmeans, ".")
plt.show()

def print_cluster(i):
    list1 = []
    for ind in order_centroids[i, :10]:
        list1.append(terms[ind])
    return(list1)


#Output
#Recommendation of product based on the current product selected by user.
#To recommend related product based on, Frequently bought together.
#Top words in each cluster based on product description
#Optimal clusters is
true_k = 10

model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print
# # Optimal clusters is

true_k = 10

model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

#print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print_cluster(i)

#Predicting clusters based on key search words
def show_recommendations(product):
    #print("Cluster ID:")
    Y = vectorizer.transform([product])
    prediction = model.predict(Y)
    #print(prediction)
    P=print_cluster(prediction[0])
    return(P)
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Step 1: Create the dataset
data = {
    'Marks': [85, 40, 55, 90, 70, 30, 75],
    'Hours': [4, 1, 2, 5, 3, 0.5, 1],
    'Result': ['Pass', 'Fail', 'Fail', 'Pass', 'Pass', 'Fail', 'Fail']
}

df = pd.DataFrame(data)

# Step 2: Convert Result column to binary (Pass = 1, Fail = 0)
df['Result'] = df['Result'].map({'Pass': 1, 'Fail': 0})

# Step 3: Define features and target
X = df[['Marks', 'Hours']]
y = df['Result']

# Step 4: Train the Decision Tree
clf = DecisionTreeClassifier(criterion='gini', max_depth=3)
clf.fit(X, y)

# Step 5: Visualize the Tree
plt.figure(figsize=(10, 6))
plot_tree(clf, feature_names=['Marks', 'Hours'], class_names=['Fail', 'Pass'], filled=True)
plt.title("Decision Tree Visualization")
plt.tight_layout()
plt.show()

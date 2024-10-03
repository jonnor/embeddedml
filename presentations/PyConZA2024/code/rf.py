
X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
clf = RandomForestClassifier(n_estimators=10, max_leaf_nodes=100)
clf.fit(X_train, y_train)


import emltrees
model = emltrees.new(10, 1000, 10)
with open('eml_digits.csv', 'r') as f:
    emltrees.load_model(model, f)

features = array.array('h', ...)
out = model.predict(features)


from everywhere_digits import RandomForestClassifier
model = RandomForestClassifier()
out = model.predict(x)


import m2c_digits
scores = m2c_digits.score(x)
out = argmax(scores)


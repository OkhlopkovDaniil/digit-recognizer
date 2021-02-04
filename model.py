import tensorflow as tf

"""
Intializes, trains and tests the model to classify digits
"""

def main():
	save_path = 'models/mnist model'
	epochs = 5

	train_ds = tf.keras.datasets.mnist
	(x_train, y_train), (x_test, y_test) = train_ds.load_data()
	
	x_train = tf.keras.utils.normalize(x_train)
	x_test = tf.keras.utils.normalize(x_test)

	model = tf.keras.models.Sequential()
	model.add(tf.keras.layers.Flatten())
	model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
	model.add(tf.keras.layers.Dense(64, activation=tf.nn.relu))
	model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
	
	model.compile(
		optimizer='adam',
		loss='sparse_categorical_crossentropy',
		metrics=['accuracy']
	)
	model.fit(x_train, y_train, epochs=epochs)

	print("\nTesting")
	test_loss, test_acc = model.evaluate(x_test, y_test)
	
	print('\nSaving model to:', save_path)
	model.save(save_path)


if __name__=='__main__':
	main()

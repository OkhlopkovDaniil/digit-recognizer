import tensorflow as tf

"""
Initializes, trains, tests and saves the model for recognizing digits
"""


def main():
	save_path = 'models/mnist model'

	# hyperparameters
	epochs = 10

	# training and testing data
	train_ds = tf.keras.datasets.mnist
	(x_train, y_train), (x_test, y_test) = train_ds.load_data()
	
	x_train = tf.keras.utils.normalize(x_train)
	x_test = tf.keras.utils.normalize(x_test)

	# initializing the model 
	model = tf.keras.models.Sequential()

	model.add(tf.keras.layers.Flatten())
	model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
	model.add(tf.keras.layers.Dense(64, activation=tf.nn.relu))
	model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
	
	# compiling and training the model
	model.compile(
		optimizer='adam',
		loss='sparse_categorical_crossentropy',
		metrics=['accuracy']
	)
	model.fit(x_train, y_train, epochs=epochs)

	# testing the model
	print("\nTesting")
	test_loss, test_acc = model.evaluate(x_test, y_test)
	
	# saving the model
	print('\nSaving model to:', save_path)
	model.save(save_path)


if __name__=='__main__':
	main()

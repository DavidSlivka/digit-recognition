import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_test = tf.keras.utils.normalize(x_test, axis=1)
for test in range(len(x_test)):
    for row in range(28):
        for x in range(28):
            if x_test[test][row][x] != 0:
                x_test[test][row][x] = 1


model = tf.keras.models.load_model('handwritten_digits_mnist.model')
print(len(x_test))
predictions = model.predict(x_test[:10])

wrong = 0
for x in range(len(predictions)):
    print("I predict this number is a:", y_test[x])
    print("Number Actually Is a:", np.argmax(predictions[x]))
    if np.argmax(predictions[x]) != y_test[x]:
        wrong += 1
        print('This one is wrong!')
        plt.imshow(x_test[x], cmap=plt.cm.binary)
        plt.show()
    else:
        plt.imshow(x_test[x], cmap=plt.cm.binary)
        plt.show()

print(f"The program got {wrong} wrong, out of {len(x_test)}")
print(f"{str(100 - ((wrong/len(x_test))*100))}% correct")
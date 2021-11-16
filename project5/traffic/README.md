# Traffic

### Description
An AI that classifies which traffic sign appears in a photograph.

The AI uses a Convolutional Neural Network based on the TensorFlow Keras Sequential model.

<p align="center">
  <img width="500" src="https://user-images.githubusercontent.com/74436899/141666185-8f9e1f59-8fe5-43a8-82a8-5ca4edce5b1a.jpg">
</p>

### Getting Started
1. Run ```python train_traffic_sign_classifier.py gtsrb```.
2. A unit test can be run via ```python test/test_traffic_sign_classifier.py```

### Technologies Used
* Python with TensorFlow & OpenCV

### Experimentation Process
A GIF demoing a training run can be viewed [here](https://user-images.githubusercontent.com/74436899/141786355-df10ee7c-c161-4e0c-b0c8-36bc7e40bbd4.gif).

#### Step 1 
I started by applying: **one** convolutional layer learning 32 filters using a 3×3 kernel, 
**one** max-pooling layer using a 2×2 pool size,
**one** hidden layer with 128 units and a 0.5 dropout.

The results showed that this configuration was insufficient for this data set.
Thus, one convolutional layer and one pooling layer did not generalize the image well enough,
meaning that the images were still too detailed for the model to make accurate predictions.
Furthermore, only one hidden was certainly insufficient for such a complex data set.

```
Epoch 1/10
500/500 [==============================] - 4s 8ms/step - loss: 4.7130 - accuracy: 0.0514
Epoch 2/10
500/500 [==============================] - 4s 9ms/step - loss: 3.5861 - accuracy: 0.0580
Epoch 3/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5365 - accuracy: 0.0580
Epoch 4/10
500/500 [==============================] - 5s 9ms/step - loss: 3.5134 - accuracy: 0.0581
Epoch 5/10
500/500 [==============================] - 5s 10ms/step - loss: 3.5029 - accuracy: 0.0579
Epoch 6/10
500/500 [==============================] - 5s 11ms/step - loss: 3.4975 - accuracy: 0.0581
Epoch 7/10
500/500 [==============================] - 5s 9ms/step - loss: 3.4953 - accuracy: 0.0580
Epoch 8/10
500/500 [==============================] - 5s 10ms/step - loss: 3.4939 - accuracy: 0.0581
Epoch 9/10
500/500 [==============================] - 5s 11ms/step - loss: 3.4934 - accuracy: 0.0580
Epoch 10/10
500/500 [==============================] - 5s 11ms/step - loss: 3.4931 - accuracy: 0.0580
333/333 - 1s - loss: 3.5051 - accuracy: 0.0540 - 1s/epoch - 4ms/step
```

#### Step 2
I then experimented by adding **two more hidden** layers each with 128 units and the same relu activation function.
The results were much better but there was still room for improvement.
Having more layers allowed the model to train itself better on the variety of signs in the data set.

```
Epoch 1/10
500/500 [==============================] - 4s 8ms/step - loss: 4.1340 - accuracy: 0.2812
Epoch 2/10
500/500 [==============================] - 4s 8ms/step - loss: 1.2916 - accuracy: 0.6304
Epoch 3/10
500/500 [==============================] - 4s 9ms/step - loss: 0.7957 - accuracy: 0.7731
Epoch 4/10
500/500 [==============================] - 5s 9ms/step - loss: 0.6083 - accuracy: 0.8274
Epoch 5/10
500/500 [==============================] - 5s 10ms/step - loss: 0.4563 - accuracy: 0.8742
Epoch 6/10
500/500 [==============================] - 6s 11ms/step - loss: 0.3715 - accuracy: 0.8970
Epoch 7/10
500/500 [==============================] - 6s 12ms/step - loss: 0.3506 - accuracy: 0.9057
Epoch 8/10
500/500 [==============================] - 6s 12ms/step - loss: 0.3389 - accuracy: 0.9150
Epoch 9/10
500/500 [==============================] - 6s 13ms/step - loss: 0.2838 - accuracy: 0.9293
Epoch 10/10
500/500 [==============================] - 7s 14ms/step - loss: 0.2571 - accuracy: 0.9344
333/333 - 1s - loss: 0.4418 - accuracy: 0.9097 - 1s/epoch - 4ms/step
```

#### Step 3
With the idea of preventing overfitting in mind,
I tried adding **two more dropout layers** after each of the hidden layers.
The dropout probability I set for each was 0.5.
However, this led to a large decrease in accuracy.
In this case, by having too many dropouts, the model was not able to train itself properly.

```
Epoch 1/10
500/500 [==============================] - 4s 8ms/step - loss: 5.2679 - accuracy: 0.0506
Epoch 2/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5189 - accuracy: 0.0533
Epoch 3/10
500/500 [==============================] - 4s 9ms/step - loss: 3.5135 - accuracy: 0.0531
Epoch 4/10
500/500 [==============================] - 5s 10ms/step - loss: 3.5095 - accuracy: 0.0558
Epoch 5/10
500/500 [==============================] - 5s 10ms/step - loss: 3.5087 - accuracy: 0.0557
Epoch 6/10
500/500 [==============================] - 6s 11ms/step - loss: 3.5053 - accuracy: 0.0562
Epoch 7/10
500/500 [==============================] - 6s 12ms/step - loss: 3.5055 - accuracy: 0.0545
Epoch 8/10
500/500 [==============================] - 6s 12ms/step - loss: 3.5040 - accuracy: 0.0556
Epoch 9/10
500/500 [==============================] - 6s 12ms/step - loss: 3.5050 - accuracy: 0.0542
Epoch 10/10
500/500 [==============================] - 6s 12ms/step - loss: 3.5036 - accuracy: 0.0559
333/333 - 2s - loss: 3.4982 - accuracy: 0.0548 - 2s/epoch - 6ms/step
```

#### Step 4
Subsequently, I reverted to having only **one dropout layer** with 0.5 probability after the hidden layers.
However, I added a **2nd convolutional layer** after the max-pooling layer,
thus allowing the model to extract additional high-level features.
This led to a large increase in prediction accuracy.

```
Epoch 1/10
500/500 [==============================] - 5s 10ms/step - loss: 2.3481 - accuracy: 0.4420
Epoch 2/10
500/500 [==============================] - 6s 11ms/step - loss: 0.8760 - accuracy: 0.7504
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 0.5108 - accuracy: 0.8534
Epoch 4/10
500/500 [==============================] - 6s 13ms/step - loss: 0.3728 - accuracy: 0.8936
Epoch 5/10
500/500 [==============================] - 7s 14ms/step - loss: 0.2923 - accuracy: 0.9190
Epoch 6/10
500/500 [==============================] - 8s 15ms/step - loss: 0.2098 - accuracy: 0.9411
Epoch 7/10
500/500 [==============================] - 7s 14ms/step - loss: 0.2037 - accuracy: 0.9439
Epoch 8/10
500/500 [==============================] - 8s 15ms/step - loss: 0.1664 - accuracy: 0.9545
Epoch 9/10
500/500 [==============================] - 8s 16ms/step - loss: 0.1772 - accuracy: 0.9519
Epoch 10/10
500/500 [==============================] - 9s 18ms/step - loss: 0.1747 - accuracy: 0.9535
333/333 - 3s - loss: 0.2222 - accuracy: 0.9523 - 3s/epoch - 10ms/step
```

#### Step 5
Finally, I added a **2nd pooling layer** after the 2nd convolutional layer.
Thus, further generalizing and reducing the size of the input to the neural network.
This is beneficial as the neural network becomes less sensitive to variation.
Hence, an even greater prediction accuracy was achieved on the testing data set.

```
Epoch 1/10
500/500 [==============================] - 4s 8ms/step - loss: 3.2104 - accuracy: 0.2569
Epoch 2/10
500/500 [==============================] - 5s 10ms/step - loss: 1.3792 - accuracy: 0.5892
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 0.8040 - accuracy: 0.7574
Epoch 4/10
500/500 [==============================] - 7s 14ms/step - loss: 0.5629 - accuracy: 0.8348
Epoch 5/10
500/500 [==============================] - 8s 16ms/step - loss: 0.3967 - accuracy: 0.8821
Epoch 6/10
500/500 [==============================] - 9s 17ms/step - loss: 0.3168 - accuracy: 0.9073
Epoch 7/10
500/500 [==============================] - 8s 17ms/step - loss: 0.2721 - accuracy: 0.9217
Epoch 8/10
500/500 [==============================] - 9s 17ms/step - loss: 0.2370 - accuracy: 0.9336
Epoch 9/10
500/500 [==============================] - 9s 17ms/step - loss: 0.2311 - accuracy: 0.9382
Epoch 10/10
500/500 [==============================] - 9s 18ms/step - loss: 0.1927 - accuracy: 0.9497
333/333 - 4s - loss: 0.1829 - accuracy: 0.9538 - 4s/epoch - 12ms/step
```

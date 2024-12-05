Traffic Signaling Project
Experimental Process

This project uses a convolutional neural network to classify traffic signs
into 43 groups. My initial approach focused on testing different CNN architectures to
determine which one was the most efficient in terms of accuracy and time.
I started with a simple model consisting of two layers with max pooling
and thickness, but the configuration struggled with the accuracy of the
experimental procedure, probably due to insufficient features.

Next, I increased the layers to 3 and changed the number of filters per layer
(from 32 in the first layer to 128 in the third layer).
This change led to a significant improvement in accuracy as the network started detecting
complex patterns in the image and choosing relu was also better don't know why though but it
had more accuracy than sigmoid and all. I don't know if this can be more optimized but
that was from my side.

Categorical cross-entropy is used as the loss function because it works well for multi-class classification problems.
Adam optimizer is used because I heard about it for being efficient in training DNN.
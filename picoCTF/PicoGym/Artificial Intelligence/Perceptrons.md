## Perceptron Train XOR
A perceptron is a single "neuron" in a neural network. It takes inputs x$_1$, x$_2$, ..., multiplies them by weights w$_1$, w$_2$, ..., and adds a bias b. If this sum is positive it returns True, otherwise it returns False.
```python
if ((x1*w1 + x2*w2 + b) >= 0):
	return 1
else: return 0
```

The plot for `x1*w1 + x2*w2 + b = 0` is a straight line where anything on one side is 1 and 0 on the other.
![[Pasted image 20261028231354.png]]This is called a linear classifier.
Now how do you know what weights are correct?
1) Start with training points `(x, y, label)`
2) Predict with current (random) weights and bias
3) If the classification is wrong nudge the weights as follows:
	1) w1 += learning_rate * error * x
	2) w2 += learning_rate * error * y
	3) b += learning_rate * error
	4) error = label - prediction
4) If the prediction was right do nothing

The learning_rate is a "knob" that controls the nudge.
Now because XOR has 4 possible outcomes: two times 0 and two times 1, it's impossible to draw a straight line that divides them evenly. This means 75% accuracy is the ceiling to this problem.
We can see the points far apart from each other. Looking at app.js, we find our data is loaded in config.json. This confirms this. It's nearly impossible to draw a wrong line. So input any number (or leave default even) and you get the flag.
## Perceptron Train XNOR
This is exactly the same as XOR but reversed.
## Perceptron Train Hole in Middle
Visualization of the hole in the middle:

| 1   | 1   | 1   |
| --- | --- | --- |
| 1   | 0   | 1   |
| 1   | 1   | 1   |
The 0 value in the middle is the hole. Again, there is no straight line that can separate all the 1s from the 0. So if you got the center wrong you got 8/9 which translates to 88.88888...% or 88.9%.
We finally get a little bit of a challenge. Anything under a learning rate of 0.5 isn't enough of a nudge to not go through the middle. So just put it above 0.5.

%%[picoCTF-Writeups/Artificial_Intelligence/perceptron_train_classic_0_writeup.md at main · astravoss-cloud/picoCTF-Writeups](https://github.com/astravoss-cloud/picoCTF-Writeups/blob/main/Artificial_Intelligence/perceptron_train_classic_0_writeup.md)%%
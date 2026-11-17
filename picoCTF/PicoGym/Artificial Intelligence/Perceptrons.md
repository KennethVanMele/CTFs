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
## Perceptron Train Classic 0
Rosenblatt proved that if a dataset is linearly separable, the perceptron is guaranteed to find such a line in a finite number of steps. [[Other CTF|Note]] that he doesn't say how many steps, and how big the weights will be. Just that it will classify each point correctly eventually.
This dataset has 8 points in 2 groups with a big gap between them. So the algorithm finds the line pretty fast.
## Perceptron Train Classic 1
Now the challenge makes use find 5 learning rates. Let's simulate with the data we find in config.json
```python
points=[(-4, -2, 0), (-3, -4, 0), (-2, -3, 0), (-3, -1, 0), (3, 4, 1), (4, 2, 1), (2, 3, 1), (3, 1, 1)]

def predict(w, b, x, y):
    return 1 if (x*w[0]+y*w[1]) + b >= 0 else 0

def simulate(lr, max_steps=16):
    w, b = [1.0, -1.0], 0.0
    step = 0
    while step < max_steps:
        for x, y, label in points:
	        if step >= max_steps:
		        break
            step += 1
            pred = predict(w, b, x, y)
            err = label - pred
            #If the prediction is correct error = 0 so this cancels out
            w[0] += lr * err * x
            w[1] += lr * err * y
            b += lr * err
    #Test weights and bias on points
    correct = sum(predict(w, b, x, y) == l for x, y, l in points)
    return correct / len(points), w, b

good=[]
for curlr in range(2, 2001):#0.02 - 20.0 with step 0.01 but python can't do floats here
    accuracy, weight, bias = simulate(curlr/100.0)
    if accuracy == 1.0:
        good.append((curlr/100.0, weight, bias))

print(f"Found {len(good)} points with 100% accuracy.")
for learning_rate, weight, bias in good[::200]:#only show results in steps of 200
    print(f"Learning rate: {learning_rate}, weight1: {weight[0]:6.2f}, weight2: {weight[1]:6.2f} bias: {bias}")
```

100% accuracy so just give 5 random points for the flag.
## Perceptron Train Classic 2
Let's run the simulation again with the new points.
Only 320 out of 2000 work now. Put in the top 5 and get the flag.
## Perceptron Train 3-Bit Parity
Parity adds another check. It checks how many positive integers are in the set. If the number is even, the parity is 0, when uneven its 1.
Because the parity results in a kind of checkerboard pattern it's impossible to draw a straight line that separates every even and odd corner. 75% is the max accuracy so we have to adjust that.
```python
points=[(-2, -2, -2, 0), (-2, -2, 2, 1), (-2, 2, -2, 1), (-2, 2, 2, 0), (2, -2, -2, 1), (2, -2, 2, 0), (2, 2, -2, 0), (2, 2, 2, 1)]  
  
def predict(w, b, x, y,z):  
    return 1 if (x*w[0]+y*w[1]+z*w[2]) + b >= 0 else 0  
  
def simulate(lr, max_steps=16):  
    w, b = [1.0, 1.0, 1.0], 0.0  
    step = 0  
    while step < max_steps:  
        for x, y, z, label in points:  
            if step >= max_steps:  
                break  
            step += 1  
            pred = predict(w, b, x, y, z)  
            err = label - pred  
            #If the prediction is correct error = 0 so this cancels out  
            w[0] += lr * err * x  
            w[1] += lr * err * y  
            w[2] += lr * err * z  
            b += lr * err  
    #Test weights and bias on points  
    correct = sum(predict(w, b, x, y, z) == l for x, y, z, l in points)  
    return correct / len(points), w, b  
  
good=[]  
for curlr in range(2, 2001):#0.02 - 20.0 with step 0.01 but python can't do floats here  
    accuracy, weight, bias = simulate(curlr/100.0)  
    if accuracy == 0.75:  
        good.append((curlr/100.0, weight, bias))  
  
print(f"Found {len(good)} points with 75% accuracy.")  
for learning_rate, weight, bias in good[::40]:#only show results in steps of 40  
    print(f"Learning rate: {learning_rate}, weight1: {weight[0]:6.2f}, weight2: {weight[1]:6.2f}, weight3: {weight[2]:6.2f} bias: {bias}")
```
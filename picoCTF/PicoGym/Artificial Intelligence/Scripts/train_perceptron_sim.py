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
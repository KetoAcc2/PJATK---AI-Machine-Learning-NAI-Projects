def predict(row, weights):
    activation = weights[0]
    for i in range(len(row) - 1):
        activation += weights[i + 1] * row[i]
    return 1.0 if activation >= 0.0 else 0.0


def train_weights(train, l_rate, n_epoch):
    weights = [0.0 for i in range(len(train[0]))]
    for epoch in range(n_epoch):
        # sum_error = 0.0
        for row in train:
            prediction = predict(row, weights)
            error = row[-1] - prediction
            # sum_error += error ** 2
            # threshold
            weights[0] = weights[0] + l_rate * error
            for i in range(len(row) - 1):
                weights[i + 1] = weights[i + 1] + l_rate * error * row[i]
            # print(weights, row)
        # print('epoch=%d, l_rate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))
    return weights


def perceptron(train, test, l_rate, n_epoch):
    predictions = list()
    weights = train_weights(train, l_rate, n_epoch)
    print(weights[1:])
    for row in test:
        prediction = predict(row, weights)
        predictions.append(prediction)
    return predictions


def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0


def get_training_data(train_file):
    unique_labels = dict()
    counter = 0
    dataset = list()
    for i in train_file:
        line = i.strip().split(',')
        tmp_label = line[-1]
        tmp_raw_set = line[:-1]
        if tmp_label not in unique_labels.keys():
            unique_labels[tmp_label] = float(counter)
            counter += 1
        tmp_dataset = [float(j) for j in tmp_raw_set]
        tmp_dataset.append(unique_labels[tmp_label])
        dataset.append(tmp_dataset)

    return dataset, unique_labels


def get_test_data(test_file, labels):
    dataset = list()
    for i in test_file:
        line = i.strip().split(',')
        tmp_label = line[-1]
        tmp_raw_set = line[:-1]
        tmp_dataset = [float(j) for j in tmp_raw_set]
        tmp_dataset.append(labels[tmp_label])
        dataset.append(tmp_dataset)

    return dataset


def get_class_name(labels, value):
    for k, v in labels.items():
        if value == v:
            return k
    return -1


def get_test_sample(line, labels):
    dataset = list()
    tmp_line = line.strip().split(',')
    label = tmp_line[-1]
    raw_set = tmp_line[:-1]
    tmp_dataset = [float(j) for j in raw_set]
    tmp_dataset.append(labels[label])
    dataset.append(tmp_dataset)
    return dataset


def print_results(test_data, actual, predicted, labels):
    print('accuracy:', accuracy_metric(actual, predicted), '%')

    for i in range(len(predicted)):
        print(test_data[i][:-1], 'actual:', get_class_name(labels, actual[i]),
              'predicted:', get_class_name(labels, predicted[i]))


def main():
    # f = open('data/example1_train.txt')
    f = open('data/iris_training.txt')
    train_data, labels = get_training_data(f)
    print('classification:', labels)
    # for i in train_data:
    #     print(i)

    # f = open('data/example1_test.txt')
    f = open('data/iris_test.txt')
    test_data = get_test_data(f, labels)
    # for i in test_data:
    #     print(i)

    actual = list()
    for i in test_data:
        actual.append(float(i[-1]))

    # l_rate = 0.001
    l_rate = float(input("Enter learning rate here:"))
    n_epoch = 8000

    predicted = perceptron(train_data, test_data, l_rate, n_epoch)

    print_results(test_data, actual, predicted, labels)

    sample = list()
    tmp_line = input('Enter test sample (e to exit): ')
    if tmp_line == 'e':
        exit(0)
    else:
        sample = get_test_sample(tmp_line, labels)

    actual = list()
    for i in sample:
        actual.append(float(i[-1]))

    predicted = perceptron(train_data, sample, l_rate, n_epoch)

    print_results(sample, actual, predicted, labels)


if __name__ == '__main__':
    main()

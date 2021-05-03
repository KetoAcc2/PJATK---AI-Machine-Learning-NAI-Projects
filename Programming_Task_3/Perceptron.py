class Perceptron:

    def __init__(self, language):
        self.language = language
        # self.l_rate = 0.012
        # self.n_epoch = 8000
        self.l_rate = 0.002
        self.n_epoch = 8000

    def predict(self, row, weights):
        activation = weights[0]
        for i in range(len(row) - 1):
            activation += weights[i + 1] * row[i]
        return activation

    def train_weights(self, train_data):
        weights = [0.0 for i in range(len(train_data[0]))]
        for epoch in range(self.n_epoch):
            sum_error = 0.0
            for row in train_data:
                prediction = self.predict(row, weights)
                error = row[-1] - prediction
                # error = 1 - prediction
                # sum_error += error ** 2
                weights[0] = weights[0] + self.l_rate * error
                for i in range(len(row) - 1):
                    weights[i + 1] = weights[i + 1] + self.l_rate * error * row[i]

                # normalize weights
                sum_of_weights = float(0)
                for i in range(1, len(weights), 1):
                    sum_of_weights += weights[i]

                if sum_of_weights == 0:
                    sum_of_weights = 1

                for i in range(1, len(weights), 1):
                    weights[i] /= sum_of_weights

                # print(weights, row)
            # print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))
        return weights


    def perceptron(self, train, test):
        predictions = list()
        weights = self.train_weights(train)
        # print(weights[1:])
        for row in test:
            prediction = self.predict(row, weights)
            # prediction = prediction if prediction >= 0 else 0
            predictions.append(prediction)
        return predictions

    def accuracy_metric(self, actual, predicted):
        correct = 0
        for i in range(len(actual)):
            if actual[i] == predicted[i]:
                correct += 1
        return correct / float(len(actual)) * 100.0

    def get_training_data(self, train_file):
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

    def get_test_data(self, test_file, labels):
        dataset = list()
        for i in test_file:
            line = i.strip().split(',')
            tmp_label = line[-1]
            tmp_raw_set = line[:-1]
            tmp_dataset = [float(j) for j in tmp_raw_set]
            tmp_dataset.append(labels[tmp_label])
            dataset.append(tmp_dataset)

        return dataset

    def get_class_name(self, labels, value):
        for k, v in labels.items():
            if value == v:
                return k
        return -1

    def get_test_sample(self, line, labels):
        dataset = list()
        tmp_line = line.strip().split(',')
        label = tmp_line[-1]
        raw_set = tmp_line[:-1]
        tmp_dataset = [float(j) for j in raw_set]
        tmp_dataset.append(labels[label])
        dataset.append(tmp_dataset)
        return dataset

    def print_results(self, test_data, actual, predicted, labels):
        print('accuracy:', self.accuracy_metric(actual, predicted), '%')

        for i in range(len(predicted)):
            print(test_data[i][:-1], 'actual:', self.get_class_name(labels, actual[i]),
                  'predicted:', self.get_class_name(labels, predicted[i]))

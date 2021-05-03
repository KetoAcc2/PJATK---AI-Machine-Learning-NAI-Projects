import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;


public class Main {

    private static String findMajorityClass(String[] candidateClasses)
    {
        Set<String> set = new HashSet<>(Arrays.asList(candidateClasses));
        String[] uniqueValues = set.toArray(new String[0]);
        int[] uniqueStrings = new int[uniqueValues.length];
        for (int i = 0; i < uniqueValues.length; i++) {
            for (String candidateClass : candidateClasses) {
                if (candidateClass.equals(uniqueValues[i])) {
                    uniqueStrings[i]++;
                }
            }
        }


        int superCandidate = uniqueStrings[0];
        for (int i = 1; i < uniqueStrings.length; i++) {
            if (uniqueStrings[i] > superCandidate) {
                superCandidate = uniqueStrings[i];
            }
        }

        int frequency = 0;
        for (int uniqueString : uniqueStrings) {
            if (uniqueString == superCandidate) {
                frequency++;
            }
        }

        int index = -1;
        if (frequency == 1) {
            for (int counter = 0; counter < uniqueStrings.length; counter++) {
                if (uniqueStrings[counter] == superCandidate) {
                    index = counter;
                    break;
                }
            }

            return uniqueValues[index];
        } else {
            int[] indices = new int[frequency];
            System.out.println("multiple majority classes: " + frequency + " classes");
            int indicesCounter = 0;
            for (int counter = 0; counter < uniqueStrings.length; counter++) {
                if (uniqueStrings[counter] == superCandidate) {
                    indices[indicesCounter] = counter;
                    indicesCounter++;
                }
            }

            for (int counter = 0; counter < indices.length; counter++)
                System.out.println("class index: " + indices[counter]);

            Random generator = new Random();
            int rIndex = generator.nextInt(indices.length);
            System.out.println("random index: " + rIndex);
            int nIndex = indices[rIndex];
            return uniqueValues[nIndex];
        }

    }

    private static List<Data> readInstancesFromFile(String file) {
        List<Data> trainData = new ArrayList<>();
        BufferedReader reader;
        try {
            reader = new BufferedReader(new FileReader(file));
            String line = reader.readLine();
            while (line != null) {

                String[] lineArr = line.split(",");
                double[] attributes = new double[lineArr.length - 1];

                for (int i = 0; i < lineArr.length - 1; i++) {
                    attributes[i] = Double.parseDouble(lineArr[i]);
                }

                String datasetName = lineArr[lineArr.length - 1];

                Data data = new Data(attributes, datasetName);
                trainData.add(data);

                line = reader.readLine();

            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return trainData;
    }

    private static void testWithDataset(List<Data> trainData, List<Data> testData, int k) {
        int correctClassificationsCounter = 0;

        for (int x = 0; x < testData.size(); x++) {

            String exactClass = testData.get(x).datasetName;

            List<Result> resultList = new ArrayList<>();
            double[] query = testData.get(x).dataAttributes;
            for (Data data : trainData) {
                double dist = 0.0;
                for (int j = 0; j < data.dataAttributes.length; j++) {
                    dist += Math.pow(data.dataAttributes[j] - query[j], 2);
                }
                double distance = Math.sqrt(dist);
                resultList.add(new Result(distance, data.datasetName));
            }

            resultList.sort(new DistanceComparator());
            String[] candidateClasses = new String[k];
            for (int i = 0; i < k; i++) {
                candidateClasses[i] = resultList.get(i).datasetName;
            }
            String majorityClass = findMajorityClass(candidateClasses);
            System.out.println("Class of instance " + Arrays.toString(query) + " should be: " + majorityClass);

            if (majorityClass.equals(exactClass))
                correctClassificationsCounter++;
        }

        int accuracy = (correctClassificationsCounter * 100) / testData.size();
        System.out.println("Accuracy: " + accuracy + "%");
    }

    private static void testWithDataString(List<Data> trainData, double[] query, int k) {
        List<Result> resultList = new ArrayList<>();
        for (Data data : trainData) {
            double dist = 0.0;
            for (int j = 0; j < data.dataAttributes.length; j++) {
                dist += Math.pow(data.dataAttributes[j] - query[j], 2);
            }
            double distance = Math.sqrt(dist);
            resultList.add(new Result(distance, data.datasetName));
        }

        resultList.sort(new DistanceComparator());
        String[] candidateClasses = new String[k];
        for (int i = 0; i < k; i++) {
            candidateClasses[i] = resultList.get(i).datasetName;
        }
        String majorityClass = findMajorityClass(candidateClasses);
        System.out.println("Class of instance " + Arrays.toString(query) + " is: " + majorityClass);
    }

    public static void main(String[] args){

        String trainFile = args[0];
        String testFile = args[1];

        List<Data> trainData = readInstancesFromFile(trainFile);
        List<Data> testData = readInstancesFromFile(testFile);
        int k = 3;
        testWithDataset(trainData, testData, k);

        System.out.println("-------------------------------");
        Scanner scanner = new Scanner(System.in);
        System.out.println("Put your vector in format \"0.1, 0.2, 0.3, 0.4\"");
        String line = scanner.nextLine();
        if (!(line.isBlank() || line.isEmpty())) {
            String[] strAttributes = line.trim().split(",");
            if (strAttributes.length != trainData.get(0).dataAttributes.length) {
                throw new IllegalArgumentException("Inappropriate vector format!");
            }

            double[] attributes = new double[strAttributes.length];
            for (int i = 0; i < strAttributes.length; i++) {
                attributes[i] = Double.parseDouble(strAttributes[i]);
            }
            testWithDataString(trainData, attributes, k);
        }

    }

    static class Data {
        double[] dataAttributes;
        String datasetName;

        public Data(double[] dataAttributes, String datasetName){
            this.datasetName = datasetName;
            this.dataAttributes = dataAttributes;
        }

        public String toString() {
            return Arrays.toString(dataAttributes) + "," + datasetName;
        }
    }

    static class Result {
        double distance;
        String datasetName;
        public Result(double distance, String datasetName){
            this.datasetName = datasetName;
            this.distance = distance;
        }

        @Override
        public String toString() {
            return datasetName + " .... " + distance;
        }
    }

    static class DistanceComparator implements Comparator<Result> {
        @Override
        public int compare(Result a, Result b) {
            return Double.compare(a.distance, b.distance);
        }
    }

}
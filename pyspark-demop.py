from pyspark import SparkConf, SparkContext

def main():
    # Create Spark configuration and context
    conf = SparkConf().setAppName("WordCountFromFile").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # Path to your input text file
    input_file = "sample.txt"  # <-- replace with your file path

    # Read text file into an RDD (each line is an element)
    lines = sc.textFile(input_file)

    # Split lines into words and flatten
    words = lines.flatMap(lambda line: line.split())

    # Map each word to (word, 1)
    word_pairs = words.map(lambda word: (word, 1))

    # Reduce by key (sum counts)
    word_counts = word_pairs.reduceByKey(lambda a, b: a + b)

    # Collect results
    results = word_counts.collect()

    # Print word counts
    for word, count in results:
        print(f"{word}: {count}")

    sc.stop()

if __name__ == "__main__":
    main()

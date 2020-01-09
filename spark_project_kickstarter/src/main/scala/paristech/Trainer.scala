package paristech
import org.apache.spark.SparkConf
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.ml.feature.{CountVectorizer, HashingTF, IDF, OneHotEncoderEstimator, RegexTokenizer, StopWordsRemover, StringIndexer, VectorAssembler}
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}
import org.apache.spark.sql.functions._


object Trainer {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12",
      "spark.driver.maxResultSize" -> "2g"
    ))

    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP Spark : Trainer")
      .getOrCreate()

    /*******************************************************************************
      *       TP 3
      *
      *       - lire le fichier sauvegarder précédemment
      *       - construire les Stages du pipeline, puis les assembler
      *       - trouver les meilleurs hyperparamètres pour l'entraînement du pipeline avec une grid-search
      *       - Sauvegarder le pipeline entraîné
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/
    val df: DataFrame = spark
      .read
      .parquet("src/main/resources/data/prepared_trainingset")
    //.parquet("/home/sonia/sbouden/cours-spark-telecom-master/data/prepared_trainingset")

    //println("hello world ! from Trainer")

    // --- Stage 1 : récupérer les mots des textes
    // split sentences into sequences of words (tokens)
    val tokenizer = new RegexTokenizer()
      .setPattern("\\W+")  // alternatively .setPattern("\\W").setGaps(false)
      .setGaps(true)  // regex splits on gaps
      .setInputCol("text")  //Param for input column name
      .setOutputCol("rawTokens")  //words

    val countTokens = udf { (text: Seq[String]) => text.length }
    println("\n\n\n -------------- Count words (length text) : "+  countTokens+ "\n\n\n\n")

    val tokenized: DataFrame = tokenizer.transform(df)
    println("\n\n\n -------------- Tokenization------------------------\n\n\n")

    tokenized.show()

    // --- Stage 2 : retirer les stop words
    val remover = new StopWordsRemover()
      .setInputCol("rawTokens")
      .setOutputCol("filtered")

    val dfRemover: DataFrame = remover.transform(tokenized)
    println("\n\n\n -------------- Remove Stop words --------------\n\n\n\n")
    dfRemover.show()

    // --- Stage 3 : computer la partie TF
    // Select the top vocabSize words ordered by term frequency across the corpus
    val countVectorizer = new CountVectorizer()
      .setInputCol("filtered")
      .setOutputCol("rawFeatures")  // Each vector represents the token counts of the document over the vocabulary.
    //.setVocabSize(3)
    //.setMinDF(3)

    //MinDF affects the fitting process by specifying the minimum number of documents a term must appear in to be included in the vocab

    val cvm = countVectorizer
      .fit(dfRemover)

    val dfCountVect: DataFrame = cvm
      .transform(dfRemover)

    dfCountVect.select("text", "rawFeatures", "filtered").show()

    // --- Stage 4 : computer la partie IDF
    // Term frequency-inverse document frequency (TF-IDF)
    // Term frequency TF(t,d) is the number of times that term t appears in document d,
    // while document frequency DF(t,D) is the number of documents that contains term t

    val idf = new IDF()
      .setInputCol("rawFeatures")
      .setOutputCol("tfidf")

    val idfModel = idf
      .fit(dfCountVect)

    val dfIDF: DataFrame = idfModel
      .transform(dfCountVect)

    val df_IDF: DataFrame = dfIDF
      .drop("rawTokens", "filtered", "rawFeatures")

    df_IDF.show()


    // ************** Conversion des variables catégorielles en variables numériques **************
    // --- Stage 5 : convertir country2 en quantités numériques
    val indexer = new StringIndexer()
      .setInputCol("country2")
      .setOutputCol("country_indexed")
    // FrequencyDesc: most frequent label assigned 0


    val indexerModel = indexer
      .setHandleInvalid("skip") //skips the row containing the unseen label entirely
      .fit(df_IDF)

    val dfIndexer: DataFrame = indexerModel.transform(df_IDF)
    dfIndexer.show()

    // --- Stage 6 : convertir currency2 en quantités numériques
    val indexer2 = new StringIndexer()
      .setInputCol("currency2")
      .setOutputCol("currency_indexed")

    val indexerModel2 = indexer2
      .setHandleInvalid("skip") // we can also choose to keep even rows that never appear and give them an index anyway
      .fit(dfIndexer)

    val dfIndexer2: DataFrame = indexerModel2.transform(dfIndexer)
    dfIndexer2.show()

    // --- Stage 7 et 8 : One-Hot encoder ces deux catégories
    // maps a categorical feature, represented as a label index, to a binary vector with at most a
    // single one-value indicating the presence of a specific feature value

    val onehotencoder = new OneHotEncoderEstimator()
      .setInputCols(Array("country_indexed"))
      .setOutputCols(Array("country_onehot"))

    val onehotencoderModel = onehotencoder
      .fit(dfIndexer2)

    val dfOneHot: DataFrame = onehotencoderModel.transform(dfIndexer2)

    val onehotencoder2 = new OneHotEncoderEstimator()
      .setInputCols(Array("currency_indexed"))
      .setOutputCols(Array("currency_onehot"))

    val onehotencoderModel2 = onehotencoder2.fit(dfOneHot)
    dfOneHot.show()

    val dfOneHot2: DataFrame = onehotencoderModel2.transform(dfOneHot)
    dfOneHot2.show()

    // **************  Mettre les données sous une forme utilisable par Spark.ML **************
    // --- Stage 9 : assembler toutes les features en un unique vecteur

    val assembler = new VectorAssembler()
      .setInputCols(Array("tfidf", "days_campaign", "hours_prepa", "goal", "country_onehot", "currency_onehot"))
      .setOutputCol("features")

    val dfAssembler: DataFrame = assembler.transform(dfOneHot2)

    dfAssembler.select("features").show()

    // --- Stage 10 : créer/instancier le modèle de classification

    val lr = new LogisticRegression()
      .setElasticNetParam(0.0)
      .setFitIntercept(true)
      .setFeaturesCol("features")
      .setLabelCol("final_status")
      .setStandardization(true)
      .setPredictionCol("predictions")
      .setRawPredictionCol("raw_predictions")
      .setThresholds(Array(0.7, 0.3))
      .setTol(1.0e-6)
      .setMaxIter(20)

    // --- Création du Pipeline

    val pipeline = new Pipeline()
      .setStages(Array(tokenizer, remover, countVectorizer, idf,
        indexer, indexer2, onehotencoder, onehotencoder2, assembler, lr))

    // ************** Entraînement, test, et sauvegarde du modèle **************
    // ---  Split des données en training et test sets

    val Array(training, test) = df.randomSplit(Array(0.9, 0.1), seed = 114)

    // --- Entrainement du modèle et sauvegarde du modèle
    val model = pipeline.fit(training)
    model.save("src/main/resources/preprocessed")

   // ************** Test du modèle **********************
    val dfWithSimplePredictions: DataFrame = model.transform(test)
    println("\n \n -------------------Application du modèle aux données test : dfWithSimplePredictions -----------------------------")
    dfWithSimplePredictions.groupBy("final_status", "predictions").count.show()

    val evaluator = new MulticlassClassificationEvaluator()
      .setLabelCol("final_status")
      .setPredictionCol("predictions")

    println("\n \n -------------------------------- Evaluation du modèle sans tuning -------------------------------------------- \n \n ")

    val f1score = evaluator.evaluate(dfWithSimplePredictions)
    println("\n \n \n \n f1_score du modèle sur les données de test sans tuning =  " + f1score + "\n \n \n \n")

    // ********************** Réglage des hyper-paramètres (a.k.a. tuning) du modèle **********************
    // --- Grid Search -----

    val paramGrid = new ParamGridBuilder()   // We use a ParamGridBuilder to construct a grid of parameters to search over
      .addGrid(lr.regParam, Array(10e-8, 10e-6, 10e-4, 10e-2))
      .addGrid(countVectorizer.minDF, Array(55.0, 75.0, 95.0))  // be careful it only works with a float .0
      .build()

    val trainValidationSplit = new TrainValidationSplit()
      .setEstimator(pipeline)
      .setEvaluator(evaluator)
      .setEstimatorParamMaps(paramGrid)
      .setTrainRatio(0.7)  //training set

    println("\n \n ---------------------- Evaluation du modèle avec tuning -------------------- \n \n ")
    // --- Training ---

    val modelParam = trainValidationSplit.fit(training)  //grid search on training set
    modelParam.save("src/main/resources/preprocessed")

    // --- Test du modèle ---------

    val dfWithPredictions: DataFrame = modelParam.transform(test)

    dfWithPredictions.groupBy("final_status", "predictions").count.show()
    val f1score2 = evaluator.evaluate(dfWithPredictions)
    println("\n \n \n \n  f1_score du modèle sur les données de test avec tuning =  " + f1score2 + "\n\n\n\n")

  }
}

package paristech

import org.apache.spark.SparkConf
import org.apache.spark.sql.{Column, ColumnName, DataFrame, SparkSession}
import org.apache.spark.sql.functions.{col, udf,when, length}
import org.apache.spark.sql.functions.from_unixtime
import org.apache.spark.sql.functions._
import org.apache.spark.sql.functions.{concat, lit}

object Preprocessor1 {

  def main(args: Array[String]): Unit = {

    // Des réglages optionnels du job spark. Les réglages par défaut fonctionnent très bien pour ce TP.
    // On vous donne un exemple de setting quand même
    val conf = new SparkConf().setAll {
      Map(
        "spark.scheduler.mode" -> "FIFO",
        "spark.speculation" -> "false",
        "spark.reducer.maxSizeInFlight" -> "48m",
        "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
        "spark.kryoserializer.buffer.max" -> "1g",
        "spark.shuffle.file.buffer" -> "32k",
        "spark.default.parallelism" -> "12",
        "spark.sql.shuffle.partitions" -> "12"
      )
    }

    // Initialisation du SparkSession qui est le point d'entrée vers Spark SQL (donne accès aux dataframes, aux RDD,
    // création de tables temporaires, etc., et donc aux mécanismes de distribution des calculs)
    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP Spark : Preprocessor")
      .getOrCreate()

    import spark.implicits._


    /*******************************************************************************
      *       TP 2
      *
      *       - Charger un fichier csv dans un dataFrame
      *       - Pre-processing: cleaning, filters, feature engineering => filter, select, drop, na.fill, join, udf, distinct, count, describe, collect
      *       - Sauver le dataframe au format parquet
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/

    // --- Chargement des données ---
    val df: DataFrame = spark
      .read
      .option("header", true) // utilise la première ligne du (des) fichier(s) comme header
      .option("inferSchema", "true") // pour inférer le type de chaque colonne (Int, String, etc.)
      .option("quote", "\"")   // pour éviter une mauvaise séparation de certaines colonnes
      .option("escape", "\"")  // pour éviter une mauvaise séparation de certaines colonnes
      .csv("src/main/resources/data/train_clean.csv")
      //.csv("/home/sonia/sbouden/spark_project_kickstarter_2019_2020-master/data/train_clean.csv")

    println(s"Nombre de lignes : ${df.count}")
    println(s"Nombre de colonnes : ${df.columns.length}")
    df.show()
    df.printSchema()


    val dfCasted: DataFrame = df
      .withColumn("goal", $"goal".cast("Int"))
      .withColumn("deadline", $"deadline".cast("Int"))
      .withColumn("state_changed_at", $"state_changed_at".cast("Int"))
      .withColumn("created_at", $"created_at".cast("Int"))
      .withColumn("launched_at", $"launched_at".cast("Int"))
      .withColumn("backers_count", $"backers_count".cast("Int"))
      .withColumn("final_status", $"final_status".cast("Int"))

    dfCasted.printSchema()

    // --- Cleaning ---
    dfCasted
      .select("goal", "backers_count", "final_status")
      .describe()
      .show

    /*
    val dfAddColumn: DataFrame = dfBalanced
      .withColumn("days_campaign", round((col("deadline") - col("launched_at"))/(3600*24), scale = 3))

     //val dfCasted: DataFrame = df
    dfCasted
      .withColumn("launched_at", from_unixtime($"launched_at"))
      .withColumn("created_at", from_unixtime($"created_at"))
      .withColumn("deadline", from_unixtime($"deadline"))
      .withColumn("state_changed_at", from_unixtime($"state_changed_at"))
      .show()

    import scala.math.BigDecimal.RoundingMode
    //.setScale(2, RoundingMode.HALF_UP)

    dfCasted
      .withColumn("days_campaign", round((col("deadline") - col("launched_at"))/(3600*24), scale = 3))
      .withColumn("hours_prepa", expr("launched_at-created_at "))
      .show()

    dfCasted
      .drop("created_at")
      .drop("launched_at")
      .drop("deadline")

    dfCasted
      .withColumn("name", lower($"name"))
      .withColumn("keywords", lower($"keywords"))
      .withColumn("desc", lower($"desc"))
      .select(concat($"name", lit(" "), $"keywords") as "text")
      .show()
      */

    dfCasted.groupBy("disable_communication").count.orderBy($"count".desc).show(10)
    dfCasted.groupBy("country").count.orderBy($"count".desc).show(10)
    dfCasted.groupBy("currency").count.orderBy($"count".desc).show(10)
    dfCasted.select("deadline").dropDuplicates.show()
    dfCasted.groupBy("state_changed_at").count.orderBy($"count".desc).show(10)
    dfCasted.groupBy("backers_count").count.orderBy($"count".desc).show(10)
    dfCasted.select("goal", "final_status").show(10)
    dfCasted.groupBy("country", "currency").count.orderBy($"count".desc).show(10)

    val df2: DataFrame = dfCasted.drop("disable_communication")

    // --- Les fuites du futur ---
    val dfNoFutur: DataFrame = df2.drop("backers_count", "state_changed_at")

    // --- Colonnes currency et country ---

    df.filter($"country" === "False")
      .groupBy("currency")
      .count
      .orderBy($"count".desc)
      .show(5)

    def cleanCountry(country: String, currency: String): String = {
      if (country == "False")
        currency
      else
        country
    }

    def cleanCurrency(currency: String): String = {
      if (currency != null && currency.length != 3)
        null
      else
        currency
    }

    val cleanCountryUdf = udf(cleanCountry _)
    val cleanCurrencyUdf = udf(cleanCurrency _)

    val dfCountry: DataFrame = dfNoFutur
      .withColumn("country2", cleanCountryUdf($"country", $"currency"))
      .withColumn("currency2", cleanCurrencyUdf($"currency"))
      .drop("country", "currency")

    // ou encore, en utilisant sql.functions.when:
    dfNoFutur
      .withColumn("country2", when($"country" === "False", $"currency").otherwise($"country"))
      .withColumn("currency2", when($"country".isNotNull && length($"currency") =!= 3, null).otherwise($"currency"))
      .drop("country", "currency")


    /*dfCountry.filter($"final_status" =!= 0 || $"final_status" =!= 1 )
      .orderBy($"count".desc)
      .show()

    object ColumnExt {
      implicit class ColumnMethods(col: Column) {
        def changeNull: Column = {
          when(col.isNull, -1).otherwise(col)
        }

        dfCountry
          .withColumn("days_campaign", col("days_campaign").changeNull)
          .withColumn("hours_prepa", col("hours_prepa").changeNull)
          .withColumn("goal", col("goal").changeNull)
          .show()

        def changeUnknown: Column = {
          when(col.isNull, "unknown").otherwise(col)
        }

        dfCountry
          .withColumn("country2", col("country2").changeUnknown)
          .withColumn("currency2", col("currency2").changeUnknown)
          .show()
      }
    }
       // import scala.math.BigDecimal.RoundingMode
   //.setScale(2, RoundingMode.HALF_UP)

   dfCasted
     .withColumn("name", lower($"name"))
     .withColumn("keywords", lower($"keywords"))
     .withColumn("desc", lower($"desc"))
     .select(concat($"name", lit(" "), $"keywords") as "text")
     .show()

      }
    }

    val monDataFrameFinal1: DataFrame = dfCountry
    monDataFrameFinal1
      .write
      .parquet("/home/sonia/sbouden/cours-spark-telecom-master")
     */

    // --- nombre d’éléments de chaque classe ---
    val dfBalanced: DataFrame = dfCountry
      .filter($"final_status" =!= 0 || $"final_status" =!= 1 )
      .orderBy($"count".desc)

    dfBalanced.show()

    // --- Ajouter une colonne days_campaign ---
    val dfConvert: DataFrame = dfBalanced
    dfConvert
      .withColumn("launched_at", from_unixtime($"launched_at"))
      .withColumn("created_at", from_unixtime($"created_at"))
      .withColumn("deadline", from_unixtime($"deadline"))
      .withColumn("state_changed_at", from_unixtime($"state_changed_at"))
      .show()

    dfConvert
      .withColumn("hours_prepa", expr("launched_at-created_at "))
      .show()

    val dfAddColumn: DataFrame = dfBalanced
      .withColumn("days_campaign", round((col("deadline") - col("launched_at"))/(3600*24), scale = 3))
    dfAddColumn.show(5)

    // --- Ajouter une colonne: hours_prepa ---
    val dfAddColumn2: DataFrame = dfAddColumn
      .withColumn("hours_prepa", round((col("launched_at") - col("created_at"))/3600, 3))

    dfAddColumn2.show(5)

    // --- Supprimer les colonnes launched_at, created_at et deadline ---
    val dfDropCol: DataFrame = dfAddColumn2
      .drop("launched_at", "created_at", "deadline")

    dfDropCol.show(5)

    // --- Mettre les colonnes names, desc et keywords en minuscule ---
    val dfLower: DataFrame = dfDropCol
      .withColumn("name", lower(col("name")))
      .withColumn("desc", lower(col("desc")))
      .withColumn("keywords", lower(col("keywords")))

    dfLower.show(5)


    // --- Concatenation des colonnes en une colonne text ---
    val dfText: DataFrame = dfLower
      .withColumn("text", concat($"name", lit(" "), $"desc", lit(" "), $"keywords"))

    dfText.show(5)

    // --- Remplacer valeurs nulles et unknown ---
    val dfFinal: DataFrame = dfText
      .withColumn("days_campaign", when($"days_campaign".isNull, -1).otherwise($"days_campaign"))
      .withColumn("hours_prepa", when($"hours_prepa".isNull, -1).otherwise($"hours_prepa"))
      .withColumn("goal", when($"goal".isNull, -1).otherwise($"goal"))
      .withColumn("country2", when($"country2".isNull, "unknown").otherwise($"country2"))
      .withColumn("currency2", when($"currency2".isNull, "unknown").otherwise($"currency2"))

    dfFinal.show(5)


    //--- Sauvegarde df final ---
    val monDataFrameFinal: DataFrame = dfFinal
    monDataFrameFinal.show()

    monDataFrameFinal
      .write.mode("overwrite")
      .parquet("src/main/resources/preprocessed")


  }
}

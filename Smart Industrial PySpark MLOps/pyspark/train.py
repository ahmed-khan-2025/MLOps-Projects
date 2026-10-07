# ============================================================
# SMART INDUSTRIAL PYSPARK MLOPS
# PREDICTIVE MAINTENANCE - MODEL TRAINING
# ============================================================

import os
from pathlib import Path

import mlflow
import matplotlib.pyplot as plt

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator,
    MulticlassClassificationEvaluator,
)
from pyspark.ml.feature import VectorAssembler


# ============================================================
# CONFIGURATION
# ============================================================

FEATURES = [
    "temperature",
    "vibration",
    "pressure",
    "rpm",
    "current",
    "humidity",
    "operating_hours",
]

INPUT = "/app/data/processed"

MODEL_PATH = "/app/models/machine_failure_model"

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://mlflow:5000",
)

EXPERIMENT_NAME = (
    "smart-industrial-pyspark-predictive-maintenance"
)

RANDOM_SEED = 42

NUM_TREES = 100

MAX_DEPTH = 8


# ============================================================
# CREATE DIRECTORIES
# ============================================================

Path("/app/models").mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CREATE SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder
    .appName("SmartIndustrialTraining")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# ============================================================
# MAIN TRAINING PIPELINE
# ============================================================

try:

    print("=" * 70)
    print("SMART INDUSTRIAL PYSPARK MLOPS")
    print("PREDICTIVE MAINTENANCE MODEL TRAINING")
    print("=" * 70)

    print(f"Input data      : {INPUT}")
    print(f"Model path      : {MODEL_PATH}")
    print(f"MLflow URI      : {MLFLOW_TRACKING_URI}")
    print(f"MLflow experiment: {EXPERIMENT_NAME}")

    # ========================================================
    # CHECK INPUT DATA
    # ========================================================

    print("\n" + "=" * 70)
    print("CHECKING INPUT DATA")
    print("=" * 70)

    if not os.path.exists(INPUT):
        raise FileNotFoundError(
            f"Processed dataset not found: {INPUT}"
        )

    # ========================================================
    # LOAD PROCESSED PARQUET DATA
    # ========================================================

    print("\n" + "=" * 70)
    print("LOADING PROCESSED DATA")
    print("=" * 70)

    df = (
        spark.read
        .parquet(INPUT)
        .select(*(FEATURES + ["failure"]))
        .withColumn(
            "failure",
            col("failure").cast("double"),
        )
        .dropna()
    )

    row_count = df.count()

    print(f"Total rows: {row_count}")

    print("\nDataset schema:")

    df.printSchema()

    print("\nSample data:")

    df.show(
        10,
        truncate=False,
    )

    print("\nFailure distribution:")

    (
        df.groupBy("failure")
        .count()
        .orderBy("failure")
        .show()
    )

    # ========================================================
    # TRAIN / TEST SPLIT
    # ========================================================

    print("\n" + "=" * 70)
    print("TRAIN / TEST SPLIT")
    print("=" * 70)

    train_df, test_df = df.randomSplit(
        [0.8, 0.2],
        seed=RANDOM_SEED,
    )

    train_count = train_df.count()

    test_count = test_df.count()

    print(f"Training rows: {train_count}")
    print(f"Testing rows : {test_count}")

    # ========================================================
    # FEATURE ASSEMBLER
    # ========================================================

    print("\n" + "=" * 70)
    print("CREATING FEATURE PIPELINE")
    print("=" * 70)

    assembler = VectorAssembler(
        inputCols=FEATURES,
        outputCol="features",
        handleInvalid="skip",
    )

    # ========================================================
    # RANDOM FOREST CLASSIFIER
    # ========================================================

    classifier = RandomForestClassifier(
        labelCol="failure",
        featuresCol="features",
        numTrees=NUM_TREES,
        maxDepth=MAX_DEPTH,
        seed=RANDOM_SEED,
    )

    pipeline = Pipeline(
        stages=[
            assembler,
            classifier,
        ]
    )

    # ========================================================
    # CONFIGURE MLFLOW
    # ========================================================

    print("\n" + "=" * 70)
    print("CONFIGURING MLFLOW")
    print("=" * 70)

    mlflow.set_tracking_uri(
        MLFLOW_TRACKING_URI
    )

    mlflow.set_experiment(
        EXPERIMENT_NAME
    )

    print(
        f"MLflow experiment: {EXPERIMENT_NAME}"
    )

    # ========================================================
    # START MLFLOW RUN
    # ========================================================

    with mlflow.start_run(
        run_name="random-forest-predictive-maintenance"
    ) as run:

        print("\n" + "=" * 70)
        print("TRAINING RANDOM FOREST MODEL")
        print("=" * 70)

        # ----------------------------------------------------
        # LOG PARAMETERS
        # ----------------------------------------------------

        mlflow.log_params(
            {
                "algorithm": "RandomForestClassifier",
                "num_trees": NUM_TREES,
                "max_depth": MAX_DEPTH,
                "random_seed": RANDOM_SEED,
                "train_test_split": "80/20",
                "feature_count": len(FEATURES),
                "features": ",".join(FEATURES),
                "dataset_rows": row_count,
                "training_rows": train_count,
                "testing_rows": test_count,
            }
        )

        # ----------------------------------------------------
        # TRAIN MODEL
        # ----------------------------------------------------

        model = pipeline.fit(
            train_df
        )

        print(
            "Model training completed."
        )

        # ----------------------------------------------------
        # PREDICTIONS
        # ----------------------------------------------------

        print("\n" + "=" * 70)
        print("GENERATING PREDICTIONS")
        print("=" * 70)

        predictions = model.transform(
            test_df
        )

        predictions.select(
            "failure",
            "prediction",
            "probability",
        ).show(
            20,
            truncate=False,
        )

        # ====================================================
        # EVALUATION
        # ====================================================

        print("\n" + "=" * 70)
        print("MODEL EVALUATION")
        print("=" * 70)

        # ----------------------------------------------------
        # Accuracy
        # ----------------------------------------------------

        accuracy_evaluator = (
            MulticlassClassificationEvaluator(
                labelCol="failure",
                predictionCol="prediction",
                metricName="accuracy",
            )
        )

        accuracy = accuracy_evaluator.evaluate(
            predictions
        )

        # ----------------------------------------------------
        # F1
        # ----------------------------------------------------

        f1_evaluator = (
            MulticlassClassificationEvaluator(
                labelCol="failure",
                predictionCol="prediction",
                metricName="f1",
            )
        )

        f1 = f1_evaluator.evaluate(
            predictions
        )

        # ----------------------------------------------------
        # AUC
        # ----------------------------------------------------

        auc_evaluator = (
            BinaryClassificationEvaluator(
                labelCol="failure",
                rawPredictionCol="rawPrediction",
                metricName="areaUnderROC",
            )
        )

        auc = auc_evaluator.evaluate(
            predictions
        )

        # ----------------------------------------------------
        # Precision
        # ----------------------------------------------------

        precision_evaluator = (
            MulticlassClassificationEvaluator(
                labelCol="failure",
                predictionCol="prediction",
                metricName="weightedPrecision",
            )
        )

        precision = precision_evaluator.evaluate(
            predictions
        )

        # ----------------------------------------------------
        # Recall
        # ----------------------------------------------------

        recall_evaluator = (
            MulticlassClassificationEvaluator(
                labelCol="failure",
                predictionCol="prediction",
                metricName="weightedRecall",
            )
        )

        recall = recall_evaluator.evaluate(
            predictions
        )

        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")
        print(f"AUC      : {auc:.4f}")

        # ====================================================
        # LOG METRICS TO MLFLOW
        # ====================================================

        mlflow.log_metrics(
            {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "auc": auc,
            }
        )

        # ====================================================
        # CONFUSION MATRIX
        # ====================================================

        print("\n" + "=" * 70)
        print("CONFUSION MATRIX")
        print("=" * 70)

        confusion_matrix = (
            predictions
            .groupBy(
                "failure",
                "prediction",
            )
            .count()
            .orderBy(
                "failure",
                "prediction",
            )
        )

        confusion_matrix.show()

        # Collect values for visualization

        matrix_rows = (
            confusion_matrix.collect()
        )

        matrix = [
            [0, 0],
            [0, 0],
        ]

        for row in matrix_rows:

            actual = int(
                row["failure"]
            )

            predicted = int(
                row["prediction"]
            )

            count = int(
                row["count"]
            )

            if actual in (0, 1) and predicted in (0, 1):

                matrix[actual][predicted] = count

        confusion_matrix_path = (
            "/app/models/confusion_matrix.png"
        )

        plt.figure(
            figsize=(6, 5)
        )

        plt.imshow(
            matrix
        )

        plt.title(
            "Machine Failure Prediction"
        )

        plt.xlabel(
            "Predicted"
        )

        plt.ylabel(
            "Actual"
        )

        plt.xticks(
            [0, 1],
            ["No Failure", "Failure"],
        )

        plt.yticks(
            [0, 1],
            ["No Failure", "Failure"],
        )

        for i in range(2):

            for j in range(2):

                plt.text(
                    j,
                    i,
                    str(matrix[i][j]),
                    ha="center",
                    va="center",
                )

        plt.tight_layout()

        plt.savefig(
            confusion_matrix_path,
            dpi=150,
        )

        plt.close()

        mlflow.log_artifact(
            confusion_matrix_path
        )

        print(
            f"Confusion matrix saved: "
            f"{confusion_matrix_path}"
        )

        # ====================================================
        # SAVE SPARK MODEL
        # ====================================================

        print("\n" + "=" * 70)
        print("SAVING MODEL")
        print("=" * 70)

        model.write().overwrite().save(
            MODEL_PATH
        )

        print(
            f"Model saved: {MODEL_PATH}"
        )

        # ====================================================
        # LOG MODEL DIRECTORY AS ARTIFACT
        # ====================================================

        mlflow.log_artifacts(
            MODEL_PATH,
            artifact_path="spark_model",
        )

        # ====================================================
        # MLFLOW TAGS
        # ====================================================

        mlflow.set_tags(
            {
                "project": "smart-industrial-pyspark-mlops",
                "framework": "pyspark",
                "model_type": "random_forest",
                "problem_type": "binary_classification",
                "domain": "industrial_predictive_maintenance",
            }
        )

        # ====================================================
        # RUN INFORMATION
        # ====================================================

        print("\n" + "=" * 70)
        print("MLFLOW RUN COMPLETED")
        print("=" * 70)

        print(
            f"Run ID       : {run.info.run_id}"
        )

        print(
            f"Experiment ID: {run.info.experiment_id}"
        )

        print(
            f"Accuracy     : {accuracy:.4f}"
        )

        print(
            f"Precision    : {precision:.4f}"
        )

        print(
            f"Recall       : {recall:.4f}"
        )

        print(
            f"F1 Score     : {f1:.4f}"
        )

        print(
            f"AUC          : {auc:.4f}"
        )

    # ========================================================
    # COMPLETED
    # ========================================================

    print("\n" + "=" * 70)
    print("TRAINING PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

except Exception as error:

    print("\n" + "=" * 70)
    print("TRAINING PIPELINE FAILED")
    print("=" * 70)

    print(
        f"Error: {error}"
    )

    raise

finally:

    spark.stop()

    print("\nSpark session stopped.")


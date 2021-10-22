package linreg

import breeze.linalg.{csvread, csvwrite}
import com.typesafe.scalalogging.Logger
import java.io.{File, FileInputStream, PrintWriter}
import play.api.libs.json.Json


object Main extends App {
    val logger = Logger("LinearRegression")

    logger.debug("Loading config...")
    val cfgData = Json.parse(new FileInputStream(args(0))).as[InputFile]

    logger.debug("Reading data...")
    val x = csvread(new File(cfgData.inputDataPaths.xTrainPath))
    val y = csvread(new File(cfgData.inputDataPaths.yTrainPath)).toDenseVector
    val xTest = csvread(new File(cfgData.inputDataPaths.xTestPath))

    logger.debug("Splitting data...")
    val trainUtils = TrainUtils()

    val (xTrain, xVal, yTrain, yVal) = trainUtils.trainValSplit(
        x, y, shuffle=cfgData.valParams.shuffle, valSize=cfgData.valParams.valSize
    )

    logger.debug("Fitting model...")
    val linearRegression = LinearRegression()
    linearRegression.fit(
        xTrain, yTrain, learningRate=cfgData.trainParams.learningRate, epochs=cfgData.trainParams.epochs
    )

    logger.debug("Calculating validation score...")
    val yValPred = linearRegression.predict(xVal)
    val valScore = trainUtils.meanSquaredError(yVal, yValPred)

    logger.debug("Writing validation score...")
    val pw = new PrintWriter(new File(cfgData.outputDataPaths.valScorePath))
    pw.write(valScore.toString)
    pw.close()

    logger.debug("Making predictions...")
    val yTestPred = linearRegression.predict(xTest)

    logger.debug("Writing Predictions...")
    csvwrite(new File(cfgData.outputDataPaths.yTestPredPath), yTestPred.toDenseMatrix)
}

package linreg

import breeze.linalg.{csvread, csvwrite}

import java.io.{File, FileInputStream}
import play.api.libs.json.Json


object Main extends App {
    val input = new FileInputStream(args(0))
    val json = Json.parse(input)
    val cfgData = json.as[InputFile]

    val x = csvread(new File(cfgData.inputDataPaths.xTrainPath))
    val y = csvread(new File(cfgData.inputDataPaths.yTrainPath)).toDenseVector
    val xTest = csvread(new File(cfgData.inputDataPaths.xTestPath))

    val trainUtils = TrainUtils()

    val (xTrain, xVal, yTrain, yVal) = trainUtils.trainValSplit(
        x, y, shuffle=cfgData.valParams.shuffle, valSize=cfgData.valParams.valSize
    )

    val trainTuple= trainUtils.trainValSplit(
        x, y, shuffle=cfgData.valParams.shuffle, valSize=cfgData.valParams.valSize
    )

    val linearRegression = LinearRegression()
    linearRegression.fit(
        xTrain, yTrain, learningRate=cfgData.trainParams.learningRate, epochs=cfgData.trainParams.epochs
    )

    val yValPred = linearRegression.predict(xVal)
    val valScore = trainUtils.meanSquaredError(yVal, yValPred)
    println(s"Validation Score: $valScore")

    val yTestPred = linearRegression.predict(xTest).toDenseMatrix
    csvwrite(new File(cfgData.outputDataPaths.yTestPredPath), yTestPred)
}

package linreg

import breeze.linalg.{DenseMatrix, DenseVector, sum}
import breeze.numerics.pow
import scala.util.Random

case class TrainUtils() {
  def meanSquaredError(yTrue: DenseVector[Double], yPred: DenseVector[Double]): Double = {
    require(yTrue.length == yPred.length, "Dimensions disagree")

    sum(pow(yTrue - yPred, 2)) / yTrue.length
  }

  def trainValSplit(x: DenseMatrix[Double], y: DenseVector[Double], shuffle: Boolean, valSize: Double): (
    DenseMatrix[Double], DenseMatrix[Double], DenseVector[Double], DenseVector[Double]
    ) = {
    require(x.rows == y.length, "Dimensions disagree")

    val splitIdx = (valSize * y.length).toInt

    require((0 < splitIdx) & (splitIdx < y.length), "valSize has a wrong value")

    var idxCollection = Array.range(0, y.length)
    if (shuffle) {
      idxCollection = Random.shuffle(idxCollection).toArray
    }

    val idxTrainCollection = idxCollection.slice(0, splitIdx).toIndexedSeq
    val idxValCollection = idxCollection.slice(splitIdx + 1, y.length).toIndexedSeq

    val xTrain = x(idxTrainCollection, ::).toDenseMatrix
    val yTrain = y(idxTrainCollection).toDenseVector
    val xVal = x(idxValCollection, ::).toDenseMatrix
    val yVal = y(idxValCollection).toDenseVector

    (xTrain, xVal, yTrain, yVal)
  }
}

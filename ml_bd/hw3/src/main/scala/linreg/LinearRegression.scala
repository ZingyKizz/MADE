package linreg

import breeze.linalg.{DenseMatrix, DenseVector}
import scala.util.Random

case class LinearRegression() {

  var weights: DenseVector[Double] = _
  var isFitted: Boolean = false

  private def preprocess(x: DenseMatrix[Double]): DenseMatrix[Double] = {
    val ones = DenseMatrix.ones[Double](rows=x.rows, cols=1)
    DenseMatrix.horzcat(ones, x)
  }

  private def computeGrad(x: DenseMatrix[Double], y: DenseVector[Double], idx: Int,
                          weights: DenseVector[Double]): DenseVector[Double] = {
    val xi = x(idx, ::).t
    val yi = y(idx)
    (weights * xi - yi) * xi
  }

  def fit(x: DenseMatrix[Double], y: DenseVector[Double], learningRate: Double, epochs: Int): Unit = {
    require(x.rows == y.length, "Dimensions disagree")

    val xProcessed = this.preprocess(x)

    weights = DenseVector.zeros[Double](xProcessed.cols)
    for (_ <- 1 to epochs) {
      val idxCollection = Random.shuffle(Array.range(0, y.length))
      for (idx <- idxCollection) {
        weights -= learningRate * computeGrad(xProcessed, y, idx, weights)
      }
    }
    isFitted = true
  }

  def predict(x: DenseMatrix[Double]): DenseVector[Double] = {
    require(isFitted, "Model is not fitted yet")

    val xProcessed = this.preprocess(x)
    xProcessed * weights
  }
}

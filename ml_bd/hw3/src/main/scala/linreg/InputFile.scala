package linreg

import play.api.libs.json.{Json, OFormat}

case class InputDataPaths(xTrainPath: String, yTrainPath: String, xTestPath: String)

case class TrainParams(learningRate: Double, epochs: Int)

case class ValParams(shuffle: Boolean, valSize: Double)

case class OutputDataPaths(yTestPredPath: String, valScorePath: String)

case class InputFile(inputDataPaths: InputDataPaths, trainParams: TrainParams,
                     valParams: ValParams, outputDataPaths: OutputDataPaths)

object InputDataPaths {
  implicit val format: OFormat[InputDataPaths] = Json.format[InputDataPaths]
}

object TrainParams {
  implicit val format: OFormat[TrainParams] = Json.format[TrainParams]
}

object ValParams {
  implicit val format: OFormat[ValParams] = Json.format[ValParams]
}

object OutputDataPaths {
  implicit val format: OFormat[OutputDataPaths] = Json.format[OutputDataPaths]
}

object InputFile {
  implicit val format: OFormat[InputFile] = Json.format[InputFile]
}

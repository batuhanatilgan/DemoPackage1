from pydantic import validator, Field
from typing import List, Optional, Union, Literal

try:
    from sdks.novavision.src.base.model import Package, Config, Inputs, Configs, Outputs, Response, Request, Output, Input, Image
except ImportError:
    class Package: pass
    class Config: pass
    class Inputs: pass
    class Configs: pass
    class Outputs: pass
    class Response: pass
    class Request: pass
    class Output: pass
    class Input: pass
    class Image: pass

# INPUT / OUTPUT TANIMLARI

class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config:
        title = "First Input Image"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config:
        title = "Second Input Image"

class OutputImageOne(Output):
    name: Literal["outputImageOne"] = "outputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config:
        title = "Primary Output"

class OutputImageTwo(Output):
    name: Literal["outputImageTwo"] = "outputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config:
        title = "Secondary Output"

#1. EXECUTOR AYARLARI (FILTER)

class BlurKernelSize(Config):
    name: Literal["BlurKernelSize"] = "BlurKernelSize"
    value: int = Field(default=5)
    type: Literal["integer"] = "integer"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Kernel Size"

class BlurIsGaussian(Config):
    name: Literal["BlurIsGaussian"] = "BlurIsGaussian"
    value: bool = Field(default=True)
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config:
        title = "Use Gaussian Blur"

class BlurOptions(Config):
    blurKernelSize: BlurKernelSize
    blurIsGaussian: BlurIsGaussian
    name: Literal["BlurOptions"] = "BlurOptions"
    value: Literal["Blur"] = "Blur"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Blur Mode"

class ThreshValue(Config):
    name: Literal["ThreshValue"] = "ThreshValue"
    value: float = Field(default=127.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Threshold Value"

class ThreshType(Config):
    name: Literal["ThreshType"] = "ThreshType"
    value: str = Field(default="BINARY")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Threshold Type"

class ThresholdOptions(Config):
    threshValue: ThreshValue
    threshType: ThreshType
    name: Literal["ThresholdOptions"] = "ThresholdOptions"
    value: Literal["Threshold"] = "Threshold"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Threshold Mode"

#DEPENDENT DROPDOWN 1
class ConfigFilterMode(Config):
    name: Literal["ConfigFilterMode"] = "ConfigFilterMode"
    value: Union[BlurOptions, ThresholdOptions]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Filter Operation Type"

class FilterExecutorConfig(Config):
    configFilterMode: ConfigFilterMode
    name: Literal["FilterExecutorConfig"] = "FilterExecutorConfig"
    value: Literal["FilterExecutorConfig"] = "FilterExecutorConfig"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Filter Settings"

#2. EXECUTOR AYARLARI (MIXER)

class BlendAlpha(Config):
    name: Literal["BlendAlpha"] = "BlendAlpha"
    value: float = Field(default=0.5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Alpha"

class BlendGamma(Config):
    name: Literal["BlendGamma"] = "BlendGamma"
    value: int = Field(default=0)
    type: Literal["integer"] = "integer"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Gamma"

class BlendOptions(Config):
    blendAlpha: BlendAlpha
    blendGamma: BlendGamma
    name: Literal["BlendOptions"] = "BlendOptions"
    value: Literal["Blend"] = "Blend"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Blend Images"

class ArithOperation(Config):
    name: Literal["ArithOperation"] = "ArithOperation"
    value: str = Field(default="ADD")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    class Config:
        title = "Operation"

class ArithScale(Config):
    name: Literal["ArithScale"] = "ArithScale"
    value: bool = Field(default=False)
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"
    class Config:
        title = "Auto Scale"

class ArithmeticOptions(Config):
    arithOperation: ArithOperation
    arithScale: ArithScale
    name: Literal["ArithmeticOptions"] = "ArithmeticOptions"
    value: Literal["Arithmetic"] = "Arithmetic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Arithmetic Ops"

#DEPENDENT DROPDOWN 2
class ConfigMixerMode(Config):
    name: Literal["ConfigMixerMode"] = "ConfigMixerMode"
    value: Union[BlendOptions, ArithmeticOptions]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Mixing Method"

class MixerExecutorConfig(Config):
    configMixerMode: ConfigMixerMode
    name: Literal["MixerExecutorConfig"] = "MixerExecutorConfig"
    value: Literal["MixerExecutorConfig"] = "MixerExecutorConfig"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    class Config:
        title = "Mixer Settings"

#CONFIG BAĞLANTILARI

# Filter Executor
class FilterConfigs(Configs):
    filterSettings: FilterExecutorConfig

class FilterInputs(Inputs):
    inputImageOne: InputImageOne

class FilterOutputs(Outputs):
    outputImageOne: OutputImageOne

class FilterRequest(Request):
    inputs: Optional[FilterInputs]
    configs: FilterConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class FilterResponse(Response):
    outputs: FilterOutputs

class FilterExecutor(Config):
    name: Literal["Filter"] = "Filter"
    value: Union[FilterRequest, FilterResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Single Image Filter"
        json_schema_extra = {"target": {"value": 0}}

# Mixer Executor
class MixerConfigs(Configs):
    mixerSettings: MixerExecutorConfig

class MixerInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo

class MixerOutputs(Outputs):
    outputImageOne: OutputImageOne
    outputImageTwo: OutputImageTwo

class MixerRequest(Request):
    inputs: Optional[MixerInputs]
    configs: MixerConfigs
    class Config:
        json_schema_extra = {"target": "configs"}

class MixerResponse(Response):
    outputs: MixerOutputs

class MixerExecutor(Config):
    name: Literal["Mixer"] = "Mixer"
    value: Union[MixerRequest, MixerResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Dual Image Mixer"
        json_schema_extra = {"target": {"value": 0}}

#ANA PAKET

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FilterExecutor, MixerExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True
    class Config:
        title = "Select Operation Mode"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    name: Literal["DemoPackage"] = "DemoPackage"
    configs: PackageConfigs
    type: Literal["capsule"] = "capsule"

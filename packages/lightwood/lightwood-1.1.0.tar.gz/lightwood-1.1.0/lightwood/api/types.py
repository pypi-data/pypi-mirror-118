from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from lightwood.helpers.log import log
from dataclasses_json import dataclass_json
from dataclasses_json.core import _asdict, Json
import json


@dataclass
class Feature:
    encoder: str
    data_dtype: str = None
    dependency: List[str] = None

    @staticmethod
    def from_dict(obj: Dict):
        encoder = obj['encoder']
        data_dtype = obj.get('data_dtype', None)
        dependency = obj.get('dependency', None)

        feature = Feature(
            encoder=encoder,
            data_dtype=data_dtype,
            dependency=dependency
        )

        return feature

    @staticmethod
    def from_json(data: str):
        return Feature.from_dict(json.loads(data))

    def to_dict(self, encode_json=False) -> Dict[str, Json]:
        as_dict = _asdict(self, encode_json=encode_json)
        for k in list(as_dict.keys()):
            if as_dict[k] is None:
                del as_dict[k]
        return as_dict

    def to_json(self) -> Dict[str, Json]:
        return json.dumps(self.to_dict(), indent=4)


@dataclass_json
@dataclass
class Output:
    data_dtype: str
    encoder: str = None
    models: List[str] = None
    ensemble: str = None


@dataclass_json
@dataclass
class TypeInformation:
    dtypes: Dict[str, str]
    additional_info: Dict[str, object]
    identifiers: Dict[str, str]

    def __init__(self):
        self.dtypes = dict()
        self.additional_info = dict()
        self.identifiers = dict()


@dataclass_json
@dataclass
class StatisticalAnalysis:
    nr_rows: int
    df_std_dev: Optional[float]
    # Write proper to and from dict parsing for this than switch back to using the types bellow, dataclasses_json sucks!
    train_observed_classes: object  # Union[None, List[str]]
    target_class_distribution: object  # Dict[str, float]
    histograms: object  # Dict[str, Dict[str, List[object]]]
    buckets: object  # Dict[str, Dict[str, List[object]]]
    missing: object
    distinct: object
    bias: object
    avg_words_per_sentence: object
    positive_domain: bool


@dataclass_json
@dataclass
class DataAnalysis:
    statistical_analysis: StatisticalAnalysis
    type_information: TypeInformation


@dataclass
class TimeseriesSettings:
    is_timeseries: bool
    order_by: List[str] = None
    window: int = None
    group_by: List[str] = None
    use_previous_target: bool = False
    nr_predictions: int = None
    historical_columns: List[str] = None
    target_type: str = ''  # @TODO: is the current setter (outside of initialization) a sane option?

    @staticmethod
    def from_dict(obj: Dict):
        if len(obj) > 0:
            for mandatory_setting in ['order_by', 'window']:
                if mandatory_setting not in obj:
                    err = f'Missing mandatory timeseries setting: {mandatory_setting}'
                    log.error(err)
                    raise Exception(err)

            timeseries_settings = TimeseriesSettings(
                is_timeseries=True,
                order_by=obj['order_by'],
                window=obj['window'],
                use_previous_target=obj.get('use_previous_target', True),
                historical_columns=[],
                nr_predictions=obj.get('nr_predictions', 1)
            )
            for setting in obj:
                timeseries_settings.__setattr__(setting, obj[setting])

        else:
            timeseries_settings = TimeseriesSettings(is_timeseries=False)

        return timeseries_settings

    @staticmethod
    def from_json(data: str):
        return TimeseriesSettings.from_dict(json.loads(data))

    def to_dict(self, encode_json=False) -> Dict[str, Json]:
        return _asdict(self, encode_json=encode_json)

    def to_json(self) -> Dict[str, Json]:
        return json.dumps(self.to_dict())


@dataclass
class ProblemDefinition:
    target: str
    nfolds: int
    pct_invalid: float
    unbias_target: bool
    seconds_per_model: Union[int, None]
    seconds_per_encoder: Union[int, None]
    time_aim: Union[int, None]
    target_weights: Union[List[float], None]
    positive_domain: bool
    fixed_confidence: Union[int, float, None]
    timeseries_settings: TimeseriesSettings
    anomaly_detection: bool
    anomaly_error_rate: Union[float, None]
    anomaly_cooldown: int
    ignore_features: List[str]
    fit_on_validation: bool
    strict_mode: bool

    @staticmethod
    def from_dict(obj: Dict):
        target = obj['target']
        nfolds = obj.get('nfolds', 30)
        pct_invalid = obj.get('pct_invalid', 1)
        unbias_target = obj.get('unbias_target', False)
        seconds_per_model = obj.get('seconds_per_model', None)
        seconds_per_encoder = obj.get('seconds_per_encoder', None)
        time_aim = obj.get('time_aim', None)
        target_weights = obj.get('target_weights', None)
        positive_domain = obj.get('positive_domain', False)
        fixed_confidence = obj.get('fixed_confidence', None)
        timeseries_settings = TimeseriesSettings.from_dict(obj.get('timeseries_settings', {}))
        anomaly_detection = obj.get('anomaly_detection', True)
        anomaly_error_rate = obj.get('anomaly_error_rate', None)
        anomaly_cooldown = obj.get('anomaly_detection', 1)
        ignore_features = obj.get('ignore_features', [])
        fit_on_validation = obj.get('fit_on_validation', True)
        strict_mode = obj.get('strict_mode', True)

        problem_definition = ProblemDefinition(
            target=target,
            nfolds=nfolds,
            pct_invalid=pct_invalid,
            unbias_target=unbias_target,
            seconds_per_model=seconds_per_model,
            seconds_per_encoder=seconds_per_encoder,
            time_aim=time_aim,
            target_weights=target_weights,
            positive_domain=positive_domain,
            fixed_confidence=fixed_confidence,
            timeseries_settings=timeseries_settings,
            anomaly_detection=anomaly_detection,
            anomaly_error_rate=anomaly_error_rate,
            anomaly_cooldown=anomaly_cooldown,
            ignore_features=ignore_features,
            fit_on_validation=fit_on_validation,
            strict_mode=strict_mode
        )

        return problem_definition

    @staticmethod
    def from_json(data: str):
        return ProblemDefinition.from_dict(json.loads(data))

    def to_dict(self, encode_json=False) -> Dict[str, Json]:
        return _asdict(self, encode_json=encode_json)

    def to_json(self) -> Dict[str, Json]:
        return json.dumps(self.to_dict())


@dataclass
class JsonAI:
    features: Dict[str, Feature]
    outputs: Dict[str, Output]
    problem_definition: ProblemDefinition
    identifiers: Dict[str, str]
    cleaner: Optional[object] = None
    splitter: Optional[object] = None
    analyzer: Optional[object] = None
    explainer: Optional[object] = None
    imports: Optional[List[str]] = None
    timeseries_transformer: Optional[object] = None
    timeseries_analyzer: Optional[object] = None
    accuracy_functions: Optional[List[str]] = None
    phases: Optional[Dict[str, object]] = None

    @staticmethod
    def from_dict(obj: Dict):
        features = {k: Feature.from_dict(v) for k, v in obj['features'].items()}
        outputs = {k: Output.from_dict(v) for k, v in obj['outputs'].items()}
        problem_definition = ProblemDefinition.from_dict(obj['problem_definition'])
        identifiers = obj['identifiers']
        cleaner = obj.get('cleaner', None)
        splitter = obj.get('splitter', None)
        analyzer = obj.get('analyzer', None)
        explainer = obj.get('explainer', None)
        imports = obj.get('imports', None)
        timeseries_transformer = obj.get('timeseries_transformer', None)
        timeseries_analyzer = obj.get('timeseries_analyzer', None)
        accuracy_functions = obj.get('accuracy_functions', None)
        phases = obj.get('phases', None)

        json_ai = JsonAI(
            features=features,
            outputs=outputs,
            problem_definition=problem_definition,
            identifiers=identifiers,
            cleaner=cleaner,
            splitter=splitter,
            analyzer=analyzer,
            explainer=explainer,
            imports=imports,
            timeseries_transformer=timeseries_transformer,
            timeseries_analyzer=timeseries_analyzer,
            accuracy_functions=accuracy_functions,
            phases=phases
        )

        return json_ai

    @staticmethod
    def from_json(data: str):
        return JsonAI.from_dict(json.loads(data))

    def to_dict(self, encode_json=False) -> Dict[str, Json]:
        as_dict = _asdict(self, encode_json=encode_json)
        for k in list(as_dict.keys()):
            if k == 'features':
                feature_dict = {}
                for name in self.features:
                    feature_dict[name] = self.features[name].to_dict()
                as_dict[k] = feature_dict
            if as_dict[k] is None:
                del as_dict[k]
        return as_dict

    def to_json(self) -> Dict[str, Json]:
        return json.dumps(self.to_dict(), indent=4)


@dataclass_json
@dataclass
class ModelAnalysis:
    accuracies: Dict[str, float]
    accuracy_histogram: Dict[str, list]
    accuracy_samples: Dict[str, list]
    train_sample_size: int
    test_sample_size: int
    column_importances: Dict[str, float]
    confusion_matrix: object
    histograms: object
    dtypes: object

'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._521 import BiasModification
    from ._522 import FlankMicroGeometry
    from ._523 import FlankSide
    from ._524 import LeadModification
    from ._525 import LocationOfEvaluationLowerLimit
    from ._526 import LocationOfEvaluationUpperLimit
    from ._527 import LocationOfRootReliefEvaluation
    from ._528 import LocationOfTipReliefEvaluation
    from ._529 import MainProfileReliefEndsAtTheStartOfRootReliefOption
    from ._530 import MainProfileReliefEndsAtTheStartOfTipReliefOption
    from ._531 import Modification
    from ._532 import ParabolicRootReliefStartsTangentToMainProfileRelief
    from ._533 import ParabolicTipReliefStartsTangentToMainProfileRelief
    from ._534 import ProfileModification

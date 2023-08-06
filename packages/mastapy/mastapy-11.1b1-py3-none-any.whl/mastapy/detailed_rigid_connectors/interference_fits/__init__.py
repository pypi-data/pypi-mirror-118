'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1225 import AssemblyMethods
    from ._1226 import CalculationMethods
    from ._1227 import InterferenceFitDesign
    from ._1228 import InterferenceFitHalfDesign
    from ._1229 import StressRegions
    from ._1230 import Table4JointInterfaceTypes

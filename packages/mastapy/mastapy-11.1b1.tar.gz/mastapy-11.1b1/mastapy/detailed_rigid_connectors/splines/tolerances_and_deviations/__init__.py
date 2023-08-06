'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1203 import FitAndTolerance
    from ._1204 import SAESplineTolerances

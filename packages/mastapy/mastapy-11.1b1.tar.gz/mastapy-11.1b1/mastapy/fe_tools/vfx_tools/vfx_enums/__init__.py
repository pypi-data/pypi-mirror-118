'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1165 import ProSolveMpcType
    from ._1166 import ProSolveSolverType

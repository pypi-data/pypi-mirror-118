'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1205 import AGMA6123SplineHalfRating
    from ._1206 import AGMA6123SplineJointRating
    from ._1207 import DIN5466SplineHalfRating
    from ._1208 import DIN5466SplineRating
    from ._1209 import GBT17855SplineHalfRating
    from ._1210 import GBT17855SplineJointRating
    from ._1211 import SAESplineHalfRating
    from ._1212 import SAESplineJointRating
    from ._1213 import SplineHalfRating
    from ._1214 import SplineJointRating

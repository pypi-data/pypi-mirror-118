'''_1673.py

LoadedBearingDutyCycle
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_designs import (
    _1848, _1849, _1850, _1851,
    _1852
)
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_designs.rolling import (
    _1853, _1854, _1855, _1856,
    _1857, _1858, _1860, _1865,
    _1866, _1867, _1869, _1874,
    _1875, _1876, _1877, _1880,
    _1881, _1884, _1885, _1886,
    _1887, _1888, _1889
)
from mastapy.bearings.bearing_designs.fluid_film import (
    _1902, _1904, _1906, _1908,
    _1909, _1910
)
from mastapy.bearings.bearing_designs.concept import _1912, _1913, _1914
from mastapy.utility.property import _1585
from mastapy.bearings import _1605
from mastapy.bearings.bearing_results import _1674
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_LOADED_BEARING_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedBearingDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBearingDutyCycle',)


class LoadedBearingDutyCycle(_0.APIBase):
    '''LoadedBearingDutyCycle

    This is a mastapy class.
    '''

    TYPE = _LOADED_BEARING_DUTY_CYCLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBearingDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_name(self) -> 'str':
        '''str: 'DutyCycleName' is the original name of this property.'''

        return self.wrapped.DutyCycleName

    @duty_cycle_name.setter
    def duty_cycle_name(self, value: 'str'):
        self.wrapped.DutyCycleName = str(value) if value else None

    @property
    def duration(self) -> 'float':
        '''float: 'Duration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Duration

    @property
    def bearing_design(self) -> '_1848.BearingDesign':
        '''BearingDesign: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1848.BearingDesign.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to BearingDesign. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_detailed_bearing(self) -> '_1849.DetailedBearing':
        '''DetailedBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1849.DetailedBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to DetailedBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_dummy_rolling_bearing(self) -> '_1850.DummyRollingBearing':
        '''DummyRollingBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1850.DummyRollingBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to DummyRollingBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_linear_bearing(self) -> '_1851.LinearBearing':
        '''LinearBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1851.LinearBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to LinearBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_non_linear_bearing(self) -> '_1852.NonLinearBearing':
        '''NonLinearBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1852.NonLinearBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to NonLinearBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_angular_contact_ball_bearing(self) -> '_1853.AngularContactBallBearing':
        '''AngularContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1853.AngularContactBallBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AngularContactBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_angular_contact_thrust_ball_bearing(self) -> '_1854.AngularContactThrustBallBearing':
        '''AngularContactThrustBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1854.AngularContactThrustBallBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AngularContactThrustBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_asymmetric_spherical_roller_bearing(self) -> '_1855.AsymmetricSphericalRollerBearing':
        '''AsymmetricSphericalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1855.AsymmetricSphericalRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AsymmetricSphericalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_axial_thrust_cylindrical_roller_bearing(self) -> '_1856.AxialThrustCylindricalRollerBearing':
        '''AxialThrustCylindricalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1856.AxialThrustCylindricalRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AxialThrustCylindricalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_axial_thrust_needle_roller_bearing(self) -> '_1857.AxialThrustNeedleRollerBearing':
        '''AxialThrustNeedleRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1857.AxialThrustNeedleRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AxialThrustNeedleRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_ball_bearing(self) -> '_1858.BallBearing':
        '''BallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1858.BallBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to BallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_barrel_roller_bearing(self) -> '_1860.BarrelRollerBearing':
        '''BarrelRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1860.BarrelRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to BarrelRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_crossed_roller_bearing(self) -> '_1865.CrossedRollerBearing':
        '''CrossedRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1865.CrossedRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to CrossedRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_cylindrical_roller_bearing(self) -> '_1866.CylindricalRollerBearing':
        '''CylindricalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1866.CylindricalRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to CylindricalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_deep_groove_ball_bearing(self) -> '_1867.DeepGrooveBallBearing':
        '''DeepGrooveBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1867.DeepGrooveBallBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to DeepGrooveBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_four_point_contact_ball_bearing(self) -> '_1869.FourPointContactBallBearing':
        '''FourPointContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1869.FourPointContactBallBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to FourPointContactBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_multi_point_contact_ball_bearing(self) -> '_1874.MultiPointContactBallBearing':
        '''MultiPointContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1874.MultiPointContactBallBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to MultiPointContactBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_needle_roller_bearing(self) -> '_1875.NeedleRollerBearing':
        '''NeedleRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1875.NeedleRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to NeedleRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_non_barrel_roller_bearing(self) -> '_1876.NonBarrelRollerBearing':
        '''NonBarrelRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1876.NonBarrelRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to NonBarrelRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_roller_bearing(self) -> '_1877.RollerBearing':
        '''RollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1877.RollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to RollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_rolling_bearing(self) -> '_1880.RollingBearing':
        '''RollingBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1880.RollingBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to RollingBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_self_aligning_ball_bearing(self) -> '_1881.SelfAligningBallBearing':
        '''SelfAligningBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1881.SelfAligningBallBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to SelfAligningBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_spherical_roller_bearing(self) -> '_1884.SphericalRollerBearing':
        '''SphericalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1884.SphericalRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to SphericalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_spherical_roller_thrust_bearing(self) -> '_1885.SphericalRollerThrustBearing':
        '''SphericalRollerThrustBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1885.SphericalRollerThrustBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to SphericalRollerThrustBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_taper_roller_bearing(self) -> '_1886.TaperRollerBearing':
        '''TaperRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1886.TaperRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to TaperRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_three_point_contact_ball_bearing(self) -> '_1887.ThreePointContactBallBearing':
        '''ThreePointContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1887.ThreePointContactBallBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ThreePointContactBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_thrust_ball_bearing(self) -> '_1888.ThrustBallBearing':
        '''ThrustBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1888.ThrustBallBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ThrustBallBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_toroidal_roller_bearing(self) -> '_1889.ToroidalRollerBearing':
        '''ToroidalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1889.ToroidalRollerBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ToroidalRollerBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_pad_fluid_film_bearing(self) -> '_1902.PadFluidFilmBearing':
        '''PadFluidFilmBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1902.PadFluidFilmBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to PadFluidFilmBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_plain_grease_filled_journal_bearing(self) -> '_1904.PlainGreaseFilledJournalBearing':
        '''PlainGreaseFilledJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1904.PlainGreaseFilledJournalBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to PlainGreaseFilledJournalBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_plain_journal_bearing(self) -> '_1906.PlainJournalBearing':
        '''PlainJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1906.PlainJournalBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to PlainJournalBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_plain_oil_fed_journal_bearing(self) -> '_1908.PlainOilFedJournalBearing':
        '''PlainOilFedJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1908.PlainOilFedJournalBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to PlainOilFedJournalBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_tilting_pad_journal_bearing(self) -> '_1909.TiltingPadJournalBearing':
        '''TiltingPadJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1909.TiltingPadJournalBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to TiltingPadJournalBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_tilting_pad_thrust_bearing(self) -> '_1910.TiltingPadThrustBearing':
        '''TiltingPadThrustBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1910.TiltingPadThrustBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to TiltingPadThrustBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_concept_axial_clearance_bearing(self) -> '_1912.ConceptAxialClearanceBearing':
        '''ConceptAxialClearanceBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1912.ConceptAxialClearanceBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ConceptAxialClearanceBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_concept_clearance_bearing(self) -> '_1913.ConceptClearanceBearing':
        '''ConceptClearanceBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1913.ConceptClearanceBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ConceptClearanceBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def bearing_design_of_type_concept_radial_clearance_bearing(self) -> '_1914.ConceptRadialClearanceBearing':
        '''ConceptRadialClearanceBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1914.ConceptRadialClearanceBearing.TYPE not in self.wrapped.BearingDesign.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ConceptRadialClearanceBearing. Expected: {}.'.format(self.wrapped.BearingDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDesign.__class__)(self.wrapped.BearingDesign) if self.wrapped.BearingDesign else None

    @property
    def radial_load_summary(self) -> '_1585.DutyCyclePropertySummaryForce[_1605.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'RadialLoadSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1585.DutyCyclePropertySummaryForce)[_1605.BearingLoadCaseResultsLightweight](self.wrapped.RadialLoadSummary) if self.wrapped.RadialLoadSummary else None

    @property
    def z_thrust_reaction_summary(self) -> '_1585.DutyCyclePropertySummaryForce[_1605.BearingLoadCaseResultsLightweight]':
        '''DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'ZThrustReactionSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1585.DutyCyclePropertySummaryForce)[_1605.BearingLoadCaseResultsLightweight](self.wrapped.ZThrustReactionSummary) if self.wrapped.ZThrustReactionSummary else None

    @property
    def bearing_load_case_results(self) -> 'List[_1674.LoadedBearingResults]':
        '''List[LoadedBearingResults]: 'BearingLoadCaseResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BearingLoadCaseResults, constructor.new(_1674.LoadedBearingResults))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ReportNames, str)
        return value

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result

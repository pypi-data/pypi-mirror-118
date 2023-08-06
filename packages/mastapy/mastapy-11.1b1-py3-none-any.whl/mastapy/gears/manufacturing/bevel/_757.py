'''_757.py

PinionConvex
'''


from mastapy.gears.manufacturing.bevel import (
    _758, _753, _754, _756,
    _759, _760, _761
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _775
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PINION_CONVEX = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'PinionConvex')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionConvex',)


class PinionConvex(_0.APIBase):
    '''PinionConvex

    This is a mastapy class.
    '''

    TYPE = _PINION_CONVEX

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PinionConvex.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pinion_cutter_parameters_convex(self) -> '_758.PinionFinishMachineSettings':
        '''PinionFinishMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _758.PinionFinishMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConvex.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionFinishMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConvex.__class__)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_bevel_generating_modified_roll_machine_settings(self) -> '_753.PinionBevelGeneratingModifiedRollMachineSettings':
        '''PinionBevelGeneratingModifiedRollMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _753.PinionBevelGeneratingModifiedRollMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConvex.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionBevelGeneratingModifiedRollMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConvex.__class__)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_bevel_generating_tilt_machine_settings(self) -> '_754.PinionBevelGeneratingTiltMachineSettings':
        '''PinionBevelGeneratingTiltMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _754.PinionBevelGeneratingTiltMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConvex.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionBevelGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConvex.__class__)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_conical_machine_settings_specified(self) -> '_756.PinionConicalMachineSettingsSpecified':
        '''PinionConicalMachineSettingsSpecified: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _756.PinionConicalMachineSettingsSpecified.TYPE not in self.wrapped.PinionCutterParametersConvex.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionConicalMachineSettingsSpecified. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConvex.__class__)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_hypoid_formate_tilt_machine_settings(self) -> '_759.PinionHypoidFormateTiltMachineSettings':
        '''PinionHypoidFormateTiltMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _759.PinionHypoidFormateTiltMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConvex.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionHypoidFormateTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConvex.__class__)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_hypoid_generating_tilt_machine_settings(self) -> '_760.PinionHypoidGeneratingTiltMachineSettings':
        '''PinionHypoidGeneratingTiltMachineSettings: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _760.PinionHypoidGeneratingTiltMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConvex.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionHypoidGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConvex.__class__)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_cutter_parameters_convex_of_type_pinion_machine_settings_smt(self) -> '_761.PinionMachineSettingsSMT':
        '''PinionMachineSettingsSMT: 'PinionCutterParametersConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _761.PinionMachineSettingsSMT.TYPE not in self.wrapped.PinionCutterParametersConvex.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_convex to PinionMachineSettingsSMT. Expected: {}.'.format(self.wrapped.PinionCutterParametersConvex.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PinionCutterParametersConvex.__class__)(self.wrapped.PinionCutterParametersConvex) if self.wrapped.PinionCutterParametersConvex else None

    @property
    def pinion_convex_ib_configuration(self) -> '_775.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'PinionConvexIBConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_775.BasicConicalGearMachineSettingsGenerated)(self.wrapped.PinionConvexIBConfiguration) if self.wrapped.PinionConvexIBConfiguration else None

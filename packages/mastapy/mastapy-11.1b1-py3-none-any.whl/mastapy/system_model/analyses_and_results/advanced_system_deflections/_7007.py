'''_7007.py

CylindricalGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _965, _976
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1039
from mastapy.system_model.part_model.gears import _2233, _2249
from mastapy.system_model.analyses_and_results.static_loads import _6546, _6618
from mastapy.gears.rating.cylindrical import _427
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7005, _7006, _7019
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CylindricalGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetAdvancedSystemDeflection',)


class CylindricalGearSetAdvancedSystemDeflection(_7019.GearSetAdvancedSystemDeflection):
    '''CylindricalGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_set_design(self) -> '_965.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _965.CylindricalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def micro_geometry(self) -> '_1039.CylindricalGearSetMicroGeometry':
        '''CylindricalGearSetMicroGeometry: 'MicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1039.CylindricalGearSetMicroGeometry)(self.wrapped.MicroGeometry) if self.wrapped.MicroGeometry else None

    @property
    def assembly_design(self) -> '_2233.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2233.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6546.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6546.CylindricalGearSetLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to CylindricalGearSetLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_427.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_427.CylindricalGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_427.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_427.CylindricalGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def cylindrical_gears_advanced_system_deflection(self) -> 'List[_7005.CylindricalGearAdvancedSystemDeflection]':
        '''List[CylindricalGearAdvancedSystemDeflection]: 'CylindricalGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsAdvancedSystemDeflection, constructor.new(_7005.CylindricalGearAdvancedSystemDeflection))
        return value

    @property
    def cylindrical_meshes_advanced_system_deflection(self) -> 'List[_7006.CylindricalGearMeshAdvancedSystemDeflection]':
        '''List[CylindricalGearMeshAdvancedSystemDeflection]: 'CylindricalMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesAdvancedSystemDeflection, constructor.new(_7006.CylindricalGearMeshAdvancedSystemDeflection))
        return value

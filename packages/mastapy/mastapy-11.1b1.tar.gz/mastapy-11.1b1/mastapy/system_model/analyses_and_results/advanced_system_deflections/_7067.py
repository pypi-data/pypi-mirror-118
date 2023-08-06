'''_7067.py

StraightBevelDiffGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2253
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6647
from mastapy.gears.rating.straight_bevel_diff import _362
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7065, _7066, _6975
from mastapy.system_model.analyses_and_results.system_deflections import _2516
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'StraightBevelDiffGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetAdvancedSystemDeflection',)


class StraightBevelDiffGearSetAdvancedSystemDeflection(_6975.BevelGearSetAdvancedSystemDeflection):
    '''StraightBevelDiffGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2253.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6647.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6647.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_362.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_362.StraightBevelDiffGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_362.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_362.StraightBevelDiffGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def straight_bevel_diff_gears_advanced_system_deflection(self) -> 'List[_7065.StraightBevelDiffGearAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearAdvancedSystemDeflection]: 'StraightBevelDiffGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsAdvancedSystemDeflection, constructor.new(_7065.StraightBevelDiffGearAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_diff_meshes_advanced_system_deflection(self) -> 'List[_7066.StraightBevelDiffGearMeshAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearMeshAdvancedSystemDeflection]: 'StraightBevelDiffMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesAdvancedSystemDeflection, constructor.new(_7066.StraightBevelDiffGearMeshAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2516.StraightBevelDiffGearSetSystemDeflection]':
        '''List[StraightBevelDiffGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2516.StraightBevelDiffGearSetSystemDeflection))
        return value

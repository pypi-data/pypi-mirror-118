'''_6806.py

StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2255
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6650
from mastapy.system_model.analyses_and_results.system_deflections import _2519
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6804, _6805, _6713
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation',)


class StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation(_6713.BevelGearSetAdvancedTimeSteppingAnalysisForModulation):
    '''StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2255.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2255.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6650.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6650.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2519.StraightBevelGearSetSystemDeflection':
        '''StraightBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2519.StraightBevelGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def straight_bevel_gears_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6804.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelGearsAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6804.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_meshes_advanced_time_stepping_analysis_for_modulation(self) -> 'List[_6805.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelMeshesAdvancedTimeSteppingAnalysisForModulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesAdvancedTimeSteppingAnalysisForModulation, constructor.new(_6805.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value

'''_6301.py

KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2248
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6604
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6299, _6300, _6295
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis(_6295.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2248.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2248.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6604.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6604.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_critical_speed_analysis(self) -> 'List[_6299.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCriticalSpeedAnalysis, constructor.new(_6299.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_critical_speed_analysis(self) -> 'List[_6300.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCriticalSpeedAnalysis, constructor.new(_6300.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis))
        return value

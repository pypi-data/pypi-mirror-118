'''_6035.py

KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2248
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6604
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6033, _6034, _6029
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis(_6029.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis.TYPE'):
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
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_dynamic_analysis(self) -> 'List[_6033.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsDynamicAnalysis, constructor.new(_6033.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_dynamic_analysis(self) -> 'List[_6034.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesDynamicAnalysis, constructor.new(_6034.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis))
        return value

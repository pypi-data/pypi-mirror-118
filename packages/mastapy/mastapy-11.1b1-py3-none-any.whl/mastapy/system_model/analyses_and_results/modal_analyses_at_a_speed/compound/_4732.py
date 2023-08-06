'''_4732.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2248
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4730, _4731, _4726
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4603
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed(_4726.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2248.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2248.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2248.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2248.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_modal_analysis_at_a_speed(self) -> 'List[_4730.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysisAtASpeed, constructor.new(_4730.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_modal_analysis_at_a_speed(self) -> 'List[_4731.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysisAtASpeed, constructor.new(_4731.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtASpeed))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4603.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4603.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4603.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4603.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed))
        return value

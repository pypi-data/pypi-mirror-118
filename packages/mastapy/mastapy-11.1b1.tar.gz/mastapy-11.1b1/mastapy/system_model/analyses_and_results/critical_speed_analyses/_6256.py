'''_6256.py

ConceptGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2229
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6524
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6254, _6255, _6287
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'ConceptGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCriticalSpeedAnalysis',)


class ConceptGearSetCriticalSpeedAnalysis(_6287.GearSetCriticalSpeedAnalysis):
    '''ConceptGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2229.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2229.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6524.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6524.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_critical_speed_analysis(self) -> 'List[_6254.ConceptGearCriticalSpeedAnalysis]':
        '''List[ConceptGearCriticalSpeedAnalysis]: 'ConceptGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCriticalSpeedAnalysis, constructor.new(_6254.ConceptGearCriticalSpeedAnalysis))
        return value

    @property
    def concept_meshes_critical_speed_analysis(self) -> 'List[_6255.ConceptGearMeshCriticalSpeedAnalysis]':
        '''List[ConceptGearMeshCriticalSpeedAnalysis]: 'ConceptMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCriticalSpeedAnalysis, constructor.new(_6255.ConceptGearMeshCriticalSpeedAnalysis))
        return value

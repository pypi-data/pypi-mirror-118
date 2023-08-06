'''_4853.py

HypoidGearSetModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2242
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6591
from mastapy.system_model.analyses_and_results.system_deflections import _2466
from mastapy.system_model.analyses_and_results.modal_analyses import _4852, _4851, _4793
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'HypoidGearSetModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetModalAnalysis',)


class HypoidGearSetModalAnalysis(_4793.AGMAGleasonConicalGearSetModalAnalysis):
    '''HypoidGearSetModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2242.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2242.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6591.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6591.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2466.HypoidGearSetSystemDeflection':
        '''HypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2466.HypoidGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def hypoid_gears_modal_analysis(self) -> 'List[_4852.HypoidGearModalAnalysis]':
        '''List[HypoidGearModalAnalysis]: 'HypoidGearsModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsModalAnalysis, constructor.new(_4852.HypoidGearModalAnalysis))
        return value

    @property
    def hypoid_meshes_modal_analysis(self) -> 'List[_4851.HypoidGearMeshModalAnalysis]':
        '''List[HypoidGearMeshModalAnalysis]: 'HypoidMeshesModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesModalAnalysis, constructor.new(_4851.HypoidGearMeshModalAnalysis))
        return value

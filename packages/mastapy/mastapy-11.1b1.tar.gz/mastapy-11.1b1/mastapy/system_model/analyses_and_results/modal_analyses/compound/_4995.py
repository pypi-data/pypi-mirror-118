'''_4995.py

FaceGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2236
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4993, _4994, _5000
from mastapy.system_model.analyses_and_results.modal_analyses import _4843
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'FaceGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundModalAnalysis',)


class FaceGearSetCompoundModalAnalysis(_5000.GearSetCompoundModalAnalysis):
    '''FaceGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2236.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2236.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2236.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2236.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_modal_analysis(self) -> 'List[_4993.FaceGearCompoundModalAnalysis]':
        '''List[FaceGearCompoundModalAnalysis]: 'FaceGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundModalAnalysis, constructor.new(_4993.FaceGearCompoundModalAnalysis))
        return value

    @property
    def face_meshes_compound_modal_analysis(self) -> 'List[_4994.FaceGearMeshCompoundModalAnalysis]':
        '''List[FaceGearMeshCompoundModalAnalysis]: 'FaceMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundModalAnalysis, constructor.new(_4994.FaceGearMeshCompoundModalAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4843.FaceGearSetModalAnalysis]':
        '''List[FaceGearSetModalAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4843.FaceGearSetModalAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4843.FaceGearSetModalAnalysis]':
        '''List[FaceGearSetModalAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4843.FaceGearSetModalAnalysis))
        return value

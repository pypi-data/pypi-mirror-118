'''_4056.py

FaceGearSetParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2236
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6568
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4055, _4054, _4061
from mastapy.system_model.analyses_and_results.system_deflections import _2457
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'FaceGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetParametricStudyTool',)


class FaceGearSetParametricStudyTool(_4061.GearSetParametricStudyTool):
    '''FaceGearSetParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2236.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2236.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6568.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6568.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_parametric_study_tool(self) -> 'List[_4055.FaceGearParametricStudyTool]':
        '''List[FaceGearParametricStudyTool]: 'FaceGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsParametricStudyTool, constructor.new(_4055.FaceGearParametricStudyTool))
        return value

    @property
    def face_meshes_parametric_study_tool(self) -> 'List[_4054.FaceGearMeshParametricStudyTool]':
        '''List[FaceGearMeshParametricStudyTool]: 'FaceMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesParametricStudyTool, constructor.new(_4054.FaceGearMeshParametricStudyTool))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2457.FaceGearSetSystemDeflection]':
        '''List[FaceGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2457.FaceGearSetSystemDeflection))
        return value

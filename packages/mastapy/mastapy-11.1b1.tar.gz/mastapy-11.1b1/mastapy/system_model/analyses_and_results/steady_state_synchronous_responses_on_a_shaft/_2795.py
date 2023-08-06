'''_2795.py

StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model.gears import _2255
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6650
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2796, _2794, _2702
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft',)


class StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft(_2702.BevelGearSetSteadyStateSynchronousResponseOnAShaft):
    '''StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft.TYPE'):
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
    def straight_bevel_gears_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2796.StraightBevelGearSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelGearSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelGearsSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsSteadyStateSynchronousResponseOnAShaft, constructor.new(_2796.StraightBevelGearSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def straight_bevel_meshes_steady_state_synchronous_response_on_a_shaft(self) -> 'List[_2794.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelMeshesSteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesSteadyStateSynchronousResponseOnAShaft, constructor.new(_2794.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft))
        return value

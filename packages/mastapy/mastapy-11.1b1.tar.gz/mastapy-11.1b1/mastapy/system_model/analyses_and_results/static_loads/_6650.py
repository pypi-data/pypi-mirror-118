'''_6650.py

StraightBevelGearSetLoadCase
'''


from typing import List

from mastapy.system_model.part_model.gears import _2255
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6648, _6649, _6511
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetLoadCase',)


class StraightBevelGearSetLoadCase(_6511.BevelGearSetLoadCase):
    '''StraightBevelGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetLoadCase.TYPE'):
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
    def gears(self) -> 'List[_6648.StraightBevelGearLoadCase]':
        '''List[StraightBevelGearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_6648.StraightBevelGearLoadCase))
        return value

    @property
    def straight_bevel_gears_load_case(self) -> 'List[_6648.StraightBevelGearLoadCase]':
        '''List[StraightBevelGearLoadCase]: 'StraightBevelGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsLoadCase, constructor.new(_6648.StraightBevelGearLoadCase))
        return value

    @property
    def straight_bevel_meshes_load_case(self) -> 'List[_6649.StraightBevelGearMeshLoadCase]':
        '''List[StraightBevelGearMeshLoadCase]: 'StraightBevelMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesLoadCase, constructor.new(_6649.StraightBevelGearMeshLoadCase))
        return value

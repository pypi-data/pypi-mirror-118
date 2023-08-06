'''_4625.py

ShaftModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2190
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6635
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4530
from mastapy._internal.python_net import python_net_import

_SHAFT_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'ShaftModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftModalAnalysisAtASpeed',)


class ShaftModalAnalysisAtASpeed(_4530.AbstractShaftModalAnalysisAtASpeed):
    '''ShaftModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SHAFT_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2190.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6635.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6635.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftModalAnalysisAtASpeed]':
        '''List[ShaftModalAnalysisAtASpeed]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftModalAnalysisAtASpeed))
        return value

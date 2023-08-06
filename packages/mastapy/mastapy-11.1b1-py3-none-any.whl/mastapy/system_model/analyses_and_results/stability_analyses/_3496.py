'''_3496.py

ConceptGearStabilityAnalysis
'''


from mastapy.system_model.part_model.gears import _2228
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6522
from mastapy.system_model.analyses_and_results.stability_analyses import _3526
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ConceptGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearStabilityAnalysis',)


class ConceptGearStabilityAnalysis(_3526.GearStabilityAnalysis):
    '''ConceptGearStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2228.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6522.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6522.ConceptGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

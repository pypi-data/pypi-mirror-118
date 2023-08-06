'''_3544.py

OilSealStabilityAnalysis
'''


from mastapy.system_model.part_model import _2174
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6611
from mastapy.system_model.analyses_and_results.stability_analyses import _3501
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'OilSealStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealStabilityAnalysis',)


class OilSealStabilityAnalysis(_3501.ConnectorStabilityAnalysis):
    '''OilSealStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2174.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6611.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6611.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

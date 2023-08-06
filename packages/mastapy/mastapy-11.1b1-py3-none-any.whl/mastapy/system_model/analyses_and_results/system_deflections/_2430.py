'''_2430.py

ConnectorSystemDeflection
'''


from typing import List

from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2156, _2149, _2174
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.couplings import _2305
from mastapy.system_model.analyses_and_results.system_deflections import _2459, _2484
from mastapy.math_utility.measured_vectors import _1345
from mastapy.system_model.fe import _2093
from mastapy.system_model.analyses_and_results.power_flows import (
    _3768, _3740, _3811, _3830
)
from mastapy._internal.python_net import python_net_import

_CONNECTOR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConnectorSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorSystemDeflection',)


class ConnectorSystemDeflection(_2484.MountableComponentSystemDeflection):
    '''ConnectorSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def linear_force_on_inner(self) -> 'Vector3D':
        '''Vector3D: 'LinearForceOnInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.LinearForceOnInner)
        return value

    @property
    def moment_on_inner(self) -> 'Vector3D':
        '''Vector3D: 'MomentOnInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.MomentOnInner)
        return value

    @property
    def convergence_delta_energy(self) -> 'float':
        '''float: 'ConvergenceDeltaEnergy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConvergenceDeltaEnergy

    @property
    def component_design(self) -> '_2156.Connector':
        '''Connector: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2156.Connector.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Connector. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bearing(self) -> '_2149.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.Bearing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Bearing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_oil_seal(self) -> '_2174.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2174.OilSeal.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to OilSeal. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft_hub_connection(self) -> '_2305.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2305.ShaftHubConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def outer_fe_part(self) -> '_2459.FEPartSystemDeflection':
        '''FEPartSystemDeflection: 'OuterFEPart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2459.FEPartSystemDeflection)(self.wrapped.OuterFEPart) if self.wrapped.OuterFEPart else None

    @property
    def force_on_outer_support_in_wcs(self) -> '_1345.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'ForceOnOuterSupportInWCS' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1345.VectorWithLinearAndAngularComponents)(self.wrapped.ForceOnOuterSupportInWCS) if self.wrapped.ForceOnOuterSupportInWCS else None

    @property
    def force_on_outer_support_in_lcs(self) -> '_1345.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'ForceOnOuterSupportInLCS' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1345.VectorWithLinearAndAngularComponents)(self.wrapped.ForceOnOuterSupportInLCS) if self.wrapped.ForceOnOuterSupportInLCS else None

    @property
    def outer_fe_substructure_nodes(self) -> 'List[_2093.FESubstructureNode]':
        '''List[FESubstructureNode]: 'OuterFESubstructureNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OuterFESubstructureNodes, constructor.new(_2093.FESubstructureNode))
        return value

    @property
    def power_flow_results(self) -> '_3768.ConnectorPowerFlow':
        '''ConnectorPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3768.ConnectorPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ConnectorPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_bearing_power_flow(self) -> '_3740.BearingPowerFlow':
        '''BearingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3740.BearingPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to BearingPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_oil_seal_power_flow(self) -> '_3811.OilSealPowerFlow':
        '''OilSealPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3811.OilSealPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to OilSealPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_shaft_hub_connection_power_flow(self) -> '_3830.ShaftHubConnectionPowerFlow':
        '''ShaftHubConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3830.ShaftHubConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ShaftHubConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

'''_5450.py

PartHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model import (
    _2176, _2143, _2144, _2145,
    _2146, _2149, _2151, _2152,
    _2153, _2156, _2157, _2160,
    _2161, _2162, _2163, _2170,
    _2171, _2172, _2174, _2177,
    _2179, _2180, _2182, _2184,
    _2185, _2187
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2190
from mastapy.system_model.part_model.gears import (
    _2220, _2221, _2222, _2223,
    _2224, _2225, _2226, _2227,
    _2228, _2229, _2230, _2231,
    _2232, _2233, _2234, _2235,
    _2236, _2237, _2239, _2241,
    _2242, _2243, _2244, _2245,
    _2246, _2247, _2248, _2249,
    _2250, _2251, _2252, _2253,
    _2254, _2255, _2256, _2257,
    _2258, _2259, _2260, _2261
)
from mastapy.system_model.part_model.cycloidal import _2275, _2276, _2277
from mastapy.system_model.part_model.couplings import (
    _2283, _2285, _2286, _2288,
    _2289, _2290, _2291, _2293,
    _2294, _2295, _2296, _2297,
    _2303, _2304, _2305, _2307,
    _2308, _2309, _2311, _2312,
    _2313, _2314, _2315, _2317
)
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5432
from mastapy.system_model.analyses_and_results.modal_analyses import (
    _4872, _4787, _4788, _4789,
    _4792, _4793, _4794, _4795,
    _4797, _4799, _4800, _4801,
    _4802, _4804, _4805, _4806,
    _4807, _4809, _4810, _4812,
    _4814, _4815, _4817, _4818,
    _4820, _4821, _4823, _4826,
    _4827, _4829, _4830, _4831,
    _4833, _4836, _4837, _4838,
    _4839, _4840, _4842, _4843,
    _4844, _4845, _4848, _4849,
    _4850, _4852, _4853, _4856,
    _4857, _4859, _4860, _4862,
    _4863, _4864, _4865, _4869,
    _4870, _4874, _4875, _4877,
    _4878, _4879, _4880, _4881,
    _4882, _4884, _4886, _4887,
    _4888, _4889, _4892, _4894,
    _4895, _4897, _4898, _4900,
    _4901, _4903, _4904, _4905,
    _4906, _4907, _4908, _4909,
    _4910, _4912, _4913, _4914,
    _4915, _4916, _4923, _4924,
    _4926, _4927
)
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5713
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6757
from mastapy.system_model.analyses_and_results.analysis_cases import _7232
from mastapy._internal.python_net import python_net_import

_PART_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'PartHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('PartHarmonicAnalysisOfSingleExcitation',)


class PartHarmonicAnalysisOfSingleExcitation(_7232.PartStaticLoadAnalysisCase):
    '''PartHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _PART_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2176.Part':
        '''Part: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2176.Part.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Part. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_assembly(self) -> '_2143.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_abstract_assembly(self) -> '_2144.AbstractAssembly':
        '''AbstractAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2144.AbstractAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_abstract_shaft(self) -> '_2145.AbstractShaft':
        '''AbstractShaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.AbstractShaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_abstract_shaft_or_housing(self) -> '_2146.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.AbstractShaftOrHousing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

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
    def component_design_of_type_bolt(self) -> '_2151.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.Bolt.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Bolt. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bolted_joint(self) -> '_2152.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2152.BoltedJoint.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BoltedJoint. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_component(self) -> '_2153.Component':
        '''Component: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2153.Component.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Component. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_connector(self) -> '_2156.Connector':
        '''Connector: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2156.Connector.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Connector. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_datum(self) -> '_2157.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2157.Datum.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Datum. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_external_cad_model(self) -> '_2160.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.ExternalCADModel.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ExternalCADModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_fe_part(self) -> '_2161.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2161.FEPart.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FEPart. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_flexible_pin_assembly(self) -> '_2162.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2162.FlexiblePinAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_guide_dxf_model(self) -> '_2163.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.GuideDxfModel.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to GuideDxfModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_mass_disc(self) -> '_2170.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2170.MassDisc.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MassDisc. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_measurement_component(self) -> '_2171.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2171.MeasurementComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MeasurementComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_mountable_component(self) -> '_2172.MountableComponent':
        '''MountableComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2172.MountableComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MountableComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

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
    def component_design_of_type_planet_carrier(self) -> '_2177.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.PlanetCarrier.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PlanetCarrier. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_point_load(self) -> '_2179.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2179.PointLoad.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PointLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_power_load(self) -> '_2180.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2180.PowerLoad.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PowerLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_root_assembly(self) -> '_2182.RootAssembly':
        '''RootAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2182.RootAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RootAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_specialised_assembly(self) -> '_2184.SpecialisedAssembly':
        '''SpecialisedAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2184.SpecialisedAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpecialisedAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_unbalanced_mass(self) -> '_2185.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.UnbalancedMass.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to UnbalancedMass. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_virtual_component(self) -> '_2187.VirtualComponent':
        '''VirtualComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2187.VirtualComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to VirtualComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_2190.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2190.Shaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_agma_gleason_conical_gear(self) -> '_2220.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2220.AGMAGleasonConicalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_agma_gleason_conical_gear_set(self) -> '_2221.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2221.AGMAGleasonConicalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear(self) -> '_2222.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2222.BevelDifferentialGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear_set(self) -> '_2223.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2223.BevelDifferentialGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_planet_gear(self) -> '_2224.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2224.BevelDifferentialPlanetGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_sun_gear(self) -> '_2225.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2225.BevelDifferentialSunGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_gear(self) -> '_2226.BevelGear':
        '''BevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.BevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_gear_set(self) -> '_2227.BevelGearSet':
        '''BevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2227.BevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear(self) -> '_2228.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.ConceptGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear_set(self) -> '_2229.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2229.ConceptGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_conical_gear(self) -> '_2230.ConicalGear':
        '''ConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2230.ConicalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConicalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_conical_gear_set(self) -> '_2231.ConicalGearSet':
        '''ConicalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2231.ConicalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConicalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear(self) -> '_2232.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2232.CylindricalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear_set(self) -> '_2233.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2233.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_planet_gear(self) -> '_2234.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2234.CylindricalPlanetGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear(self) -> '_2235.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2235.FaceGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FaceGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear_set(self) -> '_2236.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2236.FaceGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FaceGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_gear(self) -> '_2237.Gear':
        '''Gear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2237.Gear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Gear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_gear_set(self) -> '_2239.GearSet':
        '''GearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2239.GearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to GearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear(self) -> '_2241.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2241.HypoidGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to HypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear_set(self) -> '_2242.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2242.HypoidGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to HypoidGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2243.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2243.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2244.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2244.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2245.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2245.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2246.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2246.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2247.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2248.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2248.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planetary_gear_set(self) -> '_2249.PlanetaryGearSet':
        '''PlanetaryGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2249.PlanetaryGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear(self) -> '_2250.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.SpiralBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear_set(self) -> '_2251.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2251.SpiralBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear(self) -> '_2252.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.StraightBevelDiffGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear_set(self) -> '_2253.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2253.StraightBevelDiffGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear(self) -> '_2254.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.StraightBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear_set(self) -> '_2255.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2255.StraightBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_planet_gear(self) -> '_2256.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.StraightBevelPlanetGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_sun_gear(self) -> '_2257.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2257.StraightBevelSunGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear(self) -> '_2258.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.WormGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to WormGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear_set(self) -> '_2259.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2259.WormGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to WormGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear(self) -> '_2260.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.ZerolBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear_set(self) -> '_2261.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.ZerolBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cycloidal_assembly(self) -> '_2275.CycloidalAssembly':
        '''CycloidalAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2275.CycloidalAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cycloidal_disc(self) -> '_2276.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2276.CycloidalDisc.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDisc. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_ring_pins(self) -> '_2277.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2277.RingPins.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RingPins. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_belt_drive(self) -> '_2283.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.BeltDrive.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BeltDrive. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch(self) -> '_2285.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2285.Clutch.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Clutch. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_half(self) -> '_2286.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.ClutchHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ClutchHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling(self) -> '_2288.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2288.ConceptCoupling.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCoupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_half(self) -> '_2289.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2289.ConceptCouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coupling(self) -> '_2290.Coupling':
        '''Coupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2290.Coupling.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Coupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coupling_half(self) -> '_2291.CouplingHalf':
        '''CouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2291.CouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt(self) -> '_2293.CVT':
        '''CVT: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2293.CVT.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVT. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_pulley(self) -> '_2294.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2294.CVTPulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVTPulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_part_to_part_shear_coupling(self) -> '_2295.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2295.PartToPartShearCoupling.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCoupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_part_to_part_shear_coupling_half(self) -> '_2296.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2296.PartToPartShearCouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_pulley(self) -> '_2297.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2297.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring(self) -> '_2303.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2303.RollingRing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring_assembly(self) -> '_2304.RollingRingAssembly':
        '''RollingRingAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2304.RollingRingAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRingAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

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
    def component_design_of_type_spring_damper(self) -> '_2307.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2307.SpringDamper.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamper. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_half(self) -> '_2308.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2308.SpringDamperHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser(self) -> '_2309.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2309.Synchroniser.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Synchroniser. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_half(self) -> '_2311.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2311.SynchroniserHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_part(self) -> '_2312.SynchroniserPart':
        '''SynchroniserPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2312.SynchroniserPart.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserPart. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_sleeve(self) -> '_2313.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2313.SynchroniserSleeve.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter(self) -> '_2314.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2314.TorqueConverter.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverter. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_pump(self) -> '_2315.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2315.TorqueConverterPump.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_turbine(self) -> '_2317.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.TorqueConverterTurbine.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def harmonic_analysis_of_single_excitation(self) -> '_5432.HarmonicAnalysisOfSingleExcitation':
        '''HarmonicAnalysisOfSingleExcitation: 'HarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5432.HarmonicAnalysisOfSingleExcitation)(self.wrapped.HarmonicAnalysisOfSingleExcitation) if self.wrapped.HarmonicAnalysisOfSingleExcitation else None

    @property
    def uncoupled_modal_analysis(self) -> '_4872.PartModalAnalysis':
        '''PartModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4872.PartModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PartModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_abstract_assembly_modal_analysis(self) -> '_4787.AbstractAssemblyModalAnalysis':
        '''AbstractAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4787.AbstractAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AbstractAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_abstract_shaft_modal_analysis(self) -> '_4788.AbstractShaftModalAnalysis':
        '''AbstractShaftModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4788.AbstractShaftModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AbstractShaftModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_abstract_shaft_or_housing_modal_analysis(self) -> '_4789.AbstractShaftOrHousingModalAnalysis':
        '''AbstractShaftOrHousingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4789.AbstractShaftOrHousingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AbstractShaftOrHousingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_agma_gleason_conical_gear_modal_analysis(self) -> '_4792.AGMAGleasonConicalGearModalAnalysis':
        '''AGMAGleasonConicalGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4792.AGMAGleasonConicalGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AGMAGleasonConicalGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_agma_gleason_conical_gear_set_modal_analysis(self) -> '_4793.AGMAGleasonConicalGearSetModalAnalysis':
        '''AGMAGleasonConicalGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4793.AGMAGleasonConicalGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AGMAGleasonConicalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_assembly_modal_analysis(self) -> '_4794.AssemblyModalAnalysis':
        '''AssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4794.AssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bearing_modal_analysis(self) -> '_4795.BearingModalAnalysis':
        '''BearingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4795.BearingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BearingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_belt_drive_modal_analysis(self) -> '_4797.BeltDriveModalAnalysis':
        '''BeltDriveModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4797.BeltDriveModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BeltDriveModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_differential_gear_modal_analysis(self) -> '_4799.BevelDifferentialGearModalAnalysis':
        '''BevelDifferentialGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4799.BevelDifferentialGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelDifferentialGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_differential_gear_set_modal_analysis(self) -> '_4800.BevelDifferentialGearSetModalAnalysis':
        '''BevelDifferentialGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4800.BevelDifferentialGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelDifferentialGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_differential_planet_gear_modal_analysis(self) -> '_4801.BevelDifferentialPlanetGearModalAnalysis':
        '''BevelDifferentialPlanetGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4801.BevelDifferentialPlanetGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelDifferentialPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_differential_sun_gear_modal_analysis(self) -> '_4802.BevelDifferentialSunGearModalAnalysis':
        '''BevelDifferentialSunGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4802.BevelDifferentialSunGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelDifferentialSunGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_gear_modal_analysis(self) -> '_4804.BevelGearModalAnalysis':
        '''BevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4804.BevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_gear_set_modal_analysis(self) -> '_4805.BevelGearSetModalAnalysis':
        '''BevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4805.BevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bolted_joint_modal_analysis(self) -> '_4806.BoltedJointModalAnalysis':
        '''BoltedJointModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4806.BoltedJointModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BoltedJointModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bolt_modal_analysis(self) -> '_4807.BoltModalAnalysis':
        '''BoltModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4807.BoltModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BoltModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_clutch_half_modal_analysis(self) -> '_4809.ClutchHalfModalAnalysis':
        '''ClutchHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4809.ClutchHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ClutchHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_clutch_modal_analysis(self) -> '_4810.ClutchModalAnalysis':
        '''ClutchModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4810.ClutchModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ClutchModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_component_modal_analysis(self) -> '_4812.ComponentModalAnalysis':
        '''ComponentModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4812.ComponentModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ComponentModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_concept_coupling_half_modal_analysis(self) -> '_4814.ConceptCouplingHalfModalAnalysis':
        '''ConceptCouplingHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4814.ConceptCouplingHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConceptCouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_concept_coupling_modal_analysis(self) -> '_4815.ConceptCouplingModalAnalysis':
        '''ConceptCouplingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4815.ConceptCouplingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConceptCouplingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_concept_gear_modal_analysis(self) -> '_4817.ConceptGearModalAnalysis':
        '''ConceptGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4817.ConceptGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConceptGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_concept_gear_set_modal_analysis(self) -> '_4818.ConceptGearSetModalAnalysis':
        '''ConceptGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4818.ConceptGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConceptGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_conical_gear_modal_analysis(self) -> '_4820.ConicalGearModalAnalysis':
        '''ConicalGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4820.ConicalGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConicalGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_conical_gear_set_modal_analysis(self) -> '_4821.ConicalGearSetModalAnalysis':
        '''ConicalGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4821.ConicalGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConicalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_connector_modal_analysis(self) -> '_4823.ConnectorModalAnalysis':
        '''ConnectorModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4823.ConnectorModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConnectorModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_coupling_half_modal_analysis(self) -> '_4826.CouplingHalfModalAnalysis':
        '''CouplingHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4826.CouplingHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_coupling_modal_analysis(self) -> '_4827.CouplingModalAnalysis':
        '''CouplingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4827.CouplingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CouplingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cvt_modal_analysis(self) -> '_4829.CVTModalAnalysis':
        '''CVTModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4829.CVTModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CVTModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cvt_pulley_modal_analysis(self) -> '_4830.CVTPulleyModalAnalysis':
        '''CVTPulleyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4830.CVTPulleyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CVTPulleyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cycloidal_assembly_modal_analysis(self) -> '_4831.CycloidalAssemblyModalAnalysis':
        '''CycloidalAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4831.CycloidalAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CycloidalAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cycloidal_disc_modal_analysis(self) -> '_4833.CycloidalDiscModalAnalysis':
        '''CycloidalDiscModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4833.CycloidalDiscModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CycloidalDiscModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cylindrical_gear_modal_analysis(self) -> '_4836.CylindricalGearModalAnalysis':
        '''CylindricalGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4836.CylindricalGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CylindricalGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cylindrical_gear_set_modal_analysis(self) -> '_4837.CylindricalGearSetModalAnalysis':
        '''CylindricalGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4837.CylindricalGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CylindricalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cylindrical_planet_gear_modal_analysis(self) -> '_4838.CylindricalPlanetGearModalAnalysis':
        '''CylindricalPlanetGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4838.CylindricalPlanetGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CylindricalPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_datum_modal_analysis(self) -> '_4839.DatumModalAnalysis':
        '''DatumModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4839.DatumModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to DatumModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_external_cad_model_modal_analysis(self) -> '_4840.ExternalCADModelModalAnalysis':
        '''ExternalCADModelModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4840.ExternalCADModelModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ExternalCADModelModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_face_gear_modal_analysis(self) -> '_4842.FaceGearModalAnalysis':
        '''FaceGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4842.FaceGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to FaceGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_face_gear_set_modal_analysis(self) -> '_4843.FaceGearSetModalAnalysis':
        '''FaceGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4843.FaceGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to FaceGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_fe_part_modal_analysis(self) -> '_4844.FEPartModalAnalysis':
        '''FEPartModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4844.FEPartModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to FEPartModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_flexible_pin_assembly_modal_analysis(self) -> '_4845.FlexiblePinAssemblyModalAnalysis':
        '''FlexiblePinAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4845.FlexiblePinAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to FlexiblePinAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_gear_modal_analysis(self) -> '_4848.GearModalAnalysis':
        '''GearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4848.GearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to GearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_gear_set_modal_analysis(self) -> '_4849.GearSetModalAnalysis':
        '''GearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4849.GearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to GearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_guide_dxf_model_modal_analysis(self) -> '_4850.GuideDxfModelModalAnalysis':
        '''GuideDxfModelModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4850.GuideDxfModelModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to GuideDxfModelModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_hypoid_gear_modal_analysis(self) -> '_4852.HypoidGearModalAnalysis':
        '''HypoidGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4852.HypoidGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to HypoidGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_hypoid_gear_set_modal_analysis(self) -> '_4853.HypoidGearSetModalAnalysis':
        '''HypoidGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4853.HypoidGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to HypoidGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_conical_gear_modal_analysis(self) -> '_4856.KlingelnbergCycloPalloidConicalGearModalAnalysis':
        '''KlingelnbergCycloPalloidConicalGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4856.KlingelnbergCycloPalloidConicalGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidConicalGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis(self) -> '_4857.KlingelnbergCycloPalloidConicalGearSetModalAnalysis':
        '''KlingelnbergCycloPalloidConicalGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4857.KlingelnbergCycloPalloidConicalGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidConicalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis(self) -> '_4859.KlingelnbergCycloPalloidHypoidGearModalAnalysis':
        '''KlingelnbergCycloPalloidHypoidGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4859.KlingelnbergCycloPalloidHypoidGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidHypoidGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis(self) -> '_4860.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis':
        '''KlingelnbergCycloPalloidHypoidGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4860.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidHypoidGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis(self) -> '_4862.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis':
        '''KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4862.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis(self) -> '_4863.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4863.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_mass_disc_modal_analysis(self) -> '_4864.MassDiscModalAnalysis':
        '''MassDiscModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4864.MassDiscModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to MassDiscModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_measurement_component_modal_analysis(self) -> '_4865.MeasurementComponentModalAnalysis':
        '''MeasurementComponentModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4865.MeasurementComponentModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to MeasurementComponentModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_mountable_component_modal_analysis(self) -> '_4869.MountableComponentModalAnalysis':
        '''MountableComponentModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4869.MountableComponentModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to MountableComponentModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_oil_seal_modal_analysis(self) -> '_4870.OilSealModalAnalysis':
        '''OilSealModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4870.OilSealModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to OilSealModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_part_to_part_shear_coupling_half_modal_analysis(self) -> '_4874.PartToPartShearCouplingHalfModalAnalysis':
        '''PartToPartShearCouplingHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4874.PartToPartShearCouplingHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PartToPartShearCouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_part_to_part_shear_coupling_modal_analysis(self) -> '_4875.PartToPartShearCouplingModalAnalysis':
        '''PartToPartShearCouplingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4875.PartToPartShearCouplingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PartToPartShearCouplingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_planetary_gear_set_modal_analysis(self) -> '_4877.PlanetaryGearSetModalAnalysis':
        '''PlanetaryGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4877.PlanetaryGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PlanetaryGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_planet_carrier_modal_analysis(self) -> '_4878.PlanetCarrierModalAnalysis':
        '''PlanetCarrierModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4878.PlanetCarrierModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PlanetCarrierModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_point_load_modal_analysis(self) -> '_4879.PointLoadModalAnalysis':
        '''PointLoadModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4879.PointLoadModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PointLoadModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_power_load_modal_analysis(self) -> '_4880.PowerLoadModalAnalysis':
        '''PowerLoadModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4880.PowerLoadModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PowerLoadModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_pulley_modal_analysis(self) -> '_4881.PulleyModalAnalysis':
        '''PulleyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4881.PulleyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PulleyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_ring_pins_modal_analysis(self) -> '_4882.RingPinsModalAnalysis':
        '''RingPinsModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4882.RingPinsModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to RingPinsModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_rolling_ring_assembly_modal_analysis(self) -> '_4884.RollingRingAssemblyModalAnalysis':
        '''RollingRingAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4884.RollingRingAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to RollingRingAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_rolling_ring_modal_analysis(self) -> '_4886.RollingRingModalAnalysis':
        '''RollingRingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4886.RollingRingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to RollingRingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_root_assembly_modal_analysis(self) -> '_4887.RootAssemblyModalAnalysis':
        '''RootAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4887.RootAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to RootAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_shaft_hub_connection_modal_analysis(self) -> '_4888.ShaftHubConnectionModalAnalysis':
        '''ShaftHubConnectionModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4888.ShaftHubConnectionModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ShaftHubConnectionModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_shaft_modal_analysis(self) -> '_4889.ShaftModalAnalysis':
        '''ShaftModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4889.ShaftModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ShaftModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_specialised_assembly_modal_analysis(self) -> '_4892.SpecialisedAssemblyModalAnalysis':
        '''SpecialisedAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4892.SpecialisedAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpecialisedAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_spiral_bevel_gear_modal_analysis(self) -> '_4894.SpiralBevelGearModalAnalysis':
        '''SpiralBevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4894.SpiralBevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpiralBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_spiral_bevel_gear_set_modal_analysis(self) -> '_4895.SpiralBevelGearSetModalAnalysis':
        '''SpiralBevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4895.SpiralBevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpiralBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_spring_damper_half_modal_analysis(self) -> '_4897.SpringDamperHalfModalAnalysis':
        '''SpringDamperHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4897.SpringDamperHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpringDamperHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_spring_damper_modal_analysis(self) -> '_4898.SpringDamperModalAnalysis':
        '''SpringDamperModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4898.SpringDamperModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpringDamperModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_diff_gear_modal_analysis(self) -> '_4900.StraightBevelDiffGearModalAnalysis':
        '''StraightBevelDiffGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4900.StraightBevelDiffGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelDiffGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_diff_gear_set_modal_analysis(self) -> '_4901.StraightBevelDiffGearSetModalAnalysis':
        '''StraightBevelDiffGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4901.StraightBevelDiffGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelDiffGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_gear_modal_analysis(self) -> '_4903.StraightBevelGearModalAnalysis':
        '''StraightBevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4903.StraightBevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_gear_set_modal_analysis(self) -> '_4904.StraightBevelGearSetModalAnalysis':
        '''StraightBevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4904.StraightBevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_planet_gear_modal_analysis(self) -> '_4905.StraightBevelPlanetGearModalAnalysis':
        '''StraightBevelPlanetGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4905.StraightBevelPlanetGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_sun_gear_modal_analysis(self) -> '_4906.StraightBevelSunGearModalAnalysis':
        '''StraightBevelSunGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4906.StraightBevelSunGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelSunGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_synchroniser_half_modal_analysis(self) -> '_4907.SynchroniserHalfModalAnalysis':
        '''SynchroniserHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4907.SynchroniserHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SynchroniserHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_synchroniser_modal_analysis(self) -> '_4908.SynchroniserModalAnalysis':
        '''SynchroniserModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4908.SynchroniserModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SynchroniserModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_synchroniser_part_modal_analysis(self) -> '_4909.SynchroniserPartModalAnalysis':
        '''SynchroniserPartModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4909.SynchroniserPartModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SynchroniserPartModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_synchroniser_sleeve_modal_analysis(self) -> '_4910.SynchroniserSleeveModalAnalysis':
        '''SynchroniserSleeveModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4910.SynchroniserSleeveModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SynchroniserSleeveModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_torque_converter_modal_analysis(self) -> '_4912.TorqueConverterModalAnalysis':
        '''TorqueConverterModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4912.TorqueConverterModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to TorqueConverterModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_torque_converter_pump_modal_analysis(self) -> '_4913.TorqueConverterPumpModalAnalysis':
        '''TorqueConverterPumpModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4913.TorqueConverterPumpModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to TorqueConverterPumpModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_torque_converter_turbine_modal_analysis(self) -> '_4914.TorqueConverterTurbineModalAnalysis':
        '''TorqueConverterTurbineModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4914.TorqueConverterTurbineModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to TorqueConverterTurbineModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_unbalanced_mass_modal_analysis(self) -> '_4915.UnbalancedMassModalAnalysis':
        '''UnbalancedMassModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4915.UnbalancedMassModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to UnbalancedMassModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_virtual_component_modal_analysis(self) -> '_4916.VirtualComponentModalAnalysis':
        '''VirtualComponentModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4916.VirtualComponentModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to VirtualComponentModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_worm_gear_modal_analysis(self) -> '_4923.WormGearModalAnalysis':
        '''WormGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4923.WormGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to WormGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_worm_gear_set_modal_analysis(self) -> '_4924.WormGearSetModalAnalysis':
        '''WormGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4924.WormGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to WormGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_zerol_bevel_gear_modal_analysis(self) -> '_4926.ZerolBevelGearModalAnalysis':
        '''ZerolBevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4926.ZerolBevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ZerolBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_zerol_bevel_gear_set_modal_analysis(self) -> '_4927.ZerolBevelGearSetModalAnalysis':
        '''ZerolBevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4927.ZerolBevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ZerolBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.UncoupledModalAnalysis.__class__)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def harmonic_analysis_options(self) -> '_5713.HarmonicAnalysisOptions':
        '''HarmonicAnalysisOptions: 'HarmonicAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5713.HarmonicAnalysisOptions.TYPE not in self.wrapped.HarmonicAnalysisOptions.__class__.__mro__:
            raise CastException('Failed to cast harmonic_analysis_options to HarmonicAnalysisOptions. Expected: {}.'.format(self.wrapped.HarmonicAnalysisOptions.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicAnalysisOptions.__class__)(self.wrapped.HarmonicAnalysisOptions) if self.wrapped.HarmonicAnalysisOptions else None

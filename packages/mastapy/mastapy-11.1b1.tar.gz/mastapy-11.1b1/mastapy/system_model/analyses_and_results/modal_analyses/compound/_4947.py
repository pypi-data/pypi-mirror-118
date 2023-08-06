'''_4947.py

AssemblyCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2143, _2182
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses import _4794
from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
    _4948, _4950, _4953, _4959,
    _4960, _4961, _4966, _4971,
    _4981, _4983, _4985, _4989,
    _4995, _4996, _4997, _5004,
    _5011, _5014, _5015, _5016,
    _5018, _5020, _5025, _5026,
    _5027, _5036, _5029, _5031,
    _5035, _5041, _5042, _5047,
    _5050, _5053, _5057, _5061,
    _5065, _5068, _4940
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'AssemblyCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysis',)


class AssemblyCompoundModalAnalysis(_4940.AbstractAssemblyCompoundModalAnalysis):
    '''AssemblyCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2143.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2143.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4794.AssemblyModalAnalysis]':
        '''List[AssemblyModalAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4794.AssemblyModalAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_4948.BearingCompoundModalAnalysis]':
        '''List[BearingCompoundModalAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4948.BearingCompoundModalAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_4950.BeltDriveCompoundModalAnalysis]':
        '''List[BeltDriveCompoundModalAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4950.BeltDriveCompoundModalAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4953.BevelDifferentialGearSetCompoundModalAnalysis]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4953.BevelDifferentialGearSetCompoundModalAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_4959.BoltCompoundModalAnalysis]':
        '''List[BoltCompoundModalAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4959.BoltCompoundModalAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_4960.BoltedJointCompoundModalAnalysis]':
        '''List[BoltedJointCompoundModalAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4960.BoltedJointCompoundModalAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_4961.ClutchCompoundModalAnalysis]':
        '''List[ClutchCompoundModalAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4961.ClutchCompoundModalAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_4966.ConceptCouplingCompoundModalAnalysis]':
        '''List[ConceptCouplingCompoundModalAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4966.ConceptCouplingCompoundModalAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4971.ConceptGearSetCompoundModalAnalysis]':
        '''List[ConceptGearSetCompoundModalAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4971.ConceptGearSetCompoundModalAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_4981.CVTCompoundModalAnalysis]':
        '''List[CVTCompoundModalAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4981.CVTCompoundModalAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_4983.CycloidalAssemblyCompoundModalAnalysis]':
        '''List[CycloidalAssemblyCompoundModalAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_4983.CycloidalAssemblyCompoundModalAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_4985.CycloidalDiscCompoundModalAnalysis]':
        '''List[CycloidalDiscCompoundModalAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_4985.CycloidalDiscCompoundModalAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4989.CylindricalGearSetCompoundModalAnalysis]':
        '''List[CylindricalGearSetCompoundModalAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4989.CylindricalGearSetCompoundModalAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4995.FaceGearSetCompoundModalAnalysis]':
        '''List[FaceGearSetCompoundModalAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4995.FaceGearSetCompoundModalAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_4996.FEPartCompoundModalAnalysis]':
        '''List[FEPartCompoundModalAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_4996.FEPartCompoundModalAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4997.FlexiblePinAssemblyCompoundModalAnalysis]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4997.FlexiblePinAssemblyCompoundModalAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5004.HypoidGearSetCompoundModalAnalysis]':
        '''List[HypoidGearSetCompoundModalAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5004.HypoidGearSetCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5011.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5011.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5014.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5014.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5015.MassDiscCompoundModalAnalysis]':
        '''List[MassDiscCompoundModalAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5015.MassDiscCompoundModalAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5016.MeasurementComponentCompoundModalAnalysis]':
        '''List[MeasurementComponentCompoundModalAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5016.MeasurementComponentCompoundModalAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5018.OilSealCompoundModalAnalysis]':
        '''List[OilSealCompoundModalAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5018.OilSealCompoundModalAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5020.PartToPartShearCouplingCompoundModalAnalysis]':
        '''List[PartToPartShearCouplingCompoundModalAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5020.PartToPartShearCouplingCompoundModalAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5025.PlanetCarrierCompoundModalAnalysis]':
        '''List[PlanetCarrierCompoundModalAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5025.PlanetCarrierCompoundModalAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5026.PointLoadCompoundModalAnalysis]':
        '''List[PointLoadCompoundModalAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5026.PointLoadCompoundModalAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5027.PowerLoadCompoundModalAnalysis]':
        '''List[PowerLoadCompoundModalAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5027.PowerLoadCompoundModalAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5036.ShaftHubConnectionCompoundModalAnalysis]':
        '''List[ShaftHubConnectionCompoundModalAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5036.ShaftHubConnectionCompoundModalAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5029.RingPinsCompoundModalAnalysis]':
        '''List[RingPinsCompoundModalAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5029.RingPinsCompoundModalAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5031.RollingRingAssemblyCompoundModalAnalysis]':
        '''List[RollingRingAssemblyCompoundModalAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5031.RollingRingAssemblyCompoundModalAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5035.ShaftCompoundModalAnalysis]':
        '''List[ShaftCompoundModalAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5035.ShaftCompoundModalAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5041.SpiralBevelGearSetCompoundModalAnalysis]':
        '''List[SpiralBevelGearSetCompoundModalAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5041.SpiralBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5042.SpringDamperCompoundModalAnalysis]':
        '''List[SpringDamperCompoundModalAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5042.SpringDamperCompoundModalAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5047.StraightBevelDiffGearSetCompoundModalAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5047.StraightBevelDiffGearSetCompoundModalAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5050.StraightBevelGearSetCompoundModalAnalysis]':
        '''List[StraightBevelGearSetCompoundModalAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5050.StraightBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5053.SynchroniserCompoundModalAnalysis]':
        '''List[SynchroniserCompoundModalAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5053.SynchroniserCompoundModalAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5057.TorqueConverterCompoundModalAnalysis]':
        '''List[TorqueConverterCompoundModalAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5057.TorqueConverterCompoundModalAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5061.UnbalancedMassCompoundModalAnalysis]':
        '''List[UnbalancedMassCompoundModalAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5061.UnbalancedMassCompoundModalAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5065.WormGearSetCompoundModalAnalysis]':
        '''List[WormGearSetCompoundModalAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5065.WormGearSetCompoundModalAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5068.ZerolBevelGearSetCompoundModalAnalysis]':
        '''List[ZerolBevelGearSetCompoundModalAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5068.ZerolBevelGearSetCompoundModalAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4794.AssemblyModalAnalysis]':
        '''List[AssemblyModalAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4794.AssemblyModalAnalysis))
        return value

'''_6097.py

AssemblyCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2143, _2182
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5967
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6098, _6100, _6103, _6109,
    _6110, _6111, _6116, _6121,
    _6131, _6133, _6135, _6139,
    _6145, _6146, _6147, _6154,
    _6161, _6164, _6165, _6166,
    _6168, _6170, _6175, _6176,
    _6177, _6186, _6179, _6181,
    _6185, _6191, _6192, _6197,
    _6200, _6203, _6207, _6211,
    _6215, _6218, _6090
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'AssemblyCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundDynamicAnalysis',)


class AssemblyCompoundDynamicAnalysis(_6090.AbstractAssemblyCompoundDynamicAnalysis):
    '''AssemblyCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundDynamicAnalysis.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_5967.AssemblyDynamicAnalysis]':
        '''List[AssemblyDynamicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5967.AssemblyDynamicAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_6098.BearingCompoundDynamicAnalysis]':
        '''List[BearingCompoundDynamicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6098.BearingCompoundDynamicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_6100.BeltDriveCompoundDynamicAnalysis]':
        '''List[BeltDriveCompoundDynamicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6100.BeltDriveCompoundDynamicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6103.BevelDifferentialGearSetCompoundDynamicAnalysis]':
        '''List[BevelDifferentialGearSetCompoundDynamicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6103.BevelDifferentialGearSetCompoundDynamicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_6109.BoltCompoundDynamicAnalysis]':
        '''List[BoltCompoundDynamicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6109.BoltCompoundDynamicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_6110.BoltedJointCompoundDynamicAnalysis]':
        '''List[BoltedJointCompoundDynamicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6110.BoltedJointCompoundDynamicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_6111.ClutchCompoundDynamicAnalysis]':
        '''List[ClutchCompoundDynamicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6111.ClutchCompoundDynamicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_6116.ConceptCouplingCompoundDynamicAnalysis]':
        '''List[ConceptCouplingCompoundDynamicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6116.ConceptCouplingCompoundDynamicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6121.ConceptGearSetCompoundDynamicAnalysis]':
        '''List[ConceptGearSetCompoundDynamicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6121.ConceptGearSetCompoundDynamicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_6131.CVTCompoundDynamicAnalysis]':
        '''List[CVTCompoundDynamicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6131.CVTCompoundDynamicAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6133.CycloidalAssemblyCompoundDynamicAnalysis]':
        '''List[CycloidalAssemblyCompoundDynamicAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6133.CycloidalAssemblyCompoundDynamicAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6135.CycloidalDiscCompoundDynamicAnalysis]':
        '''List[CycloidalDiscCompoundDynamicAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6135.CycloidalDiscCompoundDynamicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6139.CylindricalGearSetCompoundDynamicAnalysis]':
        '''List[CylindricalGearSetCompoundDynamicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6139.CylindricalGearSetCompoundDynamicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6145.FaceGearSetCompoundDynamicAnalysis]':
        '''List[FaceGearSetCompoundDynamicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6145.FaceGearSetCompoundDynamicAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_6146.FEPartCompoundDynamicAnalysis]':
        '''List[FEPartCompoundDynamicAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6146.FEPartCompoundDynamicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6147.FlexiblePinAssemblyCompoundDynamicAnalysis]':
        '''List[FlexiblePinAssemblyCompoundDynamicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6147.FlexiblePinAssemblyCompoundDynamicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6154.HypoidGearSetCompoundDynamicAnalysis]':
        '''List[HypoidGearSetCompoundDynamicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6154.HypoidGearSetCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6161.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6161.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6164.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6164.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_6165.MassDiscCompoundDynamicAnalysis]':
        '''List[MassDiscCompoundDynamicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6165.MassDiscCompoundDynamicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_6166.MeasurementComponentCompoundDynamicAnalysis]':
        '''List[MeasurementComponentCompoundDynamicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6166.MeasurementComponentCompoundDynamicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_6168.OilSealCompoundDynamicAnalysis]':
        '''List[OilSealCompoundDynamicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6168.OilSealCompoundDynamicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6170.PartToPartShearCouplingCompoundDynamicAnalysis]':
        '''List[PartToPartShearCouplingCompoundDynamicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6170.PartToPartShearCouplingCompoundDynamicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_6175.PlanetCarrierCompoundDynamicAnalysis]':
        '''List[PlanetCarrierCompoundDynamicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6175.PlanetCarrierCompoundDynamicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_6176.PointLoadCompoundDynamicAnalysis]':
        '''List[PointLoadCompoundDynamicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6176.PointLoadCompoundDynamicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_6177.PowerLoadCompoundDynamicAnalysis]':
        '''List[PowerLoadCompoundDynamicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6177.PowerLoadCompoundDynamicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6186.ShaftHubConnectionCompoundDynamicAnalysis]':
        '''List[ShaftHubConnectionCompoundDynamicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6186.ShaftHubConnectionCompoundDynamicAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_6179.RingPinsCompoundDynamicAnalysis]':
        '''List[RingPinsCompoundDynamicAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6179.RingPinsCompoundDynamicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6181.RollingRingAssemblyCompoundDynamicAnalysis]':
        '''List[RollingRingAssemblyCompoundDynamicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6181.RollingRingAssemblyCompoundDynamicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_6185.ShaftCompoundDynamicAnalysis]':
        '''List[ShaftCompoundDynamicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6185.ShaftCompoundDynamicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6191.SpiralBevelGearSetCompoundDynamicAnalysis]':
        '''List[SpiralBevelGearSetCompoundDynamicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6191.SpiralBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_6192.SpringDamperCompoundDynamicAnalysis]':
        '''List[SpringDamperCompoundDynamicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6192.SpringDamperCompoundDynamicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6197.StraightBevelDiffGearSetCompoundDynamicAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundDynamicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6197.StraightBevelDiffGearSetCompoundDynamicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6200.StraightBevelGearSetCompoundDynamicAnalysis]':
        '''List[StraightBevelGearSetCompoundDynamicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6200.StraightBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6203.SynchroniserCompoundDynamicAnalysis]':
        '''List[SynchroniserCompoundDynamicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6203.SynchroniserCompoundDynamicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6207.TorqueConverterCompoundDynamicAnalysis]':
        '''List[TorqueConverterCompoundDynamicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6207.TorqueConverterCompoundDynamicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6211.UnbalancedMassCompoundDynamicAnalysis]':
        '''List[UnbalancedMassCompoundDynamicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6211.UnbalancedMassCompoundDynamicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6215.WormGearSetCompoundDynamicAnalysis]':
        '''List[WormGearSetCompoundDynamicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6215.WormGearSetCompoundDynamicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6218.ZerolBevelGearSetCompoundDynamicAnalysis]':
        '''List[ZerolBevelGearSetCompoundDynamicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6218.ZerolBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5967.AssemblyDynamicAnalysis]':
        '''List[AssemblyDynamicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5967.AssemblyDynamicAnalysis))
        return value

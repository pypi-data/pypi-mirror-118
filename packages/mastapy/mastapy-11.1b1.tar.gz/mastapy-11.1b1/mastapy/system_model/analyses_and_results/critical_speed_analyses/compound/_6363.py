'''_6363.py

AssemblyCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2143, _2182
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6232
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6364, _6366, _6369, _6375,
    _6376, _6377, _6382, _6387,
    _6397, _6399, _6401, _6405,
    _6411, _6412, _6413, _6420,
    _6427, _6430, _6431, _6432,
    _6434, _6436, _6441, _6442,
    _6443, _6452, _6445, _6447,
    _6451, _6457, _6458, _6463,
    _6466, _6469, _6473, _6477,
    _6481, _6484, _6356
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'AssemblyCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundCriticalSpeedAnalysis',)


class AssemblyCompoundCriticalSpeedAnalysis(_6356.AbstractAssemblyCompoundCriticalSpeedAnalysis):
    '''AssemblyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundCriticalSpeedAnalysis.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_6232.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6232.AssemblyCriticalSpeedAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_6364.BearingCompoundCriticalSpeedAnalysis]':
        '''List[BearingCompoundCriticalSpeedAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6364.BearingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_6366.BeltDriveCompoundCriticalSpeedAnalysis]':
        '''List[BeltDriveCompoundCriticalSpeedAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6366.BeltDriveCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6369.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6369.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_6375.BoltCompoundCriticalSpeedAnalysis]':
        '''List[BoltCompoundCriticalSpeedAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6375.BoltCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_6376.BoltedJointCompoundCriticalSpeedAnalysis]':
        '''List[BoltedJointCompoundCriticalSpeedAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6376.BoltedJointCompoundCriticalSpeedAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_6377.ClutchCompoundCriticalSpeedAnalysis]':
        '''List[ClutchCompoundCriticalSpeedAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6377.ClutchCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_6382.ConceptCouplingCompoundCriticalSpeedAnalysis]':
        '''List[ConceptCouplingCompoundCriticalSpeedAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6382.ConceptCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6387.ConceptGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ConceptGearSetCompoundCriticalSpeedAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6387.ConceptGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_6397.CVTCompoundCriticalSpeedAnalysis]':
        '''List[CVTCompoundCriticalSpeedAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6397.CVTCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6399.CycloidalAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalAssemblyCompoundCriticalSpeedAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6399.CycloidalAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6401.CycloidalDiscCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalDiscCompoundCriticalSpeedAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6401.CycloidalDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6405.CylindricalGearSetCompoundCriticalSpeedAnalysis]':
        '''List[CylindricalGearSetCompoundCriticalSpeedAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6405.CylindricalGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6411.FaceGearSetCompoundCriticalSpeedAnalysis]':
        '''List[FaceGearSetCompoundCriticalSpeedAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6411.FaceGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_6412.FEPartCompoundCriticalSpeedAnalysis]':
        '''List[FEPartCompoundCriticalSpeedAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6412.FEPartCompoundCriticalSpeedAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6413.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6413.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6420.HypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[HypoidGearSetCompoundCriticalSpeedAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6420.HypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6427.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6427.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6430.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6430.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_6431.MassDiscCompoundCriticalSpeedAnalysis]':
        '''List[MassDiscCompoundCriticalSpeedAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6431.MassDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_6432.MeasurementComponentCompoundCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCompoundCriticalSpeedAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6432.MeasurementComponentCompoundCriticalSpeedAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_6434.OilSealCompoundCriticalSpeedAnalysis]':
        '''List[OilSealCompoundCriticalSpeedAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6434.OilSealCompoundCriticalSpeedAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6436.PartToPartShearCouplingCompoundCriticalSpeedAnalysis]':
        '''List[PartToPartShearCouplingCompoundCriticalSpeedAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6436.PartToPartShearCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_6441.PlanetCarrierCompoundCriticalSpeedAnalysis]':
        '''List[PlanetCarrierCompoundCriticalSpeedAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6441.PlanetCarrierCompoundCriticalSpeedAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_6442.PointLoadCompoundCriticalSpeedAnalysis]':
        '''List[PointLoadCompoundCriticalSpeedAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6442.PointLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_6443.PowerLoadCompoundCriticalSpeedAnalysis]':
        '''List[PowerLoadCompoundCriticalSpeedAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6443.PowerLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6452.ShaftHubConnectionCompoundCriticalSpeedAnalysis]':
        '''List[ShaftHubConnectionCompoundCriticalSpeedAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6452.ShaftHubConnectionCompoundCriticalSpeedAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_6445.RingPinsCompoundCriticalSpeedAnalysis]':
        '''List[RingPinsCompoundCriticalSpeedAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6445.RingPinsCompoundCriticalSpeedAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6447.RollingRingAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[RollingRingAssemblyCompoundCriticalSpeedAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6447.RollingRingAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_6451.ShaftCompoundCriticalSpeedAnalysis]':
        '''List[ShaftCompoundCriticalSpeedAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6451.ShaftCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6457.SpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6457.SpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_6458.SpringDamperCompoundCriticalSpeedAnalysis]':
        '''List[SpringDamperCompoundCriticalSpeedAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6458.SpringDamperCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6463.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6463.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6466.StraightBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6466.StraightBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6469.SynchroniserCompoundCriticalSpeedAnalysis]':
        '''List[SynchroniserCompoundCriticalSpeedAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6469.SynchroniserCompoundCriticalSpeedAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6473.TorqueConverterCompoundCriticalSpeedAnalysis]':
        '''List[TorqueConverterCompoundCriticalSpeedAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6473.TorqueConverterCompoundCriticalSpeedAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6477.UnbalancedMassCompoundCriticalSpeedAnalysis]':
        '''List[UnbalancedMassCompoundCriticalSpeedAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6477.UnbalancedMassCompoundCriticalSpeedAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6481.WormGearSetCompoundCriticalSpeedAnalysis]':
        '''List[WormGearSetCompoundCriticalSpeedAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6481.WormGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6484.ZerolBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCompoundCriticalSpeedAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6484.ZerolBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6232.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6232.AssemblyCriticalSpeedAnalysis))
        return value

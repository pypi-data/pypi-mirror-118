'''_4148.py

AssemblyCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.analyses_and_results.parametric_study_tools import _4048, _4001
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2143, _2182
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4149, _4151, _4154, _4160,
    _4161, _4162, _4167, _4172,
    _4182, _4184, _4186, _4190,
    _4196, _4197, _4198, _4205,
    _4212, _4215, _4216, _4217,
    _4219, _4221, _4226, _4227,
    _4228, _4237, _4230, _4232,
    _4236, _4242, _4243, _4248,
    _4251, _4254, _4258, _4262,
    _4266, _4269, _4141
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'AssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundParametricStudyTool',)


class AssemblyCompoundParametricStudyTool(_4141.AbstractAssemblyCompoundParametricStudyTool):
    '''AssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def all_duty_cycle_results(self) -> '_4048.DutyCycleResultsForAllComponents':
        '''DutyCycleResultsForAllComponents: 'AllDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4048.DutyCycleResultsForAllComponents)(self.wrapped.AllDutyCycleResults) if self.wrapped.AllDutyCycleResults else None

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
    def assembly_analysis_cases_ready(self) -> 'List[_4001.AssemblyParametricStudyTool]':
        '''List[AssemblyParametricStudyTool]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4001.AssemblyParametricStudyTool))
        return value

    @property
    def bearings(self) -> 'List[_4149.BearingCompoundParametricStudyTool]':
        '''List[BearingCompoundParametricStudyTool]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4149.BearingCompoundParametricStudyTool))
        return value

    @property
    def belt_drives(self) -> 'List[_4151.BeltDriveCompoundParametricStudyTool]':
        '''List[BeltDriveCompoundParametricStudyTool]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4151.BeltDriveCompoundParametricStudyTool))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4154.BevelDifferentialGearSetCompoundParametricStudyTool]':
        '''List[BevelDifferentialGearSetCompoundParametricStudyTool]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4154.BevelDifferentialGearSetCompoundParametricStudyTool))
        return value

    @property
    def bolts(self) -> 'List[_4160.BoltCompoundParametricStudyTool]':
        '''List[BoltCompoundParametricStudyTool]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4160.BoltCompoundParametricStudyTool))
        return value

    @property
    def bolted_joints(self) -> 'List[_4161.BoltedJointCompoundParametricStudyTool]':
        '''List[BoltedJointCompoundParametricStudyTool]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4161.BoltedJointCompoundParametricStudyTool))
        return value

    @property
    def clutches(self) -> 'List[_4162.ClutchCompoundParametricStudyTool]':
        '''List[ClutchCompoundParametricStudyTool]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4162.ClutchCompoundParametricStudyTool))
        return value

    @property
    def concept_couplings(self) -> 'List[_4167.ConceptCouplingCompoundParametricStudyTool]':
        '''List[ConceptCouplingCompoundParametricStudyTool]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4167.ConceptCouplingCompoundParametricStudyTool))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4172.ConceptGearSetCompoundParametricStudyTool]':
        '''List[ConceptGearSetCompoundParametricStudyTool]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4172.ConceptGearSetCompoundParametricStudyTool))
        return value

    @property
    def cv_ts(self) -> 'List[_4182.CVTCompoundParametricStudyTool]':
        '''List[CVTCompoundParametricStudyTool]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4182.CVTCompoundParametricStudyTool))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_4184.CycloidalAssemblyCompoundParametricStudyTool]':
        '''List[CycloidalAssemblyCompoundParametricStudyTool]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_4184.CycloidalAssemblyCompoundParametricStudyTool))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_4186.CycloidalDiscCompoundParametricStudyTool]':
        '''List[CycloidalDiscCompoundParametricStudyTool]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_4186.CycloidalDiscCompoundParametricStudyTool))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4190.CylindricalGearSetCompoundParametricStudyTool]':
        '''List[CylindricalGearSetCompoundParametricStudyTool]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4190.CylindricalGearSetCompoundParametricStudyTool))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4196.FaceGearSetCompoundParametricStudyTool]':
        '''List[FaceGearSetCompoundParametricStudyTool]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4196.FaceGearSetCompoundParametricStudyTool))
        return value

    @property
    def fe_parts(self) -> 'List[_4197.FEPartCompoundParametricStudyTool]':
        '''List[FEPartCompoundParametricStudyTool]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_4197.FEPartCompoundParametricStudyTool))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4198.FlexiblePinAssemblyCompoundParametricStudyTool]':
        '''List[FlexiblePinAssemblyCompoundParametricStudyTool]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4198.FlexiblePinAssemblyCompoundParametricStudyTool))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4205.HypoidGearSetCompoundParametricStudyTool]':
        '''List[HypoidGearSetCompoundParametricStudyTool]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4205.HypoidGearSetCompoundParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4212.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4212.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4215.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4215.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def mass_discs(self) -> 'List[_4216.MassDiscCompoundParametricStudyTool]':
        '''List[MassDiscCompoundParametricStudyTool]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4216.MassDiscCompoundParametricStudyTool))
        return value

    @property
    def measurement_components(self) -> 'List[_4217.MeasurementComponentCompoundParametricStudyTool]':
        '''List[MeasurementComponentCompoundParametricStudyTool]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4217.MeasurementComponentCompoundParametricStudyTool))
        return value

    @property
    def oil_seals(self) -> 'List[_4219.OilSealCompoundParametricStudyTool]':
        '''List[OilSealCompoundParametricStudyTool]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4219.OilSealCompoundParametricStudyTool))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4221.PartToPartShearCouplingCompoundParametricStudyTool]':
        '''List[PartToPartShearCouplingCompoundParametricStudyTool]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4221.PartToPartShearCouplingCompoundParametricStudyTool))
        return value

    @property
    def planet_carriers(self) -> 'List[_4226.PlanetCarrierCompoundParametricStudyTool]':
        '''List[PlanetCarrierCompoundParametricStudyTool]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4226.PlanetCarrierCompoundParametricStudyTool))
        return value

    @property
    def point_loads(self) -> 'List[_4227.PointLoadCompoundParametricStudyTool]':
        '''List[PointLoadCompoundParametricStudyTool]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4227.PointLoadCompoundParametricStudyTool))
        return value

    @property
    def power_loads(self) -> 'List[_4228.PowerLoadCompoundParametricStudyTool]':
        '''List[PowerLoadCompoundParametricStudyTool]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4228.PowerLoadCompoundParametricStudyTool))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4237.ShaftHubConnectionCompoundParametricStudyTool]':
        '''List[ShaftHubConnectionCompoundParametricStudyTool]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4237.ShaftHubConnectionCompoundParametricStudyTool))
        return value

    @property
    def ring_pins(self) -> 'List[_4230.RingPinsCompoundParametricStudyTool]':
        '''List[RingPinsCompoundParametricStudyTool]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_4230.RingPinsCompoundParametricStudyTool))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4232.RollingRingAssemblyCompoundParametricStudyTool]':
        '''List[RollingRingAssemblyCompoundParametricStudyTool]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4232.RollingRingAssemblyCompoundParametricStudyTool))
        return value

    @property
    def shafts(self) -> 'List[_4236.ShaftCompoundParametricStudyTool]':
        '''List[ShaftCompoundParametricStudyTool]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4236.ShaftCompoundParametricStudyTool))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4242.SpiralBevelGearSetCompoundParametricStudyTool]':
        '''List[SpiralBevelGearSetCompoundParametricStudyTool]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4242.SpiralBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def spring_dampers(self) -> 'List[_4243.SpringDamperCompoundParametricStudyTool]':
        '''List[SpringDamperCompoundParametricStudyTool]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4243.SpringDamperCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4248.StraightBevelDiffGearSetCompoundParametricStudyTool]':
        '''List[StraightBevelDiffGearSetCompoundParametricStudyTool]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4248.StraightBevelDiffGearSetCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4251.StraightBevelGearSetCompoundParametricStudyTool]':
        '''List[StraightBevelGearSetCompoundParametricStudyTool]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4251.StraightBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def synchronisers(self) -> 'List[_4254.SynchroniserCompoundParametricStudyTool]':
        '''List[SynchroniserCompoundParametricStudyTool]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4254.SynchroniserCompoundParametricStudyTool))
        return value

    @property
    def torque_converters(self) -> 'List[_4258.TorqueConverterCompoundParametricStudyTool]':
        '''List[TorqueConverterCompoundParametricStudyTool]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4258.TorqueConverterCompoundParametricStudyTool))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4262.UnbalancedMassCompoundParametricStudyTool]':
        '''List[UnbalancedMassCompoundParametricStudyTool]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4262.UnbalancedMassCompoundParametricStudyTool))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4266.WormGearSetCompoundParametricStudyTool]':
        '''List[WormGearSetCompoundParametricStudyTool]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4266.WormGearSetCompoundParametricStudyTool))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4269.ZerolBevelGearSetCompoundParametricStudyTool]':
        '''List[ZerolBevelGearSetCompoundParametricStudyTool]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4269.ZerolBevelGearSetCompoundParametricStudyTool))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4001.AssemblyParametricStudyTool]':
        '''List[AssemblyParametricStudyTool]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4001.AssemblyParametricStudyTool))
        return value

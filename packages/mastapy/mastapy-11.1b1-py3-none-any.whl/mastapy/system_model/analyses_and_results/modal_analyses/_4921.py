'''_4921.py

WhineWaterfallSettings
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.math_utility import (
    _1287, _1314, _1275, _1301,
    _1286, _1270, _1285, _1307
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.modal_analyses import (
    _4824, _4918, _4917, _4871,
    _4919
)
from mastapy.system_model.analyses_and_results.harmonic_analyses.results import (
    _5787, _5790, _5795, _5796
)
from mastapy.system_model.drawing.options import _1972, _1970
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5701, _5755
from mastapy.utility.units_and_measurements.measurements import (
    _1437, _1390, _1489, _1396,
    _1387, _1392, _1411, _1484,
    _1405, _1455, _1456, _1459
)
from mastapy.utility.property import _1589
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_WHINE_WATERFALL_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'WhineWaterfallSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('WhineWaterfallSettings',)


class WhineWaterfallSettings(_0.APIBase):
    '''WhineWaterfallSettings

    This is a mastapy class.
    '''

    TYPE = _WHINE_WATERFALL_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WhineWaterfallSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def automatically_calculate_on_change_of_settings(self) -> 'bool':
        '''bool: 'AutomaticallyCalculateOnChangeOfSettings' is the original name of this property.'''

        return self.wrapped.AutomaticallyCalculateOnChangeOfSettings

    @automatically_calculate_on_change_of_settings.setter
    def automatically_calculate_on_change_of_settings(self, value: 'bool'):
        self.wrapped.AutomaticallyCalculateOnChangeOfSettings = bool(value) if value else False

    @property
    def show_total_response_for_multiple_surfaces(self) -> 'bool':
        '''bool: 'ShowTotalResponseForMultipleSurfaces' is the original name of this property.'''

        return self.wrapped.ShowTotalResponseForMultipleSurfaces

    @show_total_response_for_multiple_surfaces.setter
    def show_total_response_for_multiple_surfaces(self, value: 'bool'):
        self.wrapped.ShowTotalResponseForMultipleSurfaces = bool(value) if value else False

    @property
    def show_total_response_for_multiple_excitations(self) -> 'bool':
        '''bool: 'ShowTotalResponseForMultipleExcitations' is the original name of this property.'''

        return self.wrapped.ShowTotalResponseForMultipleExcitations

    @show_total_response_for_multiple_excitations.setter
    def show_total_response_for_multiple_excitations(self, value: 'bool'):
        self.wrapped.ShowTotalResponseForMultipleExcitations = bool(value) if value else False

    @property
    def response_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType':
        '''enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType: 'ResponseType' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ResponseType, value) if self.wrapped.ResponseType else None

    @response_type.setter
    def response_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ResponseType = value

    @property
    def translation_or_rotation(self) -> '_1314.TranslationRotation':
        '''TranslationRotation: 'TranslationOrRotation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.TranslationOrRotation)
        return constructor.new(_1314.TranslationRotation)(value) if value else None

    @translation_or_rotation.setter
    def translation_or_rotation(self, value: '_1314.TranslationRotation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TranslationOrRotation = value

    @property
    def coordinate_system(self) -> '_4824.CoordinateSystemForWhine':
        '''CoordinateSystemForWhine: 'CoordinateSystem' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CoordinateSystem)
        return constructor.new(_4824.CoordinateSystemForWhine)(value) if value else None

    @coordinate_system.setter
    def coordinate_system(self, value: '_4824.CoordinateSystemForWhine'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CoordinateSystem = value

    @property
    def complex_component(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption':
        '''enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption: 'ComplexComponent' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ComplexComponent, value) if self.wrapped.ComplexComponent else None

    @complex_component.setter
    def complex_component(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ComplexComponent = value

    @property
    def vector_magnitude_method(self) -> '_1301.ComplexMagnitudeMethod':
        '''ComplexMagnitudeMethod: 'VectorMagnitudeMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.VectorMagnitudeMethod)
        return constructor.new(_1301.ComplexMagnitudeMethod)(value) if value else None

    @vector_magnitude_method.setter
    def vector_magnitude_method(self, value: '_1301.ComplexMagnitudeMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.VectorMagnitudeMethod = value

    @property
    def max_harmonic(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'MaxHarmonic' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.MaxHarmonic) if self.wrapped.MaxHarmonic else None

    @max_harmonic.setter
    def max_harmonic(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0, is_overridden)
        self.wrapped.MaxHarmonic = value

    @property
    def dynamic_scaling(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling':
        '''enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling: 'DynamicScaling' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.DynamicScaling, value) if self.wrapped.DynamicScaling else None

    @dynamic_scaling.setter
    def dynamic_scaling(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DynamicScaling = value

    @property
    def weighting(self) -> '_1270.AcousticWeighting':
        '''AcousticWeighting: 'Weighting' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Weighting)
        return constructor.new(_1270.AcousticWeighting)(value) if value else None

    @weighting.setter
    def weighting(self, value: '_1270.AcousticWeighting'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Weighting = value

    @property
    def show_coupled_modes(self) -> 'bool':
        '''bool: 'ShowCoupledModes' is the original name of this property.'''

        return self.wrapped.ShowCoupledModes

    @show_coupled_modes.setter
    def show_coupled_modes(self, value: 'bool'):
        self.wrapped.ShowCoupledModes = bool(value) if value else False

    @property
    def reduce_number_of_result_points(self) -> 'bool':
        '''bool: 'ReduceNumberOfResultPoints' is the original name of this property.'''

        return self.wrapped.ReduceNumberOfResultPoints

    @reduce_number_of_result_points.setter
    def reduce_number_of_result_points(self, value: 'bool'):
        self.wrapped.ReduceNumberOfResultPoints = bool(value) if value else False

    @property
    def chart_type(self) -> '_1285.DynamicsResponse3DChartType':
        '''DynamicsResponse3DChartType: 'ChartType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ChartType)
        return constructor.new(_1285.DynamicsResponse3DChartType)(value) if value else None

    @chart_type.setter
    def chart_type(self, value: '_1285.DynamicsResponse3DChartType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ChartType = value

    @property
    def maximum_order(self) -> 'float':
        '''float: 'MaximumOrder' is the original name of this property.'''

        return self.wrapped.MaximumOrder

    @maximum_order.setter
    def maximum_order(self, value: 'float'):
        self.wrapped.MaximumOrder = float(value) if value else 0.0

    @property
    def minimum_order(self) -> 'float':
        '''float: 'MinimumOrder' is the original name of this property.'''

        return self.wrapped.MinimumOrder

    @minimum_order.setter
    def minimum_order(self, value: 'float'):
        self.wrapped.MinimumOrder = float(value) if value else 0.0

    @property
    def connected_component_type(self) -> '_5787.ConnectedComponentType':
        '''ConnectedComponentType: 'ConnectedComponentType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ConnectedComponentType)
        return constructor.new(_5787.ConnectedComponentType)(value) if value else None

    @connected_component_type.setter
    def connected_component_type(self, value: '_5787.ConnectedComponentType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ConnectedComponentType = value

    @property
    def whine_waterfall_export_option(self) -> '_4918.WhineWaterfallExportOption':
        '''WhineWaterfallExportOption: 'WhineWaterfallExportOption' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.WhineWaterfallExportOption)
        return constructor.new(_4918.WhineWaterfallExportOption)(value) if value else None

    @whine_waterfall_export_option.setter
    def whine_waterfall_export_option(self, value: '_4918.WhineWaterfallExportOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.WhineWaterfallExportOption = value

    @property
    def number_of_additional_points_either_side_of_order_line(self) -> 'int':
        '''int: 'NumberOfAdditionalPointsEitherSideOfOrderLine' is the original name of this property.'''

        return self.wrapped.NumberOfAdditionalPointsEitherSideOfOrderLine

    @number_of_additional_points_either_side_of_order_line.setter
    def number_of_additional_points_either_side_of_order_line(self, value: 'int'):
        self.wrapped.NumberOfAdditionalPointsEitherSideOfOrderLine = int(value) if value else 0

    @property
    def selected_excitations(self) -> '_5790.ExcitationSourceSelectionGroup':
        '''ExcitationSourceSelectionGroup: 'SelectedExcitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5790.ExcitationSourceSelectionGroup)(self.wrapped.SelectedExcitations) if self.wrapped.SelectedExcitations else None

    @property
    def waterfall_chart_settings(self) -> '_4917.WaterfallChartSettings':
        '''WaterfallChartSettings: 'WaterfallChartSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4917.WaterfallChartSettings)(self.wrapped.WaterfallChartSettings) if self.wrapped.WaterfallChartSettings else None

    @property
    def order_cuts_chart_settings(self) -> '_4871.OrderCutsChartSettings':
        '''OrderCutsChartSettings: 'OrderCutsChartSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4871.OrderCutsChartSettings)(self.wrapped.OrderCutsChartSettings) if self.wrapped.OrderCutsChartSettings else None

    @property
    def modal_contribution_view_options(self) -> '_1972.ModalContributionViewOptions':
        '''ModalContributionViewOptions: 'ModalContributionViewOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1972.ModalContributionViewOptions)(self.wrapped.ModalContributionViewOptions) if self.wrapped.ModalContributionViewOptions else None

    @property
    def mode_view_options(self) -> '_1970.AdvancedTimeSteppingAnalysisForModulationModeViewOptions':
        '''AdvancedTimeSteppingAnalysisForModulationModeViewOptions: 'ModeViewOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1970.AdvancedTimeSteppingAnalysisForModulationModeViewOptions)(self.wrapped.ModeViewOptions) if self.wrapped.ModeViewOptions else None

    @property
    def frequency_options(self) -> '_5701.FrequencyOptionsForHarmonicAnalysisResults':
        '''FrequencyOptionsForHarmonicAnalysisResults: 'FrequencyOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5701.FrequencyOptionsForHarmonicAnalysisResults)(self.wrapped.FrequencyOptions) if self.wrapped.FrequencyOptions else None

    @property
    def reference_speed_options(self) -> '_5755.SpeedOptionsForHarmonicAnalysisResults':
        '''SpeedOptionsForHarmonicAnalysisResults: 'ReferenceSpeedOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5755.SpeedOptionsForHarmonicAnalysisResults)(self.wrapped.ReferenceSpeedOptions) if self.wrapped.ReferenceSpeedOptions else None

    @property
    def very_short_length_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1437.LengthVeryShort]':
        '''WhineWaterfallReferenceValues[LengthVeryShort]: 'VeryShortLengthReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1437.LengthVeryShort](self.wrapped.VeryShortLengthReferenceValues) if self.wrapped.VeryShortLengthReferenceValues else None

    @property
    def small_angle_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1390.AngleSmall]':
        '''WhineWaterfallReferenceValues[AngleSmall]: 'SmallAngleReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1390.AngleSmall](self.wrapped.SmallAngleReferenceValues) if self.wrapped.SmallAngleReferenceValues else None

    @property
    def small_velocity_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1489.VelocitySmall]':
        '''WhineWaterfallReferenceValues[VelocitySmall]: 'SmallVelocityReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1489.VelocitySmall](self.wrapped.SmallVelocityReferenceValues) if self.wrapped.SmallVelocityReferenceValues else None

    @property
    def angular_velocity_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1396.AngularVelocity]':
        '''WhineWaterfallReferenceValues[AngularVelocity]: 'AngularVelocityReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1396.AngularVelocity](self.wrapped.AngularVelocityReferenceValues) if self.wrapped.AngularVelocityReferenceValues else None

    @property
    def acceleration_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1387.Acceleration]':
        '''WhineWaterfallReferenceValues[Acceleration]: 'AccelerationReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1387.Acceleration](self.wrapped.AccelerationReferenceValues) if self.wrapped.AccelerationReferenceValues else None

    @property
    def angular_acceleration_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1392.AngularAcceleration]':
        '''WhineWaterfallReferenceValues[AngularAcceleration]: 'AngularAccelerationReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1392.AngularAcceleration](self.wrapped.AngularAccelerationReferenceValues) if self.wrapped.AngularAccelerationReferenceValues else None

    @property
    def force_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1411.Force]':
        '''WhineWaterfallReferenceValues[Force]: 'ForceReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1411.Force](self.wrapped.ForceReferenceValues) if self.wrapped.ForceReferenceValues else None

    @property
    def torque_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1484.Torque]':
        '''WhineWaterfallReferenceValues[Torque]: 'TorqueReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1484.Torque](self.wrapped.TorqueReferenceValues) if self.wrapped.TorqueReferenceValues else None

    @property
    def energy_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1405.Energy]':
        '''WhineWaterfallReferenceValues[Energy]: 'EnergyReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1405.Energy](self.wrapped.EnergyReferenceValues) if self.wrapped.EnergyReferenceValues else None

    @property
    def power_small_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1455.PowerSmall]':
        '''WhineWaterfallReferenceValues[PowerSmall]: 'PowerSmallReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1455.PowerSmall](self.wrapped.PowerSmallReferenceValues) if self.wrapped.PowerSmallReferenceValues else None

    @property
    def power_small_per_unit_area_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1456.PowerSmallPerArea]':
        '''WhineWaterfallReferenceValues[PowerSmallPerArea]: 'PowerSmallPerUnitAreaReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1456.PowerSmallPerArea](self.wrapped.PowerSmallPerUnitAreaReferenceValues) if self.wrapped.PowerSmallPerUnitAreaReferenceValues else None

    @property
    def pressure_reference_values(self) -> '_4919.WhineWaterfallReferenceValues[_1459.Pressure]':
        '''WhineWaterfallReferenceValues[Pressure]: 'PressureReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4919.WhineWaterfallReferenceValues)[_1459.Pressure](self.wrapped.PressureReferenceValues) if self.wrapped.PressureReferenceValues else None

    @property
    def result_location_selection_groups(self) -> '_5795.ResultLocationSelectionGroups':
        '''ResultLocationSelectionGroups: 'ResultLocationSelectionGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5795.ResultLocationSelectionGroups)(self.wrapped.ResultLocationSelectionGroups) if self.wrapped.ResultLocationSelectionGroups else None

    @property
    def active_result_locations(self) -> 'List[_5796.ResultNodeSelection]':
        '''List[ResultNodeSelection]: 'ActiveResultLocations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ActiveResultLocations, constructor.new(_5796.ResultNodeSelection))
        return value

    @property
    def degrees_of_freedom(self) -> 'List[_1589.EnumWithBool[_1307.ResultOptionsFor3DVector]]':
        '''List[EnumWithBool[ResultOptionsFor3DVector]]: 'DegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DegreesOfFreedom, constructor.new(_1589.EnumWithBool)[_1307.ResultOptionsFor3DVector])
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ReportNames, str)
        return value

    def calculate_results(self):
        ''' 'CalculateResults' is the original name of this method.'''

        self.wrapped.CalculateResults()

    def clear_cached_results(self):
        ''' 'ClearCachedResults' is the original name of this method.'''

        self.wrapped.ClearCachedResults()

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result

'''_1381.py

MeasurementSettings
'''


from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy.utility.units_and_measurements import _1380
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.utility.units_and_measurements.measurements import (
    _1387, _1388, _1389, _1390,
    _1391, _1392, _1393, _1394,
    _1395, _1396, _1397, _1398,
    _1399, _1400, _1401, _1402,
    _1403, _1404, _1405, _1406,
    _1407, _1408, _1409, _1410,
    _1411, _1412, _1413, _1414,
    _1415, _1416, _1417, _1418,
    _1419, _1420, _1421, _1422,
    _1423, _1424, _1425, _1426,
    _1427, _1428, _1429, _1430,
    _1431, _1432, _1433, _1434,
    _1435, _1436, _1437, _1438,
    _1439, _1440, _1441, _1442,
    _1443, _1444, _1445, _1446,
    _1447, _1448, _1449, _1450,
    _1451, _1452, _1453, _1454,
    _1455, _1456, _1457, _1458,
    _1459, _1460, _1461, _1462,
    _1463, _1464, _1465, _1466,
    _1467, _1468, _1469, _1470,
    _1471, _1472, _1473, _1474,
    _1475, _1476, _1477, _1478,
    _1479, _1480, _1481, _1482,
    _1483, _1484, _1485, _1486,
    _1487, _1488, _1489, _1490,
    _1491, _1492, _1493, _1494
)
from mastapy._internal.cast_exception import CastException
from mastapy.utility import _1369
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_SETTINGS = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements', 'MeasurementSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementSettings',)


class MeasurementSettings(_1369.PerMachineSettings):
    '''MeasurementSettings

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def selected_measurement(self) -> 'list_with_selected_item.ListWithSelectedItem_MeasurementBase':
        '''list_with_selected_item.ListWithSelectedItem_MeasurementBase: 'SelectedMeasurement' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_MeasurementBase)(self.wrapped.SelectedMeasurement) if self.wrapped.SelectedMeasurement else None

    @selected_measurement.setter
    def selected_measurement(self, value: 'list_with_selected_item.ListWithSelectedItem_MeasurementBase.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_MeasurementBase.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_MeasurementBase.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.SelectedMeasurement = value

    @property
    def sample_input(self) -> 'str':
        '''str: 'SampleInput' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SampleInput

    @property
    def sample_output(self) -> 'str':
        '''str: 'SampleOutput' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SampleOutput

    @property
    def number_decimal_separator(self) -> 'str':
        '''str: 'NumberDecimalSeparator' is the original name of this property.'''

        return self.wrapped.NumberDecimalSeparator

    @number_decimal_separator.setter
    def number_decimal_separator(self, value: 'str'):
        self.wrapped.NumberDecimalSeparator = str(value) if value else None

    @property
    def number_group_separator(self) -> 'str':
        '''str: 'NumberGroupSeparator' is the original name of this property.'''

        return self.wrapped.NumberGroupSeparator

    @number_group_separator.setter
    def number_group_separator(self, value: 'str'):
        self.wrapped.NumberGroupSeparator = str(value) if value else None

    @property
    def small_number_cutoff(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SmallNumberCutoff' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SmallNumberCutoff) if self.wrapped.SmallNumberCutoff else None

    @small_number_cutoff.setter
    def small_number_cutoff(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SmallNumberCutoff = value

    @property
    def large_number_cutoff(self) -> 'float':
        '''float: 'LargeNumberCutoff' is the original name of this property.'''

        return self.wrapped.LargeNumberCutoff

    @large_number_cutoff.setter
    def large_number_cutoff(self, value: 'float'):
        self.wrapped.LargeNumberCutoff = float(value) if value else 0.0

    @property
    def show_trailing_zeros(self) -> 'bool':
        '''bool: 'ShowTrailingZeros' is the original name of this property.'''

        return self.wrapped.ShowTrailingZeros

    @show_trailing_zeros.setter
    def show_trailing_zeros(self, value: 'bool'):
        self.wrapped.ShowTrailingZeros = bool(value) if value else False

    @property
    def current_selected_measurement(self) -> '_1380.MeasurementBase':
        '''MeasurementBase: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1380.MeasurementBase.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MeasurementBase. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_acceleration(self) -> '_1387.Acceleration':
        '''Acceleration: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1387.Acceleration.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Acceleration. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angle(self) -> '_1388.Angle':
        '''Angle: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1388.Angle.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Angle. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angle_per_unit_temperature(self) -> '_1389.AnglePerUnitTemperature':
        '''AnglePerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1389.AnglePerUnitTemperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AnglePerUnitTemperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angle_small(self) -> '_1390.AngleSmall':
        '''AngleSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1390.AngleSmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngleSmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angle_very_small(self) -> '_1391.AngleVerySmall':
        '''AngleVerySmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1391.AngleVerySmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngleVerySmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_acceleration(self) -> '_1392.AngularAcceleration':
        '''AngularAcceleration: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1392.AngularAcceleration.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularAcceleration. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_compliance(self) -> '_1393.AngularCompliance':
        '''AngularCompliance: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1393.AngularCompliance.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularCompliance. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_jerk(self) -> '_1394.AngularJerk':
        '''AngularJerk: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1394.AngularJerk.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularJerk. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_stiffness(self) -> '_1395.AngularStiffness':
        '''AngularStiffness: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1395.AngularStiffness.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularStiffness. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_angular_velocity(self) -> '_1396.AngularVelocity':
        '''AngularVelocity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1396.AngularVelocity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AngularVelocity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_area(self) -> '_1397.Area':
        '''Area: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1397.Area.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Area. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_area_small(self) -> '_1398.AreaSmall':
        '''AreaSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1398.AreaSmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to AreaSmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_cycles(self) -> '_1399.Cycles':
        '''Cycles: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1399.Cycles.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Cycles. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_damage(self) -> '_1400.Damage':
        '''Damage: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1400.Damage.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Damage. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_damage_rate(self) -> '_1401.DamageRate':
        '''DamageRate: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1401.DamageRate.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to DamageRate. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_data_size(self) -> '_1402.DataSize':
        '''DataSize: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1402.DataSize.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to DataSize. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_decibel(self) -> '_1403.Decibel':
        '''Decibel: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1403.Decibel.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Decibel. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_density(self) -> '_1404.Density':
        '''Density: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1404.Density.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Density. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_energy(self) -> '_1405.Energy':
        '''Energy: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1405.Energy.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Energy. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_energy_per_unit_area(self) -> '_1406.EnergyPerUnitArea':
        '''EnergyPerUnitArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1406.EnergyPerUnitArea.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to EnergyPerUnitArea. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_energy_per_unit_area_small(self) -> '_1407.EnergyPerUnitAreaSmall':
        '''EnergyPerUnitAreaSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1407.EnergyPerUnitAreaSmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to EnergyPerUnitAreaSmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_energy_small(self) -> '_1408.EnergySmall':
        '''EnergySmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1408.EnergySmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to EnergySmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_enum(self) -> '_1409.Enum':
        '''Enum: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1409.Enum.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Enum. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_flow_rate(self) -> '_1410.FlowRate':
        '''FlowRate: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1410.FlowRate.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FlowRate. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_force(self) -> '_1411.Force':
        '''Force: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1411.Force.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Force. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_force_per_unit_length(self) -> '_1412.ForcePerUnitLength':
        '''ForcePerUnitLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1412.ForcePerUnitLength.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ForcePerUnitLength. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_force_per_unit_pressure(self) -> '_1413.ForcePerUnitPressure':
        '''ForcePerUnitPressure: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1413.ForcePerUnitPressure.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ForcePerUnitPressure. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_force_per_unit_temperature(self) -> '_1414.ForcePerUnitTemperature':
        '''ForcePerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1414.ForcePerUnitTemperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ForcePerUnitTemperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_fraction_measurement_base(self) -> '_1415.FractionMeasurementBase':
        '''FractionMeasurementBase: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1415.FractionMeasurementBase.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FractionMeasurementBase. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_frequency(self) -> '_1416.Frequency':
        '''Frequency: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1416.Frequency.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Frequency. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_fuel_consumption_engine(self) -> '_1417.FuelConsumptionEngine':
        '''FuelConsumptionEngine: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1417.FuelConsumptionEngine.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FuelConsumptionEngine. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_fuel_efficiency_vehicle(self) -> '_1418.FuelEfficiencyVehicle':
        '''FuelEfficiencyVehicle: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1418.FuelEfficiencyVehicle.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to FuelEfficiencyVehicle. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_gradient(self) -> '_1419.Gradient':
        '''Gradient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1419.Gradient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Gradient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_heat_conductivity(self) -> '_1420.HeatConductivity':
        '''HeatConductivity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1420.HeatConductivity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatConductivity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_heat_transfer(self) -> '_1421.HeatTransfer':
        '''HeatTransfer: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1421.HeatTransfer.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatTransfer. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1422.HeatTransferCoefficientForPlasticGearTooth':
        '''HeatTransferCoefficientForPlasticGearTooth: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1422.HeatTransferCoefficientForPlasticGearTooth.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_heat_transfer_resistance(self) -> '_1423.HeatTransferResistance':
        '''HeatTransferResistance: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1423.HeatTransferResistance.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to HeatTransferResistance. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_impulse(self) -> '_1424.Impulse':
        '''Impulse: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1424.Impulse.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Impulse. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_index(self) -> '_1425.Index':
        '''Index: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1425.Index.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Index. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_integer(self) -> '_1426.Integer':
        '''Integer: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1426.Integer.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Integer. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_inverse_short_length(self) -> '_1427.InverseShortLength':
        '''InverseShortLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1427.InverseShortLength.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to InverseShortLength. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_inverse_short_time(self) -> '_1428.InverseShortTime':
        '''InverseShortTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1428.InverseShortTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to InverseShortTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_jerk(self) -> '_1429.Jerk':
        '''Jerk: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1429.Jerk.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Jerk. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_kinematic_viscosity(self) -> '_1430.KinematicViscosity':
        '''KinematicViscosity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1430.KinematicViscosity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to KinematicViscosity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_long(self) -> '_1431.LengthLong':
        '''LengthLong: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1431.LengthLong.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthLong. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_medium(self) -> '_1432.LengthMedium':
        '''LengthMedium: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1432.LengthMedium.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthMedium. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_per_unit_temperature(self) -> '_1433.LengthPerUnitTemperature':
        '''LengthPerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1433.LengthPerUnitTemperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthPerUnitTemperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_short(self) -> '_1434.LengthShort':
        '''LengthShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1434.LengthShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_to_the_fourth(self) -> '_1435.LengthToTheFourth':
        '''LengthToTheFourth: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1435.LengthToTheFourth.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthToTheFourth. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_very_long(self) -> '_1436.LengthVeryLong':
        '''LengthVeryLong: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1436.LengthVeryLong.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthVeryLong. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_very_short(self) -> '_1437.LengthVeryShort':
        '''LengthVeryShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1437.LengthVeryShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthVeryShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_length_very_short_per_length_short(self) -> '_1438.LengthVeryShortPerLengthShort':
        '''LengthVeryShortPerLengthShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1438.LengthVeryShortPerLengthShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LengthVeryShortPerLengthShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_angular_damping(self) -> '_1439.LinearAngularDamping':
        '''LinearAngularDamping: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1439.LinearAngularDamping.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearAngularDamping. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_angular_stiffness_cross_term(self) -> '_1440.LinearAngularStiffnessCrossTerm':
        '''LinearAngularStiffnessCrossTerm: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1440.LinearAngularStiffnessCrossTerm.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_damping(self) -> '_1441.LinearDamping':
        '''LinearDamping: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1441.LinearDamping.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearDamping. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_flexibility(self) -> '_1442.LinearFlexibility':
        '''LinearFlexibility: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1442.LinearFlexibility.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearFlexibility. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_linear_stiffness(self) -> '_1443.LinearStiffness':
        '''LinearStiffness: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1443.LinearStiffness.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to LinearStiffness. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_mass(self) -> '_1444.Mass':
        '''Mass: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1444.Mass.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Mass. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_mass_per_unit_length(self) -> '_1445.MassPerUnitLength':
        '''MassPerUnitLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1445.MassPerUnitLength.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MassPerUnitLength. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_mass_per_unit_time(self) -> '_1446.MassPerUnitTime':
        '''MassPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1446.MassPerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MassPerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_moment_of_inertia(self) -> '_1447.MomentOfInertia':
        '''MomentOfInertia: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1447.MomentOfInertia.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MomentOfInertia. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_moment_of_inertia_per_unit_length(self) -> '_1448.MomentOfInertiaPerUnitLength':
        '''MomentOfInertiaPerUnitLength: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1448.MomentOfInertiaPerUnitLength.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MomentOfInertiaPerUnitLength. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_moment_per_unit_pressure(self) -> '_1449.MomentPerUnitPressure':
        '''MomentPerUnitPressure: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1449.MomentPerUnitPressure.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to MomentPerUnitPressure. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_number(self) -> '_1450.Number':
        '''Number: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1450.Number.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Number. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_percentage(self) -> '_1451.Percentage':
        '''Percentage: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1451.Percentage.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Percentage. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power(self) -> '_1452.Power':
        '''Power: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1452.Power.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Power. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_per_small_area(self) -> '_1453.PowerPerSmallArea':
        '''PowerPerSmallArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1453.PowerPerSmallArea.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerPerSmallArea. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_per_unit_time(self) -> '_1454.PowerPerUnitTime':
        '''PowerPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1454.PowerPerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerPerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_small(self) -> '_1455.PowerSmall':
        '''PowerSmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1455.PowerSmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_small_per_area(self) -> '_1456.PowerSmallPerArea':
        '''PowerSmallPerArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1456.PowerSmallPerArea.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmallPerArea. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1457.PowerSmallPerUnitAreaPerUnitTime':
        '''PowerSmallPerUnitAreaPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1457.PowerSmallPerUnitAreaPerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_power_small_per_unit_time(self) -> '_1458.PowerSmallPerUnitTime':
        '''PowerSmallPerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1458.PowerSmallPerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PowerSmallPerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_pressure(self) -> '_1459.Pressure':
        '''Pressure: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1459.Pressure.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Pressure. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_pressure_per_unit_time(self) -> '_1460.PressurePerUnitTime':
        '''PressurePerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1460.PressurePerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PressurePerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_pressure_velocity_product(self) -> '_1461.PressureVelocityProduct':
        '''PressureVelocityProduct: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1461.PressureVelocityProduct.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PressureVelocityProduct. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_pressure_viscosity_coefficient(self) -> '_1462.PressureViscosityCoefficient':
        '''PressureViscosityCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1462.PressureViscosityCoefficient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to PressureViscosityCoefficient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_price(self) -> '_1463.Price':
        '''Price: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1463.Price.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Price. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_quadratic_angular_damping(self) -> '_1464.QuadraticAngularDamping':
        '''QuadraticAngularDamping: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1464.QuadraticAngularDamping.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to QuadraticAngularDamping. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_quadratic_drag(self) -> '_1465.QuadraticDrag':
        '''QuadraticDrag: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1465.QuadraticDrag.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to QuadraticDrag. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_rescaled_measurement(self) -> '_1466.RescaledMeasurement':
        '''RescaledMeasurement: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1466.RescaledMeasurement.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to RescaledMeasurement. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_rotatum(self) -> '_1467.Rotatum':
        '''Rotatum: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1467.Rotatum.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Rotatum. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_safety_factor(self) -> '_1468.SafetyFactor':
        '''SafetyFactor: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1468.SafetyFactor.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SafetyFactor. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_specific_acoustic_impedance(self) -> '_1469.SpecificAcousticImpedance':
        '''SpecificAcousticImpedance: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1469.SpecificAcousticImpedance.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SpecificAcousticImpedance. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_specific_heat(self) -> '_1470.SpecificHeat':
        '''SpecificHeat: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1470.SpecificHeat.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SpecificHeat. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1471.SquareRootOfUnitForcePerUnitArea':
        '''SquareRootOfUnitForcePerUnitArea: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1471.SquareRootOfUnitForcePerUnitArea.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_stiffness_per_unit_face_width(self) -> '_1472.StiffnessPerUnitFaceWidth':
        '''StiffnessPerUnitFaceWidth: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1472.StiffnessPerUnitFaceWidth.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to StiffnessPerUnitFaceWidth. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_stress(self) -> '_1473.Stress':
        '''Stress: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1473.Stress.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Stress. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_temperature(self) -> '_1474.Temperature':
        '''Temperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1474.Temperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Temperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_temperature_difference(self) -> '_1475.TemperatureDifference':
        '''TemperatureDifference: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1475.TemperatureDifference.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TemperatureDifference. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_temperature_per_unit_time(self) -> '_1476.TemperaturePerUnitTime':
        '''TemperaturePerUnitTime: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1476.TemperaturePerUnitTime.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TemperaturePerUnitTime. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_text(self) -> '_1477.Text':
        '''Text: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1477.Text.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Text. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_thermal_contact_coefficient(self) -> '_1478.ThermalContactCoefficient':
        '''ThermalContactCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1478.ThermalContactCoefficient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ThermalContactCoefficient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_thermal_expansion_coefficient(self) -> '_1479.ThermalExpansionCoefficient':
        '''ThermalExpansionCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1479.ThermalExpansionCoefficient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ThermalExpansionCoefficient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_thermo_elastic_factor(self) -> '_1480.ThermoElasticFactor':
        '''ThermoElasticFactor: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1480.ThermoElasticFactor.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to ThermoElasticFactor. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_time(self) -> '_1481.Time':
        '''Time: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1481.Time.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Time. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_time_short(self) -> '_1482.TimeShort':
        '''TimeShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1482.TimeShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TimeShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_time_very_short(self) -> '_1483.TimeVeryShort':
        '''TimeVeryShort: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1483.TimeVeryShort.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TimeVeryShort. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_torque(self) -> '_1484.Torque':
        '''Torque: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1484.Torque.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Torque. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_torque_converter_inverse_k(self) -> '_1485.TorqueConverterInverseK':
        '''TorqueConverterInverseK: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1485.TorqueConverterInverseK.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TorqueConverterInverseK. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_torque_converter_k(self) -> '_1486.TorqueConverterK':
        '''TorqueConverterK: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1486.TorqueConverterK.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TorqueConverterK. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_torque_per_unit_temperature(self) -> '_1487.TorquePerUnitTemperature':
        '''TorquePerUnitTemperature: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1487.TorquePerUnitTemperature.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to TorquePerUnitTemperature. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_velocity(self) -> '_1488.Velocity':
        '''Velocity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1488.Velocity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Velocity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_velocity_small(self) -> '_1489.VelocitySmall':
        '''VelocitySmall: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1489.VelocitySmall.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to VelocitySmall. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_viscosity(self) -> '_1490.Viscosity':
        '''Viscosity: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1490.Viscosity.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Viscosity. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_voltage(self) -> '_1491.Voltage':
        '''Voltage: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1491.Voltage.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Voltage. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_volume(self) -> '_1492.Volume':
        '''Volume: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1492.Volume.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Volume. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_wear_coefficient(self) -> '_1493.WearCoefficient':
        '''WearCoefficient: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1493.WearCoefficient.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to WearCoefficient. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    @property
    def current_selected_measurement_of_type_yank(self) -> '_1494.Yank':
        '''Yank: 'CurrentSelectedMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1494.Yank.TYPE not in self.wrapped.CurrentSelectedMeasurement.__class__.__mro__:
            raise CastException('Failed to cast current_selected_measurement to Yank. Expected: {}.'.format(self.wrapped.CurrentSelectedMeasurement.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CurrentSelectedMeasurement.__class__)(self.wrapped.CurrentSelectedMeasurement) if self.wrapped.CurrentSelectedMeasurement else None

    def default_to_metric(self):
        ''' 'DefaultToMetric' is the original name of this method.'''

        self.wrapped.DefaultToMetric()

    def default_to_imperial(self):
        ''' 'DefaultToImperial' is the original name of this method.'''

        self.wrapped.DefaultToImperial()

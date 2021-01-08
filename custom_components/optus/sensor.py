import logging
from datetime import timedelta

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from . import FordPassEntity
from .const import CONF_UNIT, DOMAIN, SENSORS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add the Entities from the config."""
    entry = hass.data[DOMAIN][config_entry.entry_id]
    sensors = []
    for key, value in SENSORS.items():
        async_add_entities([AccountSensor(entry, key, config_entry.options)], True)

class AccountSensor(
    OptusEntity,
    Entity,
):

    def __init__(self, coordinator, sensor, options):

        self.sensor = sensor
        self.options = options
        self._attr = {}
        self.coordinator = coordinator
        self._device_id = "optus_" + sensor




    def get_value(self, ftype):
        if ftype == "state":
            if self.sensor == "daysRemaining":
                return self.coordinator.data[self.sensor]
        elif ftype == "measurement":
            if self.sensor == "daysRemaining":
                return None
        elif ftype == "attribute":
            if self.sensor == "odometer":
                return None

    @property
    def name(self):
        return "optus_" + self.sensor

    @property
    def state(self):
        return self.get_value("state")

    @property
    def device_id(self):
        return self.device_id

    @property
    def device_state_attributes(self):
        return self.get_value("attribute")

    @property
    def unit_of_measurement(self):
        return self.get_value("measurement")

    @property
    def icon(self):
        return SENSORS[self.sensor]["icon"]

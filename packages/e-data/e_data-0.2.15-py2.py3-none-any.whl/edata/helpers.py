import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from edata.connectors import *
from edata.processors import *
import asyncio
from copy import deepcopy

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ['datadis']
ATTRIBUTES = {
    "cups": None,
    "contract_p1_kW": 'kW',
    "contract_p2_kW": 'kW',
    "yesterday_kWh": 'kWh',
    "yesterday_hours": 'h',
    "yesterday_p1_kWh": 'kWh',
    "yesterday_p2_kWh": 'kWh',
    "yesterday_p3_kWh": 'kWh',
    "month_kWh": 'kWh',
    "month_daily_kWh": 'kWh',
    "month_days": 'd',
    "month_p1_kWh": 'kWh',
    "month_p2_kWh": 'kWh',
    "month_p3_kWh": 'kWh',
    "month_pvpc_€": '€',
    "last_month_kWh": 'kWh',
    "last_month_daily_kWh": 'kWh',
    "last_month_days": 'd',
    "last_month_p1_kWh": 'kWh',
    "last_month_p2_kWh": 'kWh',
    "last_month_p3_kWh": 'kWh',
    "last_month_pvpc_€": '€',
    "last_month_idle_W": 'W',
    "max_power_kW": 'kW',
    "max_power_date": None,
    "max_power_mean_kW": 'kW',
    "max_power_90perc_kW": 'kW'
}

EXPERIMENTAL_ATTRS = ['month_pvpc_€', 'last_month_pvpc_€', 'last_month_idle_W']

class PlatformError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return f'{self.message}'

class Helper ():

    def __init__ (self):
        self._data = {
            'supplies': [], 'contracts': [], 'consumptions': [], 'maximeter': [], 'pvpc': []
            }
        self._attributes = {}

    @property
    def data (self):
        return deepcopy(self._data)

    @property
    def attributes (self):
        return deepcopy(self._attributes)

class EdataHelper (Helper):

    def __init__(self, platform, username, password, cups, data=None, experimental=False, log_level=logging.WARNING) -> None:
        super().__init__()
        self._cups = cups
        self._experimental = experimental
        if data is not None:
            self._data = data
        for x in ATTRIBUTES:
            if self._experimental or x not in EXPERIMENTAL_ATTRS:
                self._attributes[x] = None
        logging.getLogger().setLevel(log_level)

        if platform == 'datadis':
            self._datadis = DatadisConnector (username, password, data=self._data, log_level=log_level)
        else:
            raise PlatformError (f'platform {platform} not supported, valid options are {PLATFORMS}')

        self.last_update = datetime (1970, 1, 1)
        if self._experimental:
            self._pvpc = EsiosConnector (data=self._data, log_level=log_level)

        for x in ATTRIBUTES:
            if self._experimental or x not in EXPERIMENTAL_ATTRS:
                self._attributes[x] = None

    async def async_update (self):
        asyncio.get_event_loop().run_in_executor(None, self.update)

    def update (self):
        if self.update_data (
            self._cups, 
            datetime (datetime.today ().year, datetime.today ().month, 1, 0, 0, 0) - relativedelta (months=12), 
            datetime.today()
            ):
            self.last_update = datetime.now()
            for i in ['supplies', 'contracts', 'consumptions', 'maximeter']:
                self._data[i] = self._datadis.data[i]
            if self._experimental:
                self._data['pvpc'] = self._pvpc.data['pvpc']
            self.process_data ()

    def update_data (self, cups, date_from=None, date_to=None):
        updated = False
        try:
            updated = self._datadis.update (cups, date_from, date_to)
            if updated and self._experimental:
                self._pvpc.update(date_from, date_to)
        except Exception as e:
            _LOGGER.error (f"unhandled exception while updating data for CUPS {cups[-4:]}")
            _LOGGER.exception (e)
        return updated

    def process_data (self):
        for f in [self.process_supplies, self.process_contracts, self.process_consumptions, self.process_maximeter, self.process_pvpc]:
            try:
                f()
            except Exception as e:
                _LOGGER.error (f"unhandled exception while updating attributes")
                _LOGGER.exception (e)

        for a in self._attributes:
            if a in ATTRIBUTES and ATTRIBUTES[a] is not None:
                self._attributes[a] = round(self._attributes[a], 2) if self._attributes[a] is not None else None

    def process_supplies (self):
        for i in self._data['supplies']:
            if i['cups'] == self._cups:
                self._attributes['cups'] = self._cups
                break

    def process_contracts (self):
        most_recent_date = datetime (1970, 1, 1)
        for i in self._data['contracts']:
            if i['date_end'] > most_recent_date:
                most_recent_date = i['date_end']
                self._attributes['contract_p1_kW'] = i.get('power_p1', None)
                self._attributes['contract_p2_kW'] = i.get('power_p2', None)
                break

    def process_consumptions (self):        

        if len(self._data['consumptions']) > 0:
            processor = ConsumptionProcessor (self._data['consumptions'])

            today_starts = datetime (
                datetime.today ().year, 
                datetime.today ().month, 
                datetime.today ().day, 0, 0, 0
            )

            self._data['consumptions_daily_sum'] = processor.group_by (key='D', dt_from=today_starts-timedelta(days=30), action='sum')
            self._data['consumptions_monthly_sum'] = processor.group_by (key='M', action='sum')

            # update yesterday
            p = processor.process_range (today_starts-timedelta(days=1), today_starts)
            self._attributes["yesterday_kWh"] = p.get('total_kWh', None)
            self._attributes["yesterday_p1_kWh"] = p.get('p1_kWh', None)
            self._attributes["yesterday_p2_kWh"] = p.get('p2_kWh', None)
            self._attributes["yesterday_p3_kWh"] = p.get('p3_kWh', None)
            self._attributes["yesterday_hours"] =  p.get('delta_h', None)

            # update current month
            month_starts = datetime (
                datetime.today ().year, 
                datetime.today ().month, 1, 0, 0, 0
            )

            p = processor.process_range (month_starts, month_starts + relativedelta(months=1))
            self._attributes["month_kWh"] = p.get('total_kWh', None)
            self._attributes["month_days"] = p.get('days', None)
            self._attributes["month_daily_kWh"] = p.get('daily_kWh', None)
            self._attributes["month_p1_kWh"] = p.get('p1_kWh', None)
            self._attributes["month_p2_kWh"] = p.get('p2_kWh', None)
            self._attributes["month_p3_kWh"] = p.get('p3_kWh', None)

            # update last month
            p = processor.process_range (month_starts - relativedelta (months=1), month_starts)
            self._attributes["last_month_kWh"] = p.get('total_kWh', None)
            self._attributes["last_month_days"] = p.get('days', None)
            self._attributes["last_month_daily_kWh"] = p.get('daily_kWh', None)
            self._attributes["last_month_p1_kWh"] = p.get('p1_kWh', None)
            self._attributes["last_month_p2_kWh"] = p.get('p2_kWh', None)
            self._attributes["last_month_p3_kWh"] = p.get('p3_kWh', None)
            if self._experimental:
                self._attributes["last_month_idle_W"] = p.get('idle_avg_W', None)

    def process_maximeter (self):
        if len(self._data['maximeter']) > 0:
            date_from = datetime (
                    datetime.today ().year, 
                    datetime.today ().month, 
                    1, 0, 0, 0
                ) - relativedelta (months=12)
            processor = MaximeterProcessor (self._data['maximeter'])
            p = processor.process_range (date_from, datetime.today())
            self._attributes['max_power_kW'] = p.get('peak_kW', None)
            self._attributes['max_power_date'] = p.get('peak_date', None)
            self._attributes['max_power_mean_kW'] = p.get('peak_mean_kWh', None)
            self._attributes['max_power_90perc_kW'] = p.get('peak_tile90_kWh', None)

    def process_pvpc (self):
        if self._experimental:
            if len(self._data['consumptions']) > 0 and len(self._data['contracts']) > 0 and len(self._data['pvpc']) > 0:
                month_starts = datetime (
                        datetime.today ().year, 
                        datetime.today ().month, 1, 0, 0, 0
                    )
                processor = BillingProcessor (self._data['consumptions'], self._data['contracts'], self._data['pvpc'])
                p = processor.process_range (month_starts, datetime.today())
                self._attributes['month_pvpc_€'] = p.get('total', None)
                p = processor.process_range (month_starts - relativedelta (months=1), month_starts)
                self._attributes['last_month_pvpc_€'] = p.get('total', None)

    def __str__(self) -> str:
        return '\n'.join([f'{i}: {self._attributes[i]}' for i in self._attributes])
import time
import calendar

import sys
from datetime import datetime, tzinfo

from dateutil.parser import parse
from pydocumentdb import document_client

from States.enums import EnumMachineState


class ComputeIndicators(object):
    WINDOW_HOURS = 24 * 3

    client = document_client.DocumentClient(
        "https://msn.documents.azure.com:443", {
            'masterKey': "BMRkzudYNfdQaWF9L3tia1GqNYzZQxTU62lbbXUUmS2NRqSDbUbnB6pJ1WvAgB3H6CIMV1P7l3xI3svm2YzdmQ==",
            "secondaryKey": "trNQkijf1a40IeGVWzBEY9ffjD80NDVDMUJcqbr1MXS8ZFbraF407IZkmjT6nlbznE1v5lhmefveUXpCfv0bIQ=="
        })

    @staticmethod
    def UTC_time_to_epoch(utc_str):
        dt = parse(utc_str)
        return calendar.timegm(dt.timetuple())

    def get_data(self, machine_id, start_epoch, end_epoch):
        return self.client.QueryDocuments(
            database_or_collection_link="dbs/MSN/colls/MachineInfos",
            query=
                """
                  SELECT * FROM
                   c
                    WHERE c.MachineInfos.MachineId = %s
                     AND (c.EventEnqueuedEpoch BETWEEN %d AND %d )
                      ORDER BY c.EventEnqueuedEpoch
                """ % (
                    machine_id,
                    start_epoch,
                    end_epoch
            ),
            partition_key="PartitionId",
            options={
                'enableCrossPartitionQuery': True
            })

    def time_in_states(self, states, data):

        states_times = {state: 0 for state in states}

        current_state, current_time, min_prod_time = EnumMachineState.Unknow, 0, sys.float_info.max

        last_nb_parts = 0

        total_parts = 0

        for info in data:

            if current_state == EnumMachineState.Production:

                production_infos = info["MachineInfos"]["ProductionInfos"]

                info_prod_time, info_nb_parts = production_infos["MinPartTime"], production_infos["PartTotal"]

                if info_prod_time < min_prod_time:
                    min_prod_time = info_prod_time

                if last_nb_parts < info_nb_parts:
                    new_nb_parts = info_nb_parts - last_nb_parts
                    last_nb_parts = new_nb_parts
                    total_parts += new_nb_parts

            if info["CurrentMachineState"] != current_state:
                states_times[current_state] += info["EventEnqueuedEpoch"] - current_time
                current_time = info["EventEnqueuedEpoch"]
                current_state = info["CurrentMachineState"]

        return states_times, min_prod_time, last_nb_parts

    def start_computing(self, machine_id, from_epoch, to_epoch):

        start_time = datetime.utcnow()

        data = self.get_data(machine_id, from_epoch, to_epoch)
        ppt = self.WINDOW_HOURS * 60 * 60

        times, min_prod_time, total_parts = self.time_in_states([
            EnumMachineState.Unknow,
            EnumMachineState.Alarm,
            EnumMachineState.Off,
            EnumMachineState.PowerOn,
            EnumMachineState.Production,
            EnumMachineState.Setup,
            EnumMachineState.WarmUp
        ], data)

        ao = total_parts
        aot = times[EnumMachineState.Production]
        to = float(aot / min_prod_time)

        availability = float(aot / ppt)
        productivity = float(ao / to)
        effectiveness = float(availability * productivity)

        for state, time in times.items():
            if state != EnumMachineState.Unknow:
                print("state %s is %d of window time" % (state, (time / (self.WINDOW_HOURS * 60 * 60)) * 100))

        print("PPT %.2f" % ppt)
        print("AO %.2f" % ao)
        print("AOT %.2f" % aot)
        print("TO %.2f" % to)
        print("Availability %.2f" % availability)
        print("Productivity %.2f" % productivity)
        print("Effectiveness %.2f" % effectiveness)

        end_time = datetime.utcnow()

        indicator_snapshot = {
            "ao": ao,
            "aot": aot,
            "to": to,
            "ppt": ppt,
            "availability": availability,
            "productivity": productivity,
            "effectiveness": effectiveness,
            "states_times": times,
            "compute_started_at": self.UTC_time_to_epoch(str(start_time)),
            "compute_ended_at": self.UTC_time_to_epoch(str(end_time)),
            "window_time": self.WINDOW_HOURS * 60 * 60,
            "machine_id": machine_id,
            "from_epoch": from_epoch,
            "to_epoch": to_epoch
        }

        self.client.CreateDocument(
            database_or_collection_link="dbs/MSN/colls/IndicatorsSnapshot",
            document=indicator_snapshot
        )




epoch = ComputeIndicators.UTC_time_to_epoch("2017-02-02T20:38:32.7640000Z")

ComputeIndicators().start_computing(
    "2160144",
    from_epoch=int(epoch - ComputeIndicators.WINDOW_HOURS * 60 * 60),
    to_epoch=epoch
)

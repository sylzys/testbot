# # # Example for metrics exporter
# # import time

# # from opencensus.ext.azure import metrics_exporter
# # from opencensus.stats import aggregation as aggregation_module
# # from opencensus.stats import measure as measure_module
# # from opencensus.stats import stats as stats_module
# # from opencensus.stats import view as view_module
# # from opencensus.tags import tag_map as tag_map_module

# # stats = stats_module.stats
# # view_manager = stats.view_manager
# # stats_recorder = stats.stats_recorder

# # CARROTS_MEASURE = measure_module.MeasureInt("carrots",
# #                                             "number of carrots",
# #                                             "carrots")
# # CARROTS_VIEW = view_module.View("carrots_view",
# #                                 "number of carrots",
# #                                 [],
# #                                 CARROTS_MEASURE,
# #                                 aggregation_module.CountAggregation())

# # # Callback function to only export the metric if value is greater than 0
# # def callback_function(envelope):
# #     return envelope.data.baseData.metrics[0].value > 0

# # def main():
# #     # Enable metrics
# #     # Set the interval in seconds in which you want to send metrics
# #     exporter = metrics_exporter.new_metrics_exporter(connection_string='InstrumentationKey=e3493735-8516-4a46-a754-1ad2348cf0f5')
# #     exporter.add_telemetry_processor(callback_function)
# #     view_manager.register_exporter(exporter)

# #     view_manager.register_view(CARROTS_VIEW)
# #     mmap = stats_recorder.new_measurement_map()
# #     tmap = tag_map_module.TagMap()

# #     mmap.measure_int_put(CARROTS_MEASURE, 1000)
# #     mmap.record(tmap)
# #     # Default export interval is every 15.0s
# #     # Your application should run for at least this amount
# #     # of time so the exporter will meet this interval
# #     # Sleep can fulfill this
# #     time.sleep(60)

# #     print("Done recording metrics")

# # if __name__ == "__main__":
# #     main()
    
# #     # Copyright 2019, OpenCensus Authors
# # #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder

CARROTS_MEASURE = measure_module.MeasureInt("botdefects",
                                                     "number of bot defects",
                                                     "botdefects")
CARROTS_VIEW = view_module.View("defect view",
                                "number of bot defects",
                                [],
                                CARROTS_MEASURE,
                                aggregation_module.CountAggregation())


def main():
    # Enable metrics
    # Set the interval in seconds in which you want to send metrics
    # TODO: you need to specify the instrumentation key in a connection string
    # and place it in the APPLICATIONINSIGHTS_CONNECTION_STRING
    # environment variable.
    exporter = metrics_exporter.new_metrics_exporter(connection_string='InstrumentationKey=e3493735-8516-4a46-a754-1ad2348cf0f5')
    view_manager.register_exporter(exporter)

    view_manager.register_view(CARROTS_VIEW)
    mmap = stats_recorder.new_measurement_map()
    tmap = tag_map_module.TagMap()

    mmap.measure_int_put(CARROTS_MEASURE, 9999900)
    mmap.record(tmap)

    print("Done recording metrics")


if __name__ == "__main__":
    main()
# import psutil, time
# from opencensus.ext.azure.trace_exporter import AzureExporter
# from opencensus.trace.samplers import ProbabilitySampler
# from opencensus.trace.tracer import Tracer
# from opencensus.ext.azure import metrics_exporter
# tracer = Tracer(exporter=AzureExporter(connection_string='InstrumentationKey=e3493735-8516-4a46-a754-1ad2348cf0f5'), sampler=ProbabilitySampler(1.0))
# _exporter = metrics_exporter.new_metrics_exporter(connection_string='InstrumentationKey=e3493735-8516-4a46-a754-1ad2348cf0f5')

# for i in range(2):
#     print(psutil.Process())
#     time.sleep(0.5)

# print("Done recording metrics")
# with tracer.span(name='Erreur'):
#     print('Hello, World!')
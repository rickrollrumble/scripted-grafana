TOTAL_POWER_QUERY = """
WITH charger_data AS (SELECT TIMESTAMP(value_timestamp) AS 'time', CAST(value AS DOUBLE) AS 'Power'
              FROM connector_meter_value
                WHERE $__timeFilter(value_timestamp)
                AND reading_context = 'Sample.Periodic'
                AND measurand = 'Power.Active.Import')
                
SELECT time, sum(Power) AS 'Power (kW)'
FROM charger_data group by time;
"""
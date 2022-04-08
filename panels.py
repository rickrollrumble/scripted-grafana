from grafanalib.core import TimeSeries, OPS_FORMAT, GridPos, Target, GaugePanel, SqlTarget

dashboard_panels = {'Cost and Revenue': [
    TimeSeries(
        title="Random Walk",
        dataSource='default',
        targets=[
            Target(
                datasource='grafana',
                expr='example',
            ),
        ],
        gridPos=GridPos(h=8, w=16, x=0, y=0),
    ),
    GaugePanel(
        title="Random Walk",
        dataSource='default',
        targets=[
            Target(
                datasource='grafana',
                expr='example',
            ),
        ],
        gridPos=GridPos(h=4, w=4, x=17, y=0),
    ),
    TimeSeries(
        title="Prometheus http requests",
        dataSource='prometheus',
        targets=[
            Target(
                expr='rate(prometheus_http_requests_total[5m])',
                legendFormat="{{ handler }}",
                refId='A',
            ),
        ],
        unit=OPS_FORMAT,
        gridPos=GridPos(h=8, w=16, x=0, y=10),
    )
], 'Top View': [
    TimeSeries(
        title="Power (kW)",
        dataSource='default',
        targets=[
            SqlTarget(Target(datasource='stevedb'),
                      rawSql="""
                            WITH charger_data AS (SELECT TIMESTAMP(value_timestamp) AS 'time', CAST(value AS DOUBLE) AS 'Power'
                                          FROM connector_meter_value
                                            WHERE $__timeFilter(value_timestamp)
                                            AND reading_context = 'Sample.Periodic'
                                            AND measurand = 'Power.Active.Import')
                                            
                            SELECT time, sum(Power) AS 'Power (kW)'
                            FROM charger_data group by time;
                        """)
        ],
        drawStyle='bars',
        fillOpacity=100,
        gridPos=GridPos(h=8, w=24, x=0, y=24),
    )]}

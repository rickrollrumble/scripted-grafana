from grafanalib.core import TimeSeries, OPS_FORMAT, GridPos, Target, GaugePanel, SqlTarget

from queries import TOTAL_POWER_QUERY

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
                      rawSql=TOTAL_POWER_QUERY)
        ],
        drawStyle='bars',
        fillOpacity=100,
        gridPos=GridPos(h=8, w=24, x=0, y=24),
    )]}

from jinja2 import Template


def create_postgres_insert_sql(render_parameters):
    sql = """
    WITH processed_raw_{{channel}}_{{table_name}} AS (
        SELECT
            {%- for processed_column, column_alias in processed_columns.items() %}
            {{processed_column}} AS {{column_alias}}
            {%- if not loop.last -%}
                ,
            {%- endif -%}
            {%- endfor %}
        FROM raw.raw_{{channel}}_{{table_name}}
    )
    INSERT INTO
    {{channel}}.{{table_name}} (
        {%- for column in processed_columns.values() %}
        {{column}}
        {%- if not loop.last -%}
            ,
        {%- endif -%}
        {%- endfor %}
    )
    SELECT
    DISTINCT ON ({% for i in dimensions %}{{i}}{%- if not loop.last -%},{%- endif -%}{% endfor %}) * FROM processed_raw_{{channel}}_{{table_name}}
    ON CONFLICT ({% for i in dimensions %}{{i}}{%- if not loop.last -%},{%- endif -%}{% endfor %}) DO UPDATE SET
        {%- for metric in metrics %}
        {{metric}} = excluded.{{metric}}
        {%- if not loop.last -%}
            ,
        {%- endif -%}
        {%- endfor %}
    ;
    """
    return Template(sql).render(render_parameters)


render_parameters = {
    'channel': 'analytics',
    'table_name': 'device_report',
    'processed_columns': {
        'data_source': 'data_source',
        'TO_DATE("ga:date", \'YYYY-MM-DD\')': '"ga:date"',
        '"ga:accountId"': '"ga:accountId"',
        '"ga:country"': '"ga:country"',
        '"ga:region"': '"ga:region"',
        '"ga:metro"': '"ga:metro"',
        '"ga:sourceMedium"': '"ga:sourceMedium"',
        '"ga:source"': '"ga:source"',
        '"ga:medium"': '"ga:medium"',
        '"ga:campaign"': '"ga:campaign"',
        '"ga:deviceCategory"': '"ga:deviceCategory"',
        '"ga:users"::numeric': '"ga:users"',
        '"ga:newUsers"::numeric': '"ga:newUsers"',
        '"ga:pageviews"::numeric': '"ga:pageviews"',
        '"ga:sessions"::numeric': '"ga:sessions"',
        '"ga:sessionDuration"::numeric': '"ga:sessionDuration"',
        '"ga:bounces"::numeric': '"ga:bounces"'
    },
    'dimensions': [
        'data_source',
        '"ga:date"',
        '"ga:accountId"',
        '"ga:country"',
        '"ga:region"',
        '"ga:metro"',
        '"ga:sourceMedium"',
        '"ga:source"',
        '"ga:medium"',
        '"ga:campaign"',
        '"ga:deviceCategory"'
    ],
    'metrics': [
        '"ga:users"',
        '"ga:newUsers"',
        '"ga:pageviews"',
        '"ga:sessions"',
        '"ga:sessionDuration"',
        '"ga:bounces"'
    ]
}

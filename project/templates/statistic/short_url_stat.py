{% extends "_base.html" %}

{% block title %}Statistic | ShortUrl{% endblock title %}

{% block content %}

{{ clicks_by_date_chart|safe }}
{{ country_chart|safe }}

{% endblock content%}
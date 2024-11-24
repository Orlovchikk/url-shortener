from django.shortcuts import get_object_or_404, render
import plotly.express as px
from statistic.models import ClickData
from shortener.models import ShortUrl
from django.db.models.functions import TruncDate
from django.db.models import Count
import pycountry


def short_url_stat(request, pk):

    config = {
        "modeBarButtonsToRemove": [
            "zoom2d",
            "pan2d",
            "select2d",
            "lasso2d",
            "zoomIn2d",
            "zoomOut2d",
            "autoScale2d",
            "resetScale2d",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "toggleSpikelines",
            "toImage",
            "hoverClosestPie",
            "toggleHover",
            "resetViews",
            "sendDataToCloud",
            "editInChartStudio",
            "resetViewAxes",
            "drawline",
            "drawopenpath",
            "drawclosedpath",
            "drawcircle",
            "drawrect",
            "eraseshape",
        ],
        "displaylogo": False,
    }

    short_url = get_object_or_404(ShortUrl, short_url=pk)

    #   Переходы по дням
    clicks_by_date = (
        ClickData.objects.filter(short_url=short_url)
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    x_dates = [item["date"] for item in clicks_by_date]
    y_counts = [item["count"] for item in clicks_by_date]

    fig = px.bar(
        x=x_dates,
        y=y_counts,
        title="Количество переходов по дням",
        labels={"y": "Переходы", "x": "Дата"},
        color_discrete_sequence=["#007bff"],
        template="plotly_white",
    )

    fig.update_xaxes(
        tickformat="%Y-%m-%d",
        type="date",
        dtick="D1",
        showgrid=True,
        gridwidth=0.5,
        gridcolor="lightgray",
    )

    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="lightgray")

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    clicks_by_date_chart = fig.to_html(config=config, full_html=False)

    #   Отображение карты мира для стран
    country_clicks = (
        ClickData.objects.filter(short_url=short_url)
        .values("country")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # data = []
    # for item in country_clicks:
    #     try:
    #         country = pycountry.countries.get(alpha_2=item["country"])
    #         if hasattr(country, "alpha_3"):
    #             data.append({"country": country.alpha_3, "count": item["count"]})

    #     except (KeyError, AttributeError) as e:
    #         print(f"Error converting country code: {e}")
    #         pass

    fig = px.choropleth(
        country_clicks,
        locations="country",
        color="count",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="equirectangular",
        title="География переходов",
        locationmode="country names",
    )

    country_chart = fig.to_html(config=config, full_html=False)

    context = {
        "clicks_by_date_chart": clicks_by_date_chart,
        "country_chart": country_chart,
    }
    return render(request, "statistic/short_url_stat.py", context)

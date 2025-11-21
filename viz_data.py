import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
from streamlit_plotly_events import plotly_events

df = pd.read_csv("Analysis.csv")
df[["Price Score", "Service Score",
    "Music Score", "Ambience Score",
    "Delivery Score", "Reservation Score"]] = df[["Price Sentiment Score", "Service Sentiment Score",
    "Music Sentiment Score", "Ambience Sentiment Score",
    "Delivery Sentiment Score", "Reservation Sentiment Score"]].round(2)

df_grouped = df.groupby("name").agg({"Price Score": "mean",
                                      "Service Score":"mean",
                                      "Music Score": "mean",
                                      "Ambience Score": "mean",
                                      "Delivery Score": "mean",
                                      "Reservation Score": "mean",
                                      "latitude":"first",
                                      "longitude":"first"}).reset_index()
logo_url = "download.jpg"
st.logo(logo_url, size="large")
with st.sidebar:
    option = st.selectbox("Select Restaurant", df_grouped["name"])
    row = df_grouped[df_grouped["name"] == option]
    stars = df[df["name"] == option]
    stars = stars["stars_x"]
    st.subheader(option)
    st.write("Star Rating")
    st.write(stars.iloc[0],":star:")

with st.container(width = 500, height=500):
    fig = go.Figure(data=[go.Bar(
                x=["Price", "Service", "Music", "Ambience", "Delivery", "Reservation"], 
                y=row.iloc[0,1:])])

    # Update layout
    fig.update_layout(title="Sentiment scores", xaxis_title="Aspects", yaxis_title="Score",
                    barmode = "relative")
    fig.update_yaxes(range=[-1,1])
    st.plotly_chart(fig, width = "content")

with st.container(width="stretch"):
    st.markdown("**User Credibility Scores**")
    data = df[df["name"] == option]
    data = data[["user_id", "credibility_score","stars_y", 
                 "Price Score", "Service Score", 
                 "Music Score", "Ambience Score", 
                 "Delivery Score", "Reservation Score"]]
    data = data.sort_values("credibility_score", ascending = False)
    st.table(data)

# fig = px.scatter_mapbox(
#     df_grouped,
#     lat=df_grouped["latitude"],
#     lon=df_grouped["longitude"],
#     hover_name="name",
#     zoom=10,
#     height=500
# )

# fig.update_layout(
#     mapbox_style="open-street-map",
#     clickmode="event+select"
# )

# st.plotly_chart(fig, width="stretch", key="map")
# clicked = plotly_events(fig, click_event=True, hover_event=False, select_event=False)
# print(clicked)
# if clicked and "clickData" in clicked and clicked["clickData"]:
#     point = clicked["clickData"]["points"][0]
#     point_name = point["hovertext"]

#     selected = df_grouped[df_grouped["name"] == point_name].iloc[0]

#     st.subheader("Selected Point Details")
#     st.write({
#         "Name": selected["name"],
#         "Score": selected["Price Sentiment Score"],
#     })
# else:
#     st.info("Click a point on the map to view details.")

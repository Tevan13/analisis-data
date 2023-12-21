import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Set style seaborn
# sns.set(style='dark')

px.defaults.template = 'plotly_dark'
px.defaults.color_continuous_scale = 'reds'

# Menyiapkan data day_df
day_df = pd.read_csv("bike-sharing.csv")
day_df.head()

# Menyiapkan daily_rent_df
def daily_rent_df(df):
    daily_rent = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent

# Menyiapkan daily_casual_rent_df
def daily_casual_df(df):
    daily_casual= df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual

# Menyiapkan daily_registered_rent_df
def daily_registered_df(df):
    daily_registered = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered
    
# Dataframe sewa per jam
def hour_rent_df(df):
    hour_rent= df.groupby(by='hour').agg({
        'count': 'sum'
    }).reset_index()
    return hour_rent

# Dataframe sewa per hari
def weekday_rent_df(df):
    weekday_rent= df.groupby(by='weekday').agg({
        'count': 'sum'
    })
    ordered_days= [
        'Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri',
        'Sat'
    ]
    weekday_rent = weekday_rent.reindex(ordered_days, fill_value=0)
    return weekday_rent

# Dataframe sewa per bulan
def monthly_rent_df(df):
    monthly_rent = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent = monthly_rent.reindex(ordered_months, fill_value=0)
    return monthly_rent

# Dataframe sewa per tahun
def year_rent_df(df):
    year_rent = df.groupby(by='year').agg({
        'count': 'sum'
    }).reset_index()
    return year_rent

# Fungsi untuk membuat DataFrame workingday_rent
def workingday_rent_df(df):
    workingday_rent = df.groupby(by=["month", "workingday"]).agg({
        'count': 'sum'
    }).reset_index()

    # Urutkan bulan sesuai dengan urutan yang ditentukan
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    workingday_rent['month'] = pd.Categorical(workingday_rent['month'], categories=ordered_months, ordered=True)
    workingday_rent = workingday_rent.sort_values('month')

    return workingday_rent

# Menyiapkan holiday_rent_df
def holiday_rent_df(df):
    holiday_rent = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent

# Menyiapkan weather_rent_df
def weather_rent_df(df):
    weather_rent = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent

# Menyiapkan season_rent_df
def season_rent_df(df):
    season_rent_df = df.groupby(by='season').agg({
    'count': ['sum']
    })
    return season_rent_df

#Dataframe real_temp, fl_temp & hum
def season_temp_hum_df(df):
    season_temp_hum_df = df.groupby(by='season').agg({
    'real_temp': ['max', 'min', 'mean','sum'],
    'fl_temp': ['max', 'min', 'mean','sum'],
    'hum': ['max', 'min', 'mean','sum']
    })
    return season_temp_hum_df

# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()
 
with st.sidebar:
    # st.image('')
    # Menambahkan selectbox untuk Tipe User
    user_type = st.selectbox('Pilih Tipe User', ['Casual', 'Registered', 'Total'])

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent = daily_rent_df(main_df)
daily_casual = daily_casual_df(main_df)
daily_registered = daily_registered_df(main_df)
hour_rent = hour_rent_df(main_df)
weekday_rent = weekday_rent_df(main_df)
monthly_rent = monthly_rent_df(main_df)
year_rent = year_rent_df(main_df)
workingday_rent = workingday_rent_df(main_df)
holiday_rent = holiday_rent_df(main_df)
weather_rent = weather_rent_df(main_df)
season_rent = season_rent_df(main_df)

# Membuat Dashboard secara lengkap
st.title('🚲 Dashboard Bike Sharing 🚲')

# Membuat jumlah penyewaan harian
st.subheader(f' :bulb: Rentals Information ({user_type} User)')

# Memilih dataframe yang sesuai berdasarkan Tipe User
if user_type == 'Casual':
    user_df = daily_casual
elif user_type == 'Registered':
    user_df = daily_registered
else:
    # Menambahkan total jumlah penyewaan harian
    user_df = daily_casual.copy()
    user_df['total'] = daily_casual['casual'] + daily_registered['registered']

# Menampilkan jumlah penyewaan harian berdasarkan Tipe User
col1, col2, col3 = st.columns(3)

with col1:
    rent_user = user_df[user_type.lower()].sum()
    st.metric(f'{user_type} User', value=rent_user)

# # Membuat jumlah penyewaan harian
# st.subheader('Daily Rentals')
# col1, col2, col3 = st.columns(3)

# with col1:
#     rent_casual = daily_casual['casual'].sum()
#     st.metric('Casual User', value= rent_casual)

# with col2:
#     registered_rent= daily_registered['registered'].sum()
#     st.metric('Registered User', value= registered_rent)
 
# with col3:
#     rent_daily = daily_rent['count'].sum()
#     st.metric('Total User', value= rent_daily)

# Membuat jumlah penyewaan per jam
st.subheader(':sunglasses: Hourly Rentals')
fig_hour, ax_hour = plt.subplots(figsize=(24, 8))
ax_hour.plot(
    hour_rent.index,
    hour_rent['count'],
    marker='o', 
    linewidth=2,
    color='tab:orange'
)

for index, row in enumerate(hour_rent['count']):
    ax_hour.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax_hour.tick_params(axis='x', labelsize=15, rotation=45)
ax_hour.tick_params(axis='y', labelsize=15)
st.pyplot(fig_hour)

# Membuat jumlah penyewaan per hari
st.subheader(':sunglasses: Daily Rentals')
fig_weekday, ax_weekday = plt.subplots(figsize=(24, 8))
ax_weekday.plot(
    weekday_rent.index,
    weekday_rent['count'],
    marker='o', 
    linewidth=2,
    color='tab:green'
)

for index, row in enumerate(weekday_rent['count']):
    ax_weekday.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax_weekday.tick_params(axis='x', labelsize=25, rotation=45)
ax_weekday.tick_params(axis='y', labelsize=20)
st.pyplot(fig_weekday)

# Membuat jumlah penyewaan bulanan
st.subheader(':sunglasses: Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent.index,
    monthly_rent['count'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Hubungan antara temperature & Humidity
st.subheader(':bulb: Relationships Temp & Hum')

# Membuat DataFrame untuk scatterplot
scatter_df = season_temp_hum_df(main_df).stack(level=0).reset_index()
scatter_df.columns = ['season', 'variable', 'max', 'min', 'mean', 'sum']

# Menambahkan checkbox untuk memilih sumbu x
selected_variable = st.selectbox('Pilih Variable', ['real_temp', 'fl_temp', 'hum'])

# Memfilter data berdasarkan variable yang dipilih
scatter_data = scatter_df[scatter_df['variable'] == selected_variable]

# Membuat scatterplot
fig_scatter = px.scatter(
    scatter_data,
    x='season',
    y='mean',
    size='max',
    color='min',
    labels={'mean': f'Mean {selected_variable}', 'max': f'Max {selected_variable}', 'min': f'Min {selected_variable}'},
    title=f'Relationships between {selected_variable} with users',
    hover_name='season'
)
st.plotly_chart(fig_scatter)

# Barplot untuk workingday berdasarkan bulan
st.subheader(':bulb: Rentals based on working day')
# Barplot untuk workingday berdasarkan bulan
fig_bar = px.bar(
    workingday_rent,
    x='month',
    y='count',
    color='workingday',
    labels={'count': 'Total Count'},
    title='Workingday Count by Month',
    color_discrete_map={0: 'red', 1: 'green'},
    text='count',
    category_orders={'workingday': [0, 1]}
)

# Mengganti label pada legend
fig_bar.for_each_trace(lambda t: t.update(name='Not Working Day') if t.name == '0' else t.update(name='Working Day'))
st.plotly_chart(fig_bar)


st.caption('Copyright (c) Stevanus Ertito 2023')
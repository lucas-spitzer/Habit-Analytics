import pandas as pd

YES_OR_NO_LIST = ['Eat Properly (T/F)', 'Do Not Feed Addictions (T/F)', 'Cold Shower (T/F)']
EXERCISE_LIST = ['Date', "Swimming (min)", "Biking (min)", "Running (min)", "Lifting (min)"]
EDUCATION_LIST = ['Date', 'Schoolwork (min)', 'Developing Technical Skills (min)', 'Read & Write (min)', 'Podcasts & Audiobooks (min)']


def sub_dataframe(df_name, column_list):
  """ Create or overwrite a dataframe and csv file based on the df_name. The parameter column_list is used to directly transfer over specified the column's data into the csv. """

  master_df = pd.read_csv('Master.csv')
  
  if df_name == "YesOrNo.csv":
    sub_df = master_df.loc[:, column_list]
    sub_df.columns = [col[:-6] for col in sub_df.columns]
    sub_df.rename(columns={"Do Not Feed Addictions": "Avoid Distractions"}, inplace=True)
    df_melted = sub_df.melt(var_name='Type', value_name='Value')
    df_melted.to_csv("DesktopApp/Habit-Data/" + df_name, index=False)
    df_melted.to_csv("MobileApp/Habit-Data/" + df_name, index=False)
  else:
    new_df = master_df[column_list].copy()
    new_df.columns = [col[:-6] if col != 'Date' else col for col in new_df.columns]
    if df_name == "Education.csv":
      new_df.to_csv("DesktopApp/Habit-Data/" + df_name, index=False)
      new_df.rename(columns={"Developing Technical Skills": "Dev. Tech Skills"}, inplace=True)
      new_df.rename(columns={"Podcasts & Audiobooks": "Pods & Audio"}, inplace=True)
      new_df.to_csv("MobileApp/Habit-Data/" + df_name, index=False)
    else:
      new_df.to_csv("DesktopApp/Habit-Data/" + df_name, index=False)
      new_df.to_csv("MobileApp/Habit-Data/" + df_name, index=False)


def data_cleaning(filename):
  """ Enter the filename with data you wish to add to the master csv and dataframe. The data file goes through a cleaning and manipulation phase that will properly add observation(s). """

  master_df = pd.read_csv("Master.csv")
  df = pd.read_csv("RawData/" + filename)
  yes_or_no_list = ['Eat Properly (T/F)', 'Do Not Feed Addictions (T/F)', 'Cold Shower (T/F)']

  for row in df.itertuples():
    if row.Date in master_df['Date'].tolist():
      if row.Habit in yes_or_no_list:
        if row.Value == 1:
          master_df.loc[master_df['Date'] == row.Date, row.Habit] = 'yes'
        elif row.Value == 0:
          master_df.loc[master_df['Date'] == row.Date, row.Habit] = 'no'
      else:
        master_df.loc[master_df['Date'] == row.Date, row.Habit] = row.Value
    else:
      new_observation = pd.DataFrame({'Date': [row.Date],
        'Schoolwork (min)': [0],
        'Lifting (min)': [0],
        'Running (min)': [0],
        'Developing Technical Skills (min)': [0],
        'Read & Write (min)': [0],
        'Eat Properly (T/F)': ['no'],
        'Do Not Feed Addictions (T/F)': ['no'],
        'Cold Shower (T/F)': ['no'],
        'Swimming (min)': [0],
        'Biking (min)': [0],
        'Podcasts & Audiobooks (min)': [0]
      })
      master_df = pd.concat([master_df, new_observation], ignore_index=True)
      master_df.loc[master_df['Date'] == row.Date, row.Habit] = row.Value
  master_df = master_df.sort_values('Date')
  master_df.to_csv('Master.csv', index=False)

  # Overwrites existing sub-dataframes/files after updating Master dataframe/file.
  sub_dataframe("Education.csv", EDUCATION_LIST)
  sub_dataframe("Exercise.csv", EXERCISE_LIST)
  sub_dataframe("YesOrNo.csv", YES_OR_NO_LIST)


def summary_statistics():
  """ Calculate summary statistics to be displayed on the Desktop App. """

  master_df = pd.read_csv('Master.csv')

  num_rows = len(master_df.iloc[1:])

  education_per_day = (master_df['Schoolwork (min)'].sum() + master_df['Read & Write (min)'].sum() + master_df['Developing Technical Skills (min)'].sum() + master_df['Podcasts & Audiobooks (min)'].sum()) / 30
  excercise_per_day = (master_df['Running (min)'].sum() + master_df['Lifting (min)'].sum() + master_df['Biking (min)'].sum() + master_df['Swimming (min)'].sum()) / 30

  ep_completion_rate = master_df['Eat Properly (T/F)'].value_counts()['yes'] / 30
  ad_completion_rate = master_df['Do Not Feed Addictions (T/F)'].value_counts()['yes'] / 30
  cs_completion_rate = master_df['Cold Shower (T/F)'].value_counts()['yes'] / 30

  with open('DesktopApp/Habit-Data/SeptemberSummaryStatistics.txt', 'w') as f:
    f.write(str(education_per_day) + '\n' + str(excercise_per_day) + '\n')
    f.write(str(ep_completion_rate) + '\n' + str(ad_completion_rate) + '\n' + str(cs_completion_rate) + '\n')
  

def comparison_analysis():
  """ Compare key metrics described in the hypotheses.  
  *Important Note* All September numbers were dervied from master.csv when master.csv only contained September Data."""

  august_exercise_df = pd.read_csv('RawData/AugustExercise.csv')
  august_ep_df = pd.read_csv('RawData/AugustEP.csv')
  master_df = pd.read_csv('Master.csv')

  august_num_rows = len(august_exercise_df) 
  september_num_rows = len(master_df.iloc[0:]) 

  september_excercise_total = master_df['Running (min)'].sum() + master_df['Lifting (min)'].sum() + master_df['Biking (min)'].sum() + master_df['Swimming (min)'].sum()
  august_exercise_total = august_exercise_df['Value'].sum()

  september_daily_avg = september_excercise_total / 30
  august_daily_avg = august_exercise_total / 31

  sept_ep_comp_rate = (master_df['Eat Properly (T/F)'].value_counts()['yes'] / 30) * 100
  aug_ep_comp_rate = (august_ep_df['Value'].sum() / 31) * 100

  # Percent Increase Formula: (New Value - Old Value) / Old Value * 100%
  exercise_percent_increase = ((september_daily_avg - august_daily_avg) / august_daily_avg) * 100

  # Difference in Percentages Shows Increase
  ep_rate_increase = sept_ep_comp_rate - aug_ep_comp_rate

  print('September Exercise Total: ', september_excercise_total, '\nAugust Exercise Total: ', int(august_exercise_total))
  print('September Daily Average: ', round(september_daily_avg, 2), '\nAugust Daily Average: ', round(august_daily_avg, 2))
  print('Exercise Percent Increase: ', round(exercise_percent_increase, 2), '%')
  print('September Eat Properly Times Completed: ', master_df['Eat Properly (T/F)'].value_counts()['yes'], '\nAugust Eat Properly Times Completed: ', int(august_ep_df['Value'].sum()))
  print('September Completion Rate: ', round(sept_ep_comp_rate, 2), '%', '\nAugust Completion Rate: ', round(aug_ep_comp_rate, 2), '%')
  print('Eat Properly Completion Rate Increase: ', round(ep_rate_increase, 2), '%')


def clean_historic():
  """ Cleaning historic data and saving results in RawData folder to be utilized later. """

  historic_df = pd.read_csv('RawData/HistoricData.csv')

  historic_df['Date'] = pd.to_datetime(historic_df['Date'])

  august_df = historic_df[historic_df['Date'].dt.month == 8]

  august_ep_df = august_df[august_df['Habit'] == 'Eat Properly']
  august_ep_df = august_ep_df.drop(august_ep_df.tail(19).index)  # Removing duplicate observations
  august_ep_df.to_csv("RawData/AugustEP.csv", index=False)

  august_exercise_df = august_df[august_df['Habit'] == 'Exercise']
  august_exercise_df = august_exercise_df.drop(august_exercise_df.tail(30).index)  # Removing duplicate observations
  august_exercise_df.to_csv("RawData/AugustExercise.csv", index=False)


comparison_analysis()
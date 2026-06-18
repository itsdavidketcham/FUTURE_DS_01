import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

#using the method we used to search for a file in task 2 
search_pattern = os.path.join("C:\\Users\\david\\Downloads", "**", "bank*.csv")
found_files = glob.glob(search_pattern, recursive=True)

if not found_files:
    print("Error: Could not find any bank CSV files in Downloads.")
else:
    full_dataset = [f for f in found_files if 'bank-full' in f]
    file_path = full_dataset[0] if full_dataset else found_files[0]
    #read the data 
    df = pd.read_csv(file_path, sep=';')
    print(f"Successfully loaded data from: {os.path.basename(file_path)}")
    total_customers = len(df)
    subscribed_count = (df['y'] == 'yes').sum()
    conversion_rate = (subscribed_count / total_customers) * 100

    print("baseline marketing analysis")
    print("Total Customers Contacted:", total_customers)
    print("Total Successful Subscriptions:", subscribed_count)
    print(f"Overall Conversion Rate: {conversion_rate:.2f}%")

    #conversion Rate by Job Type

    print("subscription conversion rate by job type")
    job_analysis = df.groupby('job')['y'].value_counts(normalize=True).unstack() * 100
    job_analysis = job_analysis.sort_values(by='yes', ascending=False)
    print(job_analysis[['yes']].rename(columns={'yes': 'Conversion_Rate_%'}))

    print("impact of housing loan on subscription")
    housing_analysis = df.groupby('housing')['y'].value_counts(normalize=True).unstack() * 100
    print(housing_analysis[['yes']].rename(columns={'yes': 'Conversion_Rate_%'}))

   
    print("generating marketing chart")
    plt.figure(figsize=(10, 5))
    sns.set_theme(style="whitegrid")

    #Reset index to make plotting easy
    plot_data = job_analysis.reset_index()

    #Creating a student barplot
    ax = sns.barplot(x='job', y='yes', data=plot_data, color='lightgreen')

    #formatting labels and title cleanly
    plt.title('Bank Term Deposit Subscription Rate by Job Type')
    plt.xlabel('Job Category')
    plt.ylabel('Subscription Conversion Rate (%)')
    plt.xticks(rotation=45)
    plt.ylim(0, job_analysis['yes'].max() + 5)

    #Add data labels on top of bars
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height() + 0.5), 
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()

    #save the plot image
    plt.savefig('bank_conversion_by_job.png')
    print("Chart successfully saved as bank_conversion_by_job.png")
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num
import csv
import datetime


# Function to read data from the CSV file
def read_timeline_data(filename):
    events = []
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            start_date = datetime.datetime.strptime(row['StartDate'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(row['EndDate'], '%Y-%m-%d')
            events.append({
                'EventName': row['EventName'],
                'StartDate': start_date,
                'EndDate': end_date,
                'Position': int(row['Position'])
            })
    return events


# Define a function to plot events
def plot_event(event, events_on_same_line):
    start_date = date2num(event['StartDate'])
    end_date = date2num(event['EndDate'])
    position = event['Position']

    # Calculate the vertical position for the event
    y_position = position + events_on_same_line * 0.2  # Adjust the spacing factor

    ax.plot([start_date, end_date], [y_position, y_position], marker='o', markersize=8, label=event['EventName'])
    ax.annotate(event['EventName'], xy=(start_date, y_position), xytext=(0, 10),
                textcoords='offset points', ha='center', va='bottom')

def plot_timeline_data(timeline_data):
    # Sort events by start date
    timeline_data.sort(key=lambda x: x['StartDate'])

    # Define a list of year-start dates based on your existing code
    min_year = timeline_data[0]["StartDate"].year
    max_year = max(row["EndDate"].year for row in timeline_data) + 1
    year_range = range(min_year, max_year)
    year_start_dates = [date2num(datetime.datetime(year, 1, 1)) for year in year_range]
    for year in year_range:
        ax.axvline(date2num(datetime.datetime(year, 1, 1)), color='y', linestyle=':', label=f'Year {year}')


    ax.xaxis.set_major_locator(plt.FixedLocator(year_start_dates))
    # Define a custom date format to display just the year
    year_format = DateFormatter('%Y')
    ax.xaxis.set_major_formatter(year_format)

    # Draw a horizontal line down the center
    center_position = 0  # Adjust the position as needed
    ax.axhline(center_position, color='k', linestyle='--', label='Center Line')

    # Adjust the figure size and labels
    plt.gcf().autofmt_xdate()
    plt.xlabel('Timeline')
    plt.title('Interactive Timeline Visualization')
    plt.grid(visible=False)

    # Iterate over the list of events to plot them
    for i, event in enumerate(timeline_data):
        events_on_same_line = 0

        # Check for overlapping events
        for j, other_event in enumerate(timeline_data):
            if j > i:
                if event['StartDate'] <= other_event['EndDate'] and event['EndDate'] >= other_event['StartDate']:
                    events_on_same_line += 1

        plot_event(event, events_on_same_line)

    # Save the visualization as an image (optional)
    plt.savefig('timeline.png')

    # Display the visualization
    plt.show()

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Read the CSV file into a list of events
    timeline_data = read_timeline_data('timeline_data.csv')

    plot_timeline_data(timeline_data)



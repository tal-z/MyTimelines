import csv
import datetime

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num

from format_utils import *


matplotlib.use('TkAgg')


def read_timeline_data(filename):
    events = []
    colors = [
        "#FF6B6B",  # Coral
        "#1E90FF",  # Dodger Blue
        "#FF69B4",  # Hot Pink
        "#48D1CC",  # Medium Turquoise
        "#aa0098",  # Purple
        "#00BFFF",  # Deep Sky Blue
        "#00A500",  # Green
        "#FFA07A",  # Light Salmon
    ]

    colors_count = len(colors)
    categories = {}
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            start_date = datetime.datetime.strptime(row['StartDate'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(row['EndDate'], '%Y-%m-%d')
            category = row["Category"]
            valence = int(row['Valence'])
            force_annotation = bool(row["ForceAnnotation"])
            if category in categories:
                color, index = categories[category]
            else:
                color = colors.pop()
                index = colors_count - len(colors)
                categories[category] = color, index

            events.append({
                'EventName': row['EventName'],
                'StartDate': start_date,
                'EndDate': end_date,
                'Position': index * valence,
                'Color': color,
                'Category': category,
                'ForceAnnotation': force_annotation,
            })

    positive_positions = {e["Position"] for e in events if e["Position"] > 0}
    positive_positions = {p: idx+1 for idx, p in enumerate(positive_positions)}

    negative_positions = {e["Position"] for e in events if e["Position"] < 0}
    negative_positions = {p: -(idx+1) for idx, p in enumerate(negative_positions)}

    for event in events:
        if event["Position"] > 0:
            event["Position"] = positive_positions[event["Position"]]
        elif event["Position"] < 0:
            event["Position"] = negative_positions[event["Position"]]

    for category in categories:
        events_in_category = [e for e in events if e['Category'] == category]
        for idx, event in enumerate(events_in_category):
            event["Color"] = darken_color(
                event["Color"],
                idx/3 * (1 / len(events_in_category))
            )



    y_lim = -(len(negative_positions)+1), len(positive_positions)+1
    return events, y_lim


def plot_event(event):
    start_date = date2num(event['StartDate'])
    end_date = date2num(event['EndDate'])
    y_position = event['Position']

    # Calculate the vertical position for the event
    width = end_date - start_date
    center_x = start_date + width / 2  # Calculate the center of the line

    # Split the annotation text into multiple lines on whitespace
    event_name = event['EventName']
    color = event['Color']
    lines = split_text_into_lines(event_name)

    ax.plot([start_date, end_date], [y_position, y_position], marker='d', markersize=6, color=color)

    annotation_y = -20 if event["ForceAnnotation"] else 20

    ax.annotate(
        '\n'.join(lines),
        xy=(center_x, y_position),
        xytext=(0, annotation_y),
        textcoords='offset points',
        ha='center',
        va='center',
        bbox=dict(
            boxstyle='round,pad=0.5',
            facecolor='white',
            edgecolor='gray',
            alpha=0.7
        ),
        arrowprops=dict(
            arrowstyle='-',
            connectionstyle='arc3,rad=0.3',
            color='black'
        )
    )


def setup_plot(y_lim):
    plt.rcParams['font.family'] = 'Arial'

    # Define a list of year-start dates based on your existing code
    min_year = timeline_data[0]["StartDate"].year
    max_year = max(row["EndDate"].year for row in timeline_data) + 1
    year_range = range(min_year, max_year)
    # Draw vertical lines representing the start of years
    for year in year_range:
        ax.axvline(date2num(datetime.datetime(year, 1, 1)), color='gray', linestyle=':', label=f'Year {year}')

    # Set the y-limits based on your data
    plt.ylim(*y_lim)

    # Shade the background above zero in green and below in red
    ax.fill_between(
        [date2num(datetime.datetime(min_year, 1, 1)), date2num(datetime.datetime(max_year, 1, 1))],
        0,
        y_lim[0],
        color='tomato',
        alpha=0.15
    )
    ax.fill_between(
        [date2num(datetime.datetime(min_year, 1, 1)), date2num(datetime.datetime(max_year, 1, 1))],
        0,
        y_lim[1],
        color='seagreen',
        alpha=0.15
    )

    # Define a list of year-start dates based on your existing code
    min_year = timeline_data[0]["StartDate"].year
    max_year = max(row["EndDate"].year for row in timeline_data) + 1
    year_range = range(min_year, max_year)
    year_start_dates = [date2num(datetime.datetime(year, 1, 1)) for year in year_range]

    # Draw a horizontal line down the center
    center_position = 0  # Adjust the position as needed
    ax.axhline(center_position, color='k', linestyle='--', label='Center Line')

    # Adjust the figure size, labels, and margins
    plt.gcf().autofmt_xdate()
    plt.xlabel('Years of My Life')
    plt.ylabel('Sentiment')
    plt.title("My Life Timeline", fontsize=16)
    plt.grid(visible=False)
    plt.margins(x=0, y=0)
    # Set x-axis ticks with year labels
    ax.xaxis.set_major_locator(plt.FixedLocator(year_start_dates))
    year_format = DateFormatter('%Y')
    ax.xaxis.set_major_formatter(year_format)
    # Set y-axis ticks
    y_ticks = [y_lim[0]/2, 0, y_lim[1]/2]
    y_tick_labels = ['Negative', 'Neutral', 'Positive']
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tick_labels)


def plot_timeline_data(timeline_data):
    # Sort events by start date and their position
    timeline_data.sort(key=lambda x: (abs(x['Position']), x['StartDate'], x['EndDate']))

    # Create a dictionary to keep track of the current vertical position of each line
    line_positions = {}

    # Iterate over the list of events to plot them
    for i, event in enumerate(timeline_data):
        start_date = event['StartDate']
        end_date = event['EndDate']
        y_position = event['Position']

        # Check for overlaps and adjust the y_position
        if y_position in line_positions:
            # The vertical position is already occupied; find a new one
            if y_position != 0:
                while y_position in line_positions:
                    y_position += .1
            event['Position'] = y_position

        # Update the line_positions dictionary
        line_positions[y_position] = end_date

        # Plot the event with the adjusted y_position
        plot_event(event)

    # Save the visualization as an image (optional)
    # plt.tight_layout()
    plt.savefig('timeline.png')
    # Display the visualization
    plt.show()


# Create a Matplotlib figure and axis
fig, ax = plt.subplots()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Read the CSV file into a list of events
    timeline_data, y_limit = read_timeline_data('real_timeline_data.csv')
    setup_plot(y_limit)
    plot_timeline_data(timeline_data)

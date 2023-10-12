import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num
import matplotlib.colors as mcolors
import csv
import datetime


def read_timeline_data(filename):
    events = []
    colors = list(mcolors.TABLEAU_COLORS.values())
    colors_count = len(colors)
    categories = {}
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            start_date = datetime.datetime.strptime(row['StartDate'], '%Y-%m-%d')
            end_date = datetime.datetime.strptime(row['EndDate'], '%Y-%m-%d')
            category = row["Category"]
            valence = int(row['Valence'])
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

    return events


def split_text_into_lines(text, max_line_length=25):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_line_length:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def plot_event(event, events_on_same_line, is_up):
    start_date = date2num(event['StartDate'])
    end_date = date2num(event['EndDate'])
    position = event['Position']

    # Calculate the vertical position for the event
    y_position = position + events_on_same_line * 0  # Adjust the spacing factor
    width = end_date - start_date
    center_x = start_date + width / 2  # Calculate the center of the line

    # Split the annotation text into multiple lines on whitespace
    event_name = event['EventName']
    color = event['Color']
    lines = split_text_into_lines(event_name)

    ax.plot([start_date, end_date], [y_position, y_position], marker='X', markersize=10, color=color)

    # Place the annotation at the center of the line with multiple lines
    if is_up:
        annotation_y = 15
    else:
        annotation_y = -20

    ax.annotate(
        '\n'.join(lines),
        xy=(center_x, y_position),
        xytext=(0, annotation_y),
        textcoords='offset points',
        ha='center',
        va='center',
        bbox=dict(
            boxstyle='round',
            facecolor='w',
            edgecolor='black',
        ),
        arrowprops=dict(
            arrowstyle='->',
            connectionstyle='arc3,rad=0.5',
            color='black')
    )


def setup_plot():
    # Define a list of year-start dates based on your existing code
    min_year = timeline_data[0]["StartDate"].year
    max_year = max(row["EndDate"].year for row in timeline_data) + 1
    year_range = range(min_year, max_year)
    year_start_dates = [date2num(datetime.datetime(year, 1, 1)) for year in year_range]
    # Draw vertical lines representing the start of years
    for year in year_range:
        ax.axvline(date2num(datetime.datetime(year, 1, 1)), color='y', linestyle=':', label=f'Year {year}')

    # Add x ticks with year labels
    ax.xaxis.set_major_locator(plt.FixedLocator(year_start_dates))
    year_format = DateFormatter('%Y')
    ax.xaxis.set_major_formatter(year_format)
    # Hide the y-axis ticks
    y_ticks = [-2, 0, 2.5]  # Adjust the positions as needed
    y_tick_labels = ['Bad', 'Neutral', 'Good']

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tick_labels)
    # Draw a horizontal line down the center
    center_position = 0  # Adjust the position as needed
    ax.axhline(center_position, color='k', linestyle='--', label='Center Line')

    # Adjust the figure size and labels
    plt.gcf().autofmt_xdate()
    plt.xlabel('Years of My Life')
    plt.title("Timeline of My Life\n\n")
    plt.grid(visible=False)


def plot_timeline_data(timeline_data):
    # Sort events by start date
    timeline_data.sort(key=lambda x: x['StartDate'])
    timeline_data.sort(key=lambda x: abs(x['Position']))

    # Iterate over the list of events to plot them
    annotation_is_up = True
    for i, event in enumerate(timeline_data):
        annotation_is_up = not annotation_is_up
        events_on_same_line = 0

        # Check for overlapping events
        for j, other_event in enumerate(timeline_data):
            if j != i:
                    if (
                            (event['StartDate'] <= other_event['EndDate'] and event['EndDate'] >= other_event['StartDate'])
                            or (other_event['StartDate'] <= event['EndDate'] and other_event['EndDate'] >= event['StartDate'])
                    ):
                        events_on_same_line += 1

        plot_event(event, events_on_same_line, annotation_is_up)

    # Save the visualization as an image (optional)
    plt.savefig('timeline.png')
    # Display the visualization
    plt.show()

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Read the CSV file into a list of events
    timeline_data = read_timeline_data('real_timeline_data.csv')
    setup_plot()
    plot_timeline_data(timeline_data)



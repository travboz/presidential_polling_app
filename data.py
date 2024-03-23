from bs4 import BeautifulSoup
import requests


def scrape_poll_data():

    URL = "https://projects.fivethirtyeight.com/polls/president-general/"

    html_data = requests.get(URL)

    soup = BeautifulSoup(html_data.content, "html.parser")

    rows = soup.find_all(class_="visible-row")

    pollster_data_array = []

    for r in rows:
        date = r.find(class_="date-wrapper").text

        pollster = r.find(class_="pollster-name").text

        sample_size = r.find(class_="sample").text

        leader = r.find(class_="leader").text
        net = r.find(class_="net").text

        answers = r.find_all(class_="answer")
        values = r.find_all(class_="value")

        if len(values) == 1:
            next_row = r.findNext("tr")
            value = next_row.find(class_="value")
            answer = next_row.find(class_="answer")
            answers.append(answer)
            values.append(value)

        first_person = answers[0].text
        second_person = answers[2].text

        first_value = values[0].find(class_="heat-map").text
        second_value = values[2].find(class_="heat-map").text

        pollster_data = {
            "date": date,
            "pollster_name": pollster,
            "leader": leader,
            "sample_size": sample_size,
            "net": net,
            "first_person": first_person,
            "first_value": first_value,
            "second_person": second_person,
            "second_value": second_value,
        }

        pollster_data_array.append(pollster_data)

    return pollster_data_array

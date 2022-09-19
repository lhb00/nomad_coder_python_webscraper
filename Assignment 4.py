from bs4 import BeautifulSoup
import requests


def extract_jobs(term):
    url = f"https://remoteok.com/remote-{term}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    if request.status_code == 200:
        results = []
        soup = BeautifulSoup(request.text, "html.parser")
        # write your ✨magical✨ code here
        jobs = soup.find("table", id="jobsboard")
        td_array = jobs.find_all(
            "td", class_="company position company_and_position")
        td_array.pop(0)
        for td in td_array:
            company = td.find("h3")
            position = td.find("h2")
            anchors = td.find_all("a", class_="preventLink")
            anchor = anchors[0]
            location = td.find_all("div", class_="location")
            region = location[0]
            wage = location[1]
            link = anchor['href']
            jobs_data = {
                "company": company.string.strip("\n"
                                                " "),
                "position": position.string.strip("\n"
                                                  " "),
                "region": region.string,
                "wage": wage.string.strip("💰 "),
                "link": f"https://remoteok.com/{link}"
            }
            results.append(jobs_data)
        for result in results:
            print(result)
            print(
                "----------------------------------------------------------------"
            )

    else:
        print("Can't get jobs.")


extract_jobs("rust")

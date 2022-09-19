from bs4 import BeautifulSoup
import requests


def extract_remoteok_jobs(term):
    url = f"https://remoteok.com/remote-{term}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    if request.status_code == 200:
        results = []
        soup = BeautifulSoup(request.text, "html.parser")
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
            link = anchor['href']
            jobs_data = {
                "link": f"https://remoteok.com/{link}",
                "company": company.string.strip("\n"
                                                " "),
                "location": region.string.strip("🇺🇸 " " 🔒" "🌏 "                            "🇪🇺 " "🇨🇦 " "🇬🇧 " "🇲🇽 " "🇩🇪 " "💰 " "*"),
                "position": position.string.strip("\n"
                                                  " ")
            }
            results.append(jobs_data)
        return results

    else:
        print("Can't get jobs.")

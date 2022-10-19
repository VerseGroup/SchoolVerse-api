from icalendar import Calendar, Event
import requests
from datetime import datetime

MONTHS_WITH_31 = [1, 3, 5, 7, 8, 10, 12]
MONTHS_WITH_30 = [4, 6, 9, 11]
MONTHS_WITH_29 = [2]

def convert_ical_to_json(ical_link):
    r = requests.get(ical_link)
    cal = Calendar.from_ical(r.text)

    events = []
    for component in cal.walk():

        if component.name == "VEVENT":
            event = {}
            event["summary"] = str(component.get("summary"))
            event["id"] = str(component.get("UID"))
            try:
                event["start"] = component.get("dtstart").dt
            except:
                event["start"] = ''
            try:
                event["end"] = component.get("dtend").dt
            except:
                event["end"] = ''
            try:
                event["location"] = str(component.get("location"))
                event["description"] = str(component.get("description"))
            except:
                pass

            if event["location"] == None:
                event["location"] = ''
            if event["description"] == None:
                event["description"] = ''

            # convert to datetime.datetime
            if type(event['start']) == datetime.time:
                event['start'] = datetime.combine(event['day'], event['start'])
            if type(event['end']) == datetime.time:
                event['end'] = datetime.combine(event['day'], event['end'])
            if type(event['start']) == datetime.date:
                event['start'] = datetime.combine(event['start'], datetime.min.time())
            if type(event['end']) == datetime.date:
                event['end'] = datetime.combine(event['end'], datetime.min.time())

            if type(event['start']) != datetime:
                event['start'] = None
            if type(event['end']) != datetime:
                event['end'] = None
            
            events.append(event)

    return events

def convert_all_school_events(ical_link):

    r = requests.get(ical_link)
    cal = Calendar.from_ical(r.text)

    events = []
    days = []
    for component in cal.walk():
         if component.name == "VEVENT":

            event = {}
            event["summary"] = str(component.get("summary"))
            event["id"] = str(component.get("UID"))

            event['start'] = component.get("DTSTART").dt
            stamp = str(event['start'])
            stamp = stamp.split('-')

            # +1 cause days are 1 off - i believe because of EST/UTC ~ fix later
            day = int(stamp[2].split(" ")[0]) + 1
            month = int(stamp[1])
            year = int(stamp[0])

            if day >= 31 and month in MONTHS_WITH_31:
                day = 1
                month += 1
            elif day >= 30 and month in MONTHS_WITH_30:
                day = 1
                month += 1
            elif day >= 29 and month in MONTHS_WITH_29:
                day = 1
                month += 1

            if month > 12:
                month = 1
                year += 1

            stamp = datetime(year, month, day)
            event['day'] = stamp

            try:
                event['start'] = component.get("DTSTART").dt
                event['end'] = component.get("DTEND").dt

                # convert to datetime.datetime
                if type(event['start']) == datetime.time:
                    event['start'] = datetime.combine(event['day'], event['start'])
                if type(event['end']) == datetime.time:
                    event['end'] = datetime.combine(event['day'], event['end'])

                if type(event['start']) == datetime.date:
                    event['start'] = datetime.combine(event['start'], datetime.min.time())
                if type(event['end']) == datetime.date:
                    event['end'] = datetime.combine(event['end'], datetime.min.time())
                
            except:
                event['start'] = None
                event['end'] = None

            # if event['day'] is type datetime.date convert to datetime.datetime
            if type(event['day']) == datetime.date:
                event['day'] = datetime.combine(event['day'], datetime.min.time())

            if type(event['day']) != datetime:
                raise Exception("day is not datetime.datetime")

            if event['start'] is not None and type(event['start']) != datetime:
                event['start'] = None

            if event['end'] is not None and type(event['end']) != datetime:
                event['end'] = None
        
            event['location'] = str(component.get("location"))
            event['description'] = str(component.get("description"))

            if "Day -" in event["summary"]:
                day = event["summary"].split("-")[1]
                days.append({
                    "day" : f"Day {day}",
                    "date" : event["day"],
                    "id" : event["id"]
                })
            else:
                events.append(event)

    return days, events

def scrape_sport() -> list:

    sport_links = {'Base.JV.B.17: Baseball - JV Boys': 'webcal://api.veracross.com/hackley/teams/96550.ics?t=cad64a0966bfc8f0cd814e3ba3ba416f&uid=F92DB59E-A8C5-41EC-A087-6D3EF83F5828', 'Base.MS.17: Baseball - Middle School': 'webcal://api.veracross.com/hackley/teams/96520.ics?t=33bda8c4b5c5a3c172dfd6b086f942e6&uid=E088CDEE-D2E0-41C4-A8C6-604B5CB8C0CB', 'Base.V.B.17: Baseball - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96557.ics?t=8701e44ea5893091d8e33f255f29f27d&uid=6507A9A5-8FCE-4879-B2D9-187F320C51F1', 'Bask.JV.B.17: Basketball - JV Boys': 'webcal://api.veracross.com/hackley/teams/96554.ics?t=cf11d1b076170874d940639d2a727b8f&uid=B9994B30-617A-4345-8E92-2EA5F3CFA734', 'Bask.JV.G.17: Basketball - JV Girls': 'webcal://api.veracross.com/hackley/teams/96545.ics?t=51ec4f2ab986ef812eea55458dadccaa&uid=DF297976-B7BC-46B9-9311-9555915BD333', 'Bask.MS.B.Blck.17: Basketball - Middle School Boys - Black': 'webcal://api.veracross.com/hackley/teams/96516.ics?t=6343de5ff85c41e38f82892d962b0e48&uid=BB5A97BB-AF12-4FC6-B799-0567ADC05DCC', 'Bask.MS.B.Gray.17: Basketball - Middle School Boys - Gray': 'webcal://api.veracross.com/hackley/teams/96525.ics?t=224f5423e4925363ad149a106d125d37&uid=80D71686-0CE1-49F8-BA5D-C2DC14B94BF8', 'Bask.MS.G.Blck.17: Basketball - Middle School Girls - Black': 'webcal://api.veracross.com/hackley/teams/96512.ics?t=512871caf994ff2c6ee42644bced28c1&uid=51911C2B-A86D-4E4F-AE90-FBB5DF53221E', 'Bask.MS.G.Gray.17: Basketball - Middle School Girls - Gray': 'webcal://api.veracross.com/hackley/teams/96528.ics?t=758fecb3eb97f3dab686167a1817575a&uid=E3735A52-ED3C-4948-83D6-C07857FE4677', 'Bask.V.B.17: Basketball - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96542.ics?t=967529c1bedc355318d7a8fce3bb8488&uid=F7BDFCF6-71A6-4297-A990-F300808CDD2C', 'Bask.V.G.17: Basketball - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96548.ics?t=449b83833918b628bf4ad00e191a4d34&uid=69A5B401-BB97-418B-B80A-2C6019249E2E', 'CrCtry.NS.C.17: Cross Country - Middle School Coed': 'webcal://api.veracross.com/hackley/teams/96529.ics?t=2e3d3e454eae6cbe7abf3f9548a72b8e&uid=1CBCDC1B-3C09-414D-A1DC-DF874D699672', 'CrCtry.V.C.17: Cross Country - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96539.ics?t=cd455f8361cd91bcb8a2e8b85e9ce51d&uid=5E486B62-A16D-483C-A16D-18A7D1F76856', 'Fenc.JV.C.17: Fencing - JV Coed': 'webcal://api.veracross.com/hackley/teams/96566.ics?t=b5a59c05240b237630843e611ae2586c&uid=D961D102-B168-4BFF-9C5F-233096D02783', 'Fenc.MS.17: Fencing - Middle School': 'webcal://api.veracross.com/hackley/teams/96530.ics?t=5cb2d6603e02084624f35de402fcc3e0&uid=1668025B-684D-4353-BABD-6A44FDFA9D97', 'Fenc.V.C.17: Fencing - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96544.ics?t=db0c4ddc1f3fc4d47da9157c629322da&uid=1296288E-4FD8-42B3-9529-295ED1FD0C97', 'FlHock.MS.17: Field Hockey - Middle School': 'webcal://api.veracross.com/hackley/teams/96531.ics?t=c1e1c13caffc9997520c2bb1d94fe187&uid=00C4BED5-E40D-4468-A0CC-8231356DB0FA', 'FlHoky.JV.17: Field Hockey - JV': 'webcal://api.veracross.com/hackley/teams/96543.ics?t=00f55dd6ace4d2355f03e53f7e894dc2&uid=E74286DC-449D-4714-B44E-C566DE0BB235', 'FlHoky.V.17: Field Hockey - Varsity': 'webcal://api.veracross.com/hackley/teams/96555.ics?t=8a195260354c25c653e621c5b078acb8&uid=D8F065BC-5A07-4B6E-ABC3-8ED3237C4734', 'Foot.JV.17: Football - JV': 'webcal://api.veracross.com/hackley/teams/96540.ics?t=adb57b2dc6a305a70a002560666a306f&uid=A4BCA146-358F-4B07-ABC5-6FC7B4D8EA78', 'Foot.MS.17: Football - Middle School': 'webcal://api.veracross.com/hackley/teams/96519.ics?t=553cdd369eacb801bb38e9ffa2cc86b0&uid=3CAEF1A1-3D42-442B-8520-6FE4EB3A5D81', 'Foot.V.17: Football - Varsity': 'webcal://api.veracross.com/hackley/teams/96558.ics?t=6c06c7422d683fbf9a493ae66472cf24&uid=42DD85FF-6BCD-427D-B323-CB1C24148064', 'Golf.V.B.17: Golf - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96564.ics?t=8a66222bc8f832c7a83a58a270c9a1ce&uid=935028D8-DDF8-441A-8AB1-58045A9A03A0', 'Golf.V.G.17: Golf - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96549.ics?t=4374e2b4f2966c8b791e3693060c0460&uid=49214825-A8FA-4557-A206-2A88B768E656', 'IdrTrck.V.C.17: Indoor Track - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96569.ics?t=cd69c4bc05207218c80503753e632ef7&uid=AC9A240B-00CD-4160-B886-7939ECE18ADF', 'Lacr.JV.B.17: Lacrosse - JV Boys': 'webcal://api.veracross.com/hackley/teams/96538.ics?t=456b4781fadecbd3fa197c9fcc55c714&uid=3B548114-E83A-4146-8363-1475EC807B5D', 'Lacr.JV.G.17: Lacrosse - JV Girls': 'webcal://api.veracross.com/hackley/teams/96537.ics?t=b129a56ee6e652c561f40988d4feddb9&uid=168B4125-F41C-46C4-8A45-16EF29C0F699', 'Lacr.MS.B.17: Lacrosse - Middle School Boys': 'webcal://api.veracross.com/hackley/teams/96522.ics?t=5538cceb7d1dc73a88852e12699c24eb&uid=FA914FCD-4EAC-4AF2-9FC7-A2692A34C7D5', 'Lacr.MS.G.17: Lacrosse - Middle School Girls': 'webcal://api.veracross.com/hackley/teams/96533.ics?t=2a6b8a47382d332e69b56ffe822ea6b1&uid=B518923B-6DC8-4108-B69B-08039F36FE6D', 'Lacr.V.B.17: Lacrosse - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96565.ics?t=259003266a9f8898de7547b4921bb886&uid=BBB586CE-E9E6-4D4A-936A-A2010D27E228', 'Lacr.V.G.17: Lacrosse - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96553.ics?t=77dbcb94a1ee57acf1bc0adfa094a86b&uid=05C08D9B-E383-4E77-BC6A-E9F7A8385286', 'Socc.JV.B.17: Soccer - JV Boys': 'webcal://api.veracross.com/hackley/teams/96552.ics?t=23a5281e08cac7e1f8a276cbe230f1e4&uid=29B4133B-F6CF-4462-A9B5-2E9CED5F7410', 'Socc.JV.G.17: Soccer - JV Girls': 'webcal://api.veracross.com/hackley/teams/96535.ics?t=34f24e96a38401f330470af97fe8b4de&uid=43FBDC42-469C-4EED-98BE-8155DA1D107B', 'Socc.MS.B.Blck.17: Soccer - Middle School Boys - Black': 'webcal://api.veracross.com/hackley/teams/96532.ics?t=ae5fd09c3a8b48d0f1833b930e533a3d&uid=9195925C-414E-48A8-9ADF-72AD7A373A32', 'Socc.MS.B.Gray.17: Soccer - Middle School Boys - Gray': 'webcal://api.veracross.com/hackley/teams/96523.ics?t=f1551bb1171b133f77c05010489a4552&uid=F0C2D05C-03EB-48F8-9695-74F032A18116', 'Socc.MS.G.17: Soccer - Middle School Girls': 'webcal://api.veracross.com/hackley/teams/96515.ics?t=913b8acc822ac3cf416377bcf5f6d6e0&uid=652B20D0-6DD6-4441-B00E-F28CA9C415B6', 'Socc.MS.G.Blck.17: Soccer - Middle School Girls - Black': 'webcal://api.veracross.com/hackley/teams/96513.ics?t=6c07edd4889d66a2412de6c9d2b80cfb&uid=5C2CDEFF-A2D4-405B-88F2-3AC63EDBC4E3', 'Socc.V.B.17: Soccer - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96556.ics?t=63e028d79709f12c1265f51819ef149a&uid=C60D1B7D-A741-40C5-AAEE-0E6BE2682B45', 'Socc.V.G.17: Soccer - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96536.ics?t=401878877006a5eb4dd904358707cc75&uid=B77D6FF6-CA3D-4728-8DA2-322E17ECE2C3', 'Soft.JV.G.17: Softball - JV Girls': 'webcal://api.veracross.com/hackley/teams/96562.ics?t=f91cc4e544d6f25c7199bbd48b7ad3a3&uid=C1D5034E-B8CB-48CE-8736-228C2291620B', 'Soft.MS.17: Softball - Middle School': 'webcal://api.veracross.com/hackley/teams/96517.ics?t=bcba9b810384453a5673fab5f2145c0b&uid=C4FBCB94-5ABA-41FB-9038-2F233FA17AF4', 'Soft.V.G.17: Softball - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96568.ics?t=123d5fa482cffcb2342972627851eaa8&uid=A633AA1C-7873-42D5-BCEE-5475E2AE830B', 'Squa.JV.B.17: Squash - JV Boys': 'webcal://api.veracross.com/hackley/teams/96561.ics?t=df7bb2b2b3a17d7f347f7fbf440243b0&uid=07C80C7F-6036-45A1-9001-A6364507D458', 'Squa.JV.G.17: Squash - JV Girls': 'webcal://api.veracross.com/hackley/teams/96563.ics?t=ec90c9d674f05197504e1b6695b18ea7&uid=5FCC7D08-288A-4B82-8B7F-06310A96457A', 'Squa.MS.C.Blck.17: Squash - Middle School Coed - Black': 'webcal://api.veracross.com/hackley/teams/96527.ics?t=3d5630fc95374caffea842f8cc2ab5df&uid=98BDFAC3-5DBD-448D-976C-1A4641C6DF1C', 'Squa.MS.C.Gray.17: Squash - Middle School Coed - Gray': 'webcal://api.veracross.com/hackley/teams/96518.ics?t=8f3cdbc162a4c494b81cc7f8f6d44b2f&uid=A508EEFF-C6D0-4828-A9F5-E408CA2683DA', 'Squa.V.B.17: Squash - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96534.ics?t=9c5f7f18b157d7c4d6a3cfa23b3c7815&uid=0FBFCCC5-FBE8-4354-ACBE-C23D04C66BCF', 'Squa.V.G.17: Squash - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96560.ics?t=3a45c09917bd22a68fbd480cc4f6593d&uid=E8C3851C-0BA0-4988-9AB7-5AE24AB13BD6', 'Swim.MS.C.17: Swimming - Middle School Coed': 'webcal://api.veracross.com/hackley/teams/96514.ics?t=0dc4c902c7cd36f3ed25ff151934846e&uid=B3640558-500A-4438-B3D1-F2C82254C999', 'Swim.V.C.17: Swimming - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96567.ics?t=5b4c3be17880c99dd3cf0323e411a4a4&uid=6124BCF1-566A-4969-A762-34E911A29626', 'Tenn.JV.B.17: Tennis - JV Boys': 'webcal://api.veracross.com/hackley/teams/96570.ics?t=bf6d2e77ca78b7438a68f4c58754f6d1&uid=BC6C5058-ADD2-409F-B92D-99CC2405DB22', 'Tenn.JV.G.17: Tennis - JV Girls': 'webcal://api.veracross.com/hackley/teams/96551.ics?t=071309440dca157304c3a6c745ab0b9c&uid=677BD4AF-B399-46C3-9366-14BC7639A0A4', 'Tenn.MS.C.Blck.17: Tennis - Middle School Coed - Black': 'webcal://api.veracross.com/hackley/teams/96521.ics?t=21b0d9b71fe1beff2e58e4480aec9c34&uid=0A7063E5-8DA1-4CE4-950C-1ED0B4ECC616', 'Tenn.MS.C.Gray.17: Tennis - Middle School Coed - Gray': 'webcal://api.veracross.com/hackley/teams/96511.ics?t=c4392d142944c19047c448bd52b780a1&uid=2955015B-C830-46B9-A083-CD89C227760F', 'Tenn.V.B.17: Tennis - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96541.ics?t=4dee80756c3534c4e2b8776faeb2de7e&uid=01D02A20-DE09-4226-8126-C4F3674DF0C5', 'Tenn.V.G.17: Tennis - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96559.ics?t=bd59200b19335f1a91437abfdca969cc&uid=041FBD9C-55C8-4DB2-AFAB-F3A897A48EFA', 'TrkFl.MS.C.17: Track & Field - Middle School Coed': 'webcal://api.veracross.com/hackley/teams/96526.ics?t=1a17976958d240c0335c42ecad3bdc79&uid=BB5C396F-42F5-4F48-93CA-51B22B56B032', 'TrkFl.V.C.17: Track & Field - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96546.ics?t=11507ca8b83dc549a0de798360a2186e&uid=004618F0-0E48-4830-8472-AB6EF8370655', 'Wres.MS.17: Wrestling - Middle School': 'webcal://api.veracross.com/hackley/teams/96524.ics?t=6806d05588257001eff3708561463500&uid=6537BF36-50BF-439A-919D-09E93C667CDA', 'Wres.V.17: Wrestling - Varsity': 'webcal://api.veracross.com/hackley/teams/96547.ics?t=31e525efbb80d82e4d69c60a276df9ae&uid=E8C10955-1598-42DF-ACAD-F0EE24D9DE9A'}

    sports = []
    for link in sport_links:
        name = link
        link = sport_links[link]
        events = convert_ical_to_json(link.replace('webcal', 'http'))

        sport = {
            'id': name,
            'events': events,
            'link': link,
            'name': name,
        }

        sports.append(sport)

    for sport in sports:
        existing_descrptions = []
        events = sport['events']
        for event in events:
            if event['description'] in existing_descrptions:
                events.remove(event)
                print(f"removed {event['description']}")
                continue
            else:
                existing_descrptions.append(event['description'])
        sport['events'] = events

    return sports

# testing
if __name__ == "__main__":
    #print(scrape_sport())
    #print(convert_all_school_events("https://api.veracross.com/hackley/subscribe/96063164-4BFD-4841-8679-0898F3C40A20.ics?uid=2B8CA74A-62FE-4859-A02A-C628CC7FDB52"))
    pass
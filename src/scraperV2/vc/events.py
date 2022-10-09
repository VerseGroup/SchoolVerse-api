from icalendar import Calendar, Event
import requests
from datetime import datetime

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
            stamp = datetime(int(stamp[0]), int(stamp[1]), int(stamp[2].split(" ")[0]))
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

    sport_links = {'Base.JV.B.17: Baseball - JV Boys': 'webcal://api.veracross.com/hackley/teams/96550.ics?t=cad64a0966bfc8f0cd814e3ba3ba416f&uid=75293E98-E9BC-47D7-B442-6E0CA251BDAC', 'Base.MS.17: Baseball - Middle School': 'webcal://api.veracross.com/hackley/teams/96520.ics?t=33bda8c4b5c5a3c172dfd6b086f942e6&uid=3BF23FCB-2ECE-4951-AA3D-46BAA15A0CD0', 'Base.V.B.17: Baseball - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96557.ics?t=8701e44ea5893091d8e33f255f29f27d&uid=A3BC3508-C69B-48C2-9B34-F68A6C2818BE', 
    'Bask.JV.B.17: Basketball - JV Boys': 'webcal://api.veracross.com/hackley/teams/96554.ics?t=cf11d1b076170874d940639d2a727b8f&uid=660902F5-0578-4D5E-AC04-566CCCA79197', 'Bask.JV.G.17: Basketball - JV Girls': 'webcal://api.veracross.com/hackley/teams/96545.ics?t=51ec4f2ab986ef812eea55458dadccaa&uid=B6B9F8CA-C323-42E5-9C7D-EB2A9DFE7C00', 'Bask.MS.B.Blck.17: Basketball - Middle School Boys - Black': 'webcal://api.veracross.com/hackley/teams/96516.ics?t=6343de5ff85c41e38f82892d962b0e48&uid=4536D5BA-5808-4661-87E5-BF3E78D936A9', 
    'Bask.MS.B.Gray.17: Basketball - Middle School Boys - Gray': 'webcal://api.veracross.com/hackley/teams/96525.ics?t=224f5423e4925363ad149a106d125d37&uid=D4D781E3-E1A5-47F8-B13E-31BFD8912C09', 'Bask.MS.G.Blck.17: Basketball - Middle School Girls - Black': 'webcal://api.veracross.com/hackley/teams/96512.ics?t=512871caf994ff2c6ee42644bced28c1&uid=531C8656-D361-4EB6-93CC-434DFD2C5E2E', 'Bask.MS.G.Gray.17: Basketball - Middle School Girls - Gray': 'webcal://api.veracross.com/hackley/teams/96528.ics?t=758fecb3eb97f3dab686167a1817575a&uid=5B495C1F-000E-4182-BC9C-2398210E13BD', 
    'Bask.V.B.17: Basketball - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96542.ics?t=967529c1bedc355318d7a8fce3bb8488&uid=AC407CBC-8DE9-4553-BF24-12F1CFA4E59F', 'Bask.V.G.17: Basketball - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96548.ics?t=449b83833918b628bf4ad00e191a4d34&uid=F07733D8-A9D0-4735-B8AF-43CB3349A16D', 'CrCtry.NS.C.17: Cross Country - Middle School Coed': 'webcal://api.veracross.com/hackley/teams/96529.ics?t=2e3d3e454eae6cbe7abf3f9548a72b8e&uid=2FFB9676-84C1-40B3-AC20-68545FCD54EF', 
    'CrCtry.V.C.17: Cross Country - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96539.ics?t=cd455f8361cd91bcb8a2e8b85e9ce51d&uid=9662B57B-D810-430E-AF3A-904A37BD017C', 'Fenc.JV.C.17: Fencing - JV Coed': 'webcal://api.veracross.com/hackley/teams/96566.ics?t=b5a59c05240b237630843e611ae2586c&uid=C2FC56D3-A015-4A25-BF41-0EAB3511B3FC', 'Fenc.MS.17: Fencing - Middle School': 'webcal://api.veracross.com/hackley/teams/96530.ics?t=5cb2d6603e02084624f35de402fcc3e0&uid=A7414D7C-56BD-40C2-96AB-DDA6A1D41288',
    'Fenc.V.C.17: Fencing - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96544.ics?t=db0c4ddc1f3fc4d47da9157c629322da&uid=5FF3C083-89C5-45B7-9625-A72D3FA170EF', 'FlHock.MS.17: Field Hockey - Middle School': 'webcal://api.veracross.com/hackley/teams/96531.ics?t=c1e1c13caffc9997520c2bb1d94fe187&uid=51A07403-0FA4-4D9F-BBC3-623AB7B65A52', 'FlHoky.JV.17: Field Hockey - JV': 'webcal://api.veracross.com/hackley/teams/96543.ics?t=00f55dd6ace4d2355f03e53f7e894dc2&uid=D2B53DD5-2EE3-4E1D-8491-774988C59454', 
    'FlHoky.V.17: Field Hockey - Varsity': 'webcal://api.veracross.com/hackley/teams/96555.ics?t=8a195260354c25c653e621c5b078acb8&uid=6051C3FC-53DC-4191-BEDF-A8114DFC852B', 'Foot.JV.17: Football - JV': 'webcal://api.veracross.com/hackley/teams/96540.ics?t=adb57b2dc6a305a70a002560666a306f&uid=21E6AECC-1870-4CE8-90F5-012E4D34C72D', 'Foot.MS.17: Football - Middle School': 'webcal://api.veracross.com/hackley/teams/96519.ics?t=553cdd369eacb801bb38e9ffa2cc86b0&uid=B397BA5C-C711-41AD-92BA-8DEB780C3A45', 
    'Foot.V.17: Football - Varsity': 'webcal://api.veracross.com/hackley/teams/96558.ics?t=6c06c7422d683fbf9a493ae66472cf24&uid=372E56F7-2F81-493C-8F97-BB83314FF03A', 'Golf.V.B.17: Golf - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96564.ics?t=8a66222bc8f832c7a83a58a270c9a1ce&uid=2AF74DA7-D10D-4797-9B59-D756767E5DB9', 'Golf.V.G.17: Golf - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96549.ics?t=4374e2b4f2966c8b791e3693060c0460&uid=B2308361-FFE8-471B-A0C9-40DD92E4410D', 
    'IdrTrck.V.C.17: Indoor Track - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96569.ics?t=cd69c4bc05207218c80503753e632ef7&uid=04AFA632-7140-43CB-B2B0-77A736D0C3CE', 'Lacr.JV.B.17: Lacrosse - JV Boys': 'webcal://api.veracross.com/hackley/teams/96538.ics?t=456b4781fadecbd3fa197c9fcc55c714&uid=93435E31-7713-45CD-8182-A4E5CC2233BF', 'Lacr.JV.G.17: Lacrosse - JV Girls': 'webcal://api.veracross.com/hackley/teams/96537.ics?t=b129a56ee6e652c561f40988d4feddb9&uid=803F6D23-DB7F-48DA-8125-853C28DA8BA9', 
    'Lacr.MS.B.17: Lacrosse - Middle School Boys': 'webcal://api.veracross.com/hackley/teams/96522.ics?t=5538cceb7d1dc73a88852e12699c24eb&uid=CBA857D4-9576-430B-A6EB-C0159E812413', 'Lacr.MS.G.17: Lacrosse - Middle School Girls': 'webcal://api.veracross.com/hackley/teams/96533.ics?t=2a6b8a47382d332e69b56ffe822ea6b1&uid=7DD01110-AFAE-4F20-A0B4-C34FC1E0C7E9', 'Lacr.V.B.17: Lacrosse - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96565.ics?t=259003266a9f8898de7547b4921bb886&uid=C40110EA-6445-45E6-AC6B-48D01366FAF9', 
    'Lacr.V.G.17: Lacrosse - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96553.ics?t=77dbcb94a1ee57acf1bc0adfa094a86b&uid=6F6AD79D-8611-43E3-976C-552A22857B1E', 'Socc.JV.B.17: Soccer - JV Boys': 'webcal://api.veracross.com/hackley/teams/96552.ics?t=23a5281e08cac7e1f8a276cbe230f1e4&uid=74288B55-3C44-4242-A823-11929F196387', 'Socc.JV.G.17: Soccer - JV Girls': 'webcal://api.veracross.com/hackley/teams/96535.ics?t=34f24e96a38401f330470af97fe8b4de&uid=074BF7F7-B8B9-4217-B316-992EA19B98D3', 
    'Socc.MS.B.Blck.17: Soccer - Middle School Boys - Black': 'webcal://api.veracross.com/hackley/teams/96532.ics?t=ae5fd09c3a8b48d0f1833b930e533a3d&uid=F79154FE-25BE-443D-9A96-F6A81DB21A44', 'Socc.MS.B.Gray.17: Soccer - Middle School Boys - Gray': 'webcal://api.veracross.com/hackley/teams/96523.ics?t=f1551bb1171b133f77c05010489a4552&uid=FFCC1B70-D5C5-4E3B-95C5-0804B1C7EB71', 'Socc.MS.G.17: Soccer - Middle School Girls': 'webcal://api.veracross.com/hackley/teams/96515.ics?t=913b8acc822ac3cf416377bcf5f6d6e0&uid=7F9312A6-0C19-49AA-A368-7CFB6E4C193F', 
    'Socc.MS.G.Blck.17: Soccer - Middle School Girls - Black': 'webcal://api.veracross.com/hackley/teams/96513.ics?t=6c07edd4889d66a2412de6c9d2b80cfb&uid=84F145E9-5E64-4F50-A089-E9C6FEDDE365', 'Socc.V.B.17: Soccer - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96556.ics?t=63e028d79709f12c1265f51819ef149a&uid=942D8EB2-D9E9-4FE7-89AC-BDD9DA2A8E53', 'Socc.V.G.17: Soccer - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96536.ics?t=401878877006a5eb4dd904358707cc75&uid=EE9A5D74-8797-4D81-A4DC-1EFADB02D5A3', 
    'Soft.JV.G.17: Softball - JV Girls': 'webcal://api.veracross.com/hackley/teams/96562.ics?t=f91cc4e544d6f25c7199bbd48b7ad3a3&uid=2DA744BF-8243-42BB-A7B0-1A0D121C58F3', 'Soft.MS.17: Softball - Middle School': 'webcal://api.veracross.com/hackley/teams/96517.ics?t=bcba9b810384453a5673fab5f2145c0b&uid=468169D5-C020-4458-87F3-2F51FF767F68', 'Soft.V.G.17: Softball - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96568.ics?t=123d5fa482cffcb2342972627851eaa8&uid=5F9D71CB-177B-4C25-B5EF-2F3787A2F554', 
    'Squa.JV.B.17: Squash - JV Boys': 'webcal://api.veracross.com/hackley/teams/96561.ics?t=df7bb2b2b3a17d7f347f7fbf440243b0&uid=B86E1E68-B2CD-4CD7-9327-8FEBFB2BBC0E', 'Squa.JV.G.17: Squash - JV Girls': 'webcal://api.veracross.com/hackley/teams/96563.ics?t=ec90c9d674f05197504e1b6695b18ea7&uid=968CAD68-0C22-4E0E-956E-7C3F5675B23F', 'Squa.MS.C.Blck.17: Squash - Middle School Coed - Black': 'webcal://api.veracross.com/hackley/teams/96527.ics?t=3d5630fc95374caffea842f8cc2ab5df&uid=95F91336-45C0-4926-8176-D2D0D80AF6F1', 
    'Squa.MS.C.Gray.17: Squash - Middle School Coed - Gray': 'webcal://api.veracross.com/hackley/teams/96518.ics?t=8f3cdbc162a4c494b81cc7f8f6d44b2f&uid=A197F209-5DAA-4CE3-BD7E-686308F4F180', 'Squa.V.B.17: Squash - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96534.ics?t=9c5f7f18b157d7c4d6a3cfa23b3c7815&uid=2DBC554F-43D1-463E-8734-71E517A99167', 'Squa.V.G.17: Squash - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96560.ics?t=3a45c09917bd22a68fbd480cc4f6593d&uid=DA01150D-A0C2-41B0-A431-C71FD6A07AD6', 
    'Swim.MS.C.17: Swimming - Middle School Coed': 'webcal://api.veracross.com/hackley/teams/96514.ics?t=0dc4c902c7cd36f3ed25ff151934846e&uid=E8DFFDED-89F8-4E9A-8D28-D39E6417980E', 'Swim.V.C.17: Swimming - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96567.ics?t=5b4c3be17880c99dd3cf0323e411a4a4&uid=4FCD4BC5-F2F2-48A5-8939-FB3648F9845B', 'Tenn.JV.B.17: Tennis - JV Boys': 'webcal://api.veracross.com/hackley/teams/96570.ics?t=bf6d2e77ca78b7438a68f4c58754f6d1&uid=BFAF8093-61D0-4C3D-B439-2E4CDE4D75AD', 
    'Tenn.JV.G.17: Tennis - JV Girls': 'webcal://api.veracross.com/hackley/teams/96551.ics?t=071309440dca157304c3a6c745ab0b9c&uid=64F3BAED-F24C-4F36-9DF3-747F0734D96A', 'Tenn.MS.C.Blck.17: Tennis - Middle School Coed - Black': 'webcal://api.veracross.com/hackley/teams/96521.ics?t=21b0d9b71fe1beff2e58e4480aec9c34&uid=5E739756-257A-4D29-91B8-231180A76AE5', 'Tenn.MS.C.Gray.17: Tennis - Middle School Coed - Gray': 'webcal://api.veracross.com/hackley/teams/96511.ics?t=c4392d142944c19047c448bd52b780a1&uid=37169041-CABC-4673-B88C-F28277ABED97', 
    'Tenn.V.B.17: Tennis - Varsity Boys': 'webcal://api.veracross.com/hackley/teams/96541.ics?t=4dee80756c3534c4e2b8776faeb2de7e&uid=888CA248-9ED2-4FD2-8A88-D571BAE0365C', 'Tenn.V.G.17: Tennis - Varsity Girls': 'webcal://api.veracross.com/hackley/teams/96559.ics?t=bd59200b19335f1a91437abfdca969cc&uid=FC1B7A84-6583-4CE9-871D-41223A780F34', 'TrkFl.MS.C.17: Track & Field - Middle School Coed': 'webcal://api.veracross.com/hackley/teams/96526.ics?t=1a17976958d240c0335c42ecad3bdc79&uid=9AC5EECD-5E01-4B85-A96B-9AB5B8C45C1B', 
    'TrkFl.V.C.17: Track & Field - Varsity Coed': 'webcal://api.veracross.com/hackley/teams/96546.ics?t=11507ca8b83dc549a0de798360a2186e&uid=E0FBBCF4-DEA1-4EF1-ABB5-A326F18FE7BB', 'Wres.MS.17: Wrestling - Middle School': 'webcal://api.veracross.com/hackley/teams/96524.ics?t=6806d05588257001eff3708561463500&uid=DF9445F9-34C1-40C1-8CE6-18C153873F04', 'Wres.V.17: Wrestling - Varsity': 'webcal://api.veracross.com/hackley/teams/96547.ics?t=31e525efbb80d82e4d69c60a276df9ae&uid=2216DC78-7082-4EF7-B513-133644484D0D'}

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

    return sports

# testing
if __name__ == "__main__":
    #print(scrape_sport())
    #print(convert_all_school_events("https://api.veracross.com/hackley/subscribe/96063164-4BFD-4841-8679-0898F3C40A20.ics?uid=2B8CA74A-62FE-4859-A02A-C628CC7FDB52"))
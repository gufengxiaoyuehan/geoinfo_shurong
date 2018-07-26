import requests

data = {
	"_id" : "55c89cf7093a0c0fd69c5d39",
	"properties" : {
		"text" : "I need his hugs, his touch, his kiss, and his smile 😪#rolandandcaixi #hoddies #superman #red #wink #sweetsweetlove",
		"userID" : "insta1465128558",
		"userName" : "florence_caixi",
		"day" : "30",
		"month" : "06",
		"year" : "2015",
		"hour" : "14",
		"minute" : "56",
		"second" : "04",
		"source" : "instagram",
		"sentiment" : "positive",
		"sentiStrings" : "",
		"labelledSentiment" : "positive",
		"crowder" : "admin"
	},
	"coordinate" : {
		"type" : "Point",
		"coordinates" : [
			103.735324891,
			1.340812684
		]
	}
}
r = requests.post("http://127.0.0.1:5000/api/v1.0/infos/", json=data)
print(r.status_code)
# Hadasim

הנחות מקלות בהסבר:השרת והלקוח רצים מאותה נקודת קצה (מחשב אישי).
אופן השימוש:מתחברים לmongodb compass שמחובר לmongodb atlas
מריצים את קוד השרת שנמצא בקובץ app.py 
על מנת לקבל את רשימת כל החברים בקופת חולים נשתמש בניתוב "api/members"
דוגמת הרצה:![image](https://github.com/rivkaadler1/Hadasim/assets/79863410/fd4a5ce5-e8e8-420b-afb8-53379b73e783)
על מנת לקבל חבר מסוים במערכת נשתמש לדוגמה בניתוב :api/members?member_id=223456789
דוגמת הרצה:![image](https://github.com/rivkaadler1/Hadasim/assets/79863410/5e97c254-c56b-4f77-a2cf-e7d55dd68bb0)
על מנת להכניס רשומה חדשה נשתמש בTest by curlבניתוב מהסוג:curl -X POST http://localhost:5000/api/members -H 'Content-Type: application/json' -d '{"first_name": "Yedidya", "last_name": 
"Adler", "address": {"city": "Petah Tikva", "street": "Trumpeldor", "number": "22"}, "date_of_birth": "2002-05-20", 
"telephone": "+1-555-970-1212", "mobile_phone": "+54-876-1904", "vaccine_dates": ["2021-06-01"], "vaccine_manufacturers": ["Moderna"], "positive_result_date": null, 
"recovery_date": null, "member_id": "394959999"}' 
 
דוגמת הרצה:![image](https://github.com/rivkaadler1/Hadasim/assets/79863410/af72357d-2722-4d85-839d-bcdbd4b016d1)
ניתן לראות שהובייקט הוסף לבסיס הנתונים:
![image](https://github.com/rivkaadler1/Hadasim/assets/79863410/28b6146c-1cc6-4949-8610-ea302bca9120)

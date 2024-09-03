from utils import DataBaza

db = DataBaza()
print_ = True
while True:

    if print_:
        print("Assalomu alaykum! Programmamizga xush kelibsiz!")
        print("Databaza bilan bog'liq operatsiyalarni bajarishni boshlaymiz..."); print_ = False
    
    amal = input("Iltimos, databazaga xodimni\
                 qo'shish uchun ADD,\n\
                 o'chirib tashlash uchun DEL,\n\
                 tekshirish uchun CHECK\n\
                 buyruqlaridan birini tanlang: ").lower()
    if amal == "chiqish": break
    elif not amal in ["add", "del", "check"]: print("Bajarmoqchi bo'layotgan operatsiya mavjud emas, iltimos ADD yoki DEL yoki CHECK dan birini tanlang!"); continue
    elif amal == "add": user_id = db.add_user(); break
    elif amal == "del": 
        del_id = int(input(f"Iltimos, databazadan o'chiriladigan id ni kiriting: "))
        db.del_user(del_id); break
    elif amal == "check": xodim_id, aniqlilik_darajasi = db.check_db(); break



            
    


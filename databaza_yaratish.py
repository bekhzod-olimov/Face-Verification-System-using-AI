import face_recognition, os, pickle
from glob import glob

db_yulak, rasmlar_turgan_yulak = "databazalar", "test_uchun_rasmlar"
os.makedirs(db_yulak, exist_ok = True)

def db_yaratish(rasmlar_yulagi, id_nomi, db_yulagi):

    if os.path.isfile(db_yulagi): 
        with open(db_yulagi, "rb") as f: databaza = pickle.load(f); print(f"Databazada mavjud id lar -> {databaza.keys()}")
    else: databaza = {}

    rasm_fayllari = [".jpg", ".jpeg", ".png"]
    rasmlar = glob(f"{rasmlar_yulagi}/{id_nomi}/*{[fayl for fayl in rasm_fayllari]}")
    xodimlar_soni = len(rasmlar)
    print(f"{id_nomi} xodimning {xodimlar_soni} dona rasmi topildi!\n")

    for idx, rasm in enumerate(rasmlar):
        if idx == 1: break
        print(f"{idx + 1} / {xodimlar_soni}")
        print(f"{id_nomi} xodimni databazaga qo'shish jarayoni boshlandi...")
        xodim_rasmi = face_recognition.load_image_file(rasm)
        xodim_ftlari = face_recognition.face_encodings(xodim_rasmi)[0]
        databaza[id_nomi] = xodim_ftlari
        print(f"{id_nomi} xodimni databazaga qo'shish jarayoni muvafaqqiyatli yakunlandi!\n")

    with open(db_yulagi, "wb") as fayl: print(f"Databazada mavjud id lar -> {databaza.keys()}"); pickle.dump(databaza, fayl)

id_nomi = str(input("Iltimos, xodimning id ni kiriting: "))
db_yulagi = f"{db_yulak}/{input('Iltimos, tashkilotning nomini kiriting: ')}.pkl"


db_yaratish(rasmlar_yulagi = rasmlar_turgan_yulak, id_nomi = id_nomi, db_yulagi = db_yulagi)

    


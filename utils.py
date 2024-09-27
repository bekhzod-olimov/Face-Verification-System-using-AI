# Import libraries
import os, cv2, pickle, face_recognition, numpy as np
from glob import glob; from PIL import Image
from src.anti_spoof_predict import AntiSpoofPredict

class DataBaza:

    def __init__(self, db_path = "databaza", db_name = "db.pkl", models_path = "antispoofing"):
        self.db_path, self.db_name, self.models_path = db_path, db_name, models_path
        self.db_full_path = f"{self.db_path}/{self.db_name}"
        self.model_test = AntiSpoofPredict("-1")

    # Function to create database
    def create_db(self): os.makedirs(self.db_path, exist_ok = True); self.databaza = {}; self.id = 0
        
    def load_db(self, check = False):

        """

        This function loads database.
        
        """
        
        print("Databaza yuklanmoqda, iltimos kuting...")
        with open(self.db_full_path, "rb") as f: self.databaza = pickle.load(f)
        print(f"DBdagi hozirgi id lar -> {self.databaza.keys()}")
        if not check: self.id = list(self.databaza.keys())[-1]

    def save_db(self): 
        with open(self.db_full_path, "wb") as fayl: 
            print(f"Databazada mavjud id lar -> {list(self.databaza.keys())}"); 
            pickle.dump(self.databaza, fayl)

    def add_user(self, arr = ["test_uchun_rasmlar/abbosjon/03-3.jpg", "test_uchun_rasmlar/abbosjon/04-4.jpg", "test_uchun_rasmlar/abbosjon/05-5.jpg"]):
# ["test_uchun_rasmlar/ibrohimjon/IMG_20240427_165959_061.jpg", "test_uchun_rasmlar/ibrohimjon/IMG_20240427_170003_137.jpg", "test_uchun_rasmlar/ibrohimjon/IMG_20240427_170005_467.jpg"]
# ["test_uchun_rasmlar/abdukarim/02-3.jpg", "test_uchun_rasmlar/abdukarim/02-5.jpg", "test_uchun_rasmlar/abdukarim/abdukarim.jpg"]
# ["test_uchun_rasmlar/eldor/IMG_20240427_170251_778.jpg", "test_uchun_rasmlar/eldor/IMG_20240427_170258_010.jpg", "test_uchun_rasmlar/eldor/IMG_20240427_170302_269.jpg"]
# ["test_uchun_rasmlar/abbosjon/03-3.jpg", "test_uchun_rasmlar/abbosjon/04-4.jpg", "test_uchun_rasmlar/abbosjon/05-5.jpg"]

        if not os.path.isfile(self.db_full_path): 
            print("Databaza yangidan yaratilmoqda...")
            self.create_db()
        else: self.load_db()

        print(f"Xodimning {len(arr)} dona rasmi topildi!\n")
        print(f"Xodimni databazaga qo'shish jarayoni boshlanmoqda...")

        self.id += 1
        ftlar = []
        for idx, rasm_yulagi in enumerate(arr):
            xodim_rasmi, xodim_ftlari = self.get_fts(rasm_yulagi)
            ftlar.append(xodim_ftlari)
        self.databaza[self.id] = ftlar
        print(f"Xodimni databazaga qo'shish jarayoni muvafaqqiyatli yakunlandi!\n")

        # for idx, rasm_yulagi in enumerate(arr):
        #     if idx == 1: break
        #     xodim_rasmi, xodim_ftlari = self.get_fts(rasm_yulagi)
        #     self.databaza[self.id] = xodim_ftlari
        # print(f"Xodimni databazaga qo'shish jarayoni muvafaqqiyatli yakunlandi!\n")
        
        self.save_db()

        return self.id

    def del_user(self, del_id):

        self.load_db()
        if del_id not in self.databaza: print("Xodim databaza mavjud emas.")
        elif del_id in self.databaza:
            print(f"{del_id} id bilan saqlangan foydalanuvchining ma'lumotlari databazadan o'chirilmoqda...\n")
            del self.databaza[del_id]; self.save_db()
        self.load_db()
            
        return del_id
    
    def get_fts(self, rasm_yulagi): 

        xodim_rasmi = face_recognition.load_image_file(rasm_yulagi)
        xodim_ftlari = face_recognition.face_encodings(xodim_rasmi)[0]

        return xodim_rasmi, xodim_ftlari
    
    def read_image(self, rasm_yulagi): return cv2.cvtColor(cv2.imread(rasm_yulagi), cv2.COLOR_BGR2RGB)

    def get_pil_im(self, im_path): return Image.open(im_path).convert("RGB")

    def get_info(self, rasm):

        yuz_koordinatalari = face_recognition.face_locations(rasm)
        yuz_xususiyatlari = face_recognition.face_encodings(rasm, yuz_koordinatalari)

        return yuz_koordinatalari, yuz_xususiyatlari

    def antispoofing(self, rasm_yulagi, model_path):

        ori_im = self.get_pil_im(rasm_yulagi)
        image_bbox = self.model_test.get_bbox(np.array(ori_im))
        x1, y1, x2, y2 = image_bbox
        ori_im = ori_im.crop((x1, y1, x1+x2, y1+y2))

        return self.model_test.predict(ori_im, model_path)
    
    def check_db(self, data = {"image": "xodimlar_rasmlari/abbosjon.jpg", "data": [1,2,3,4]}): # data = {"image": "xodimlar_rasmlari/abbosjon.jpg", "data": [1,7,5,8]}
        self.load_db(check = True)

        assert "image" in list(data.keys()), print("Berilgan ma'lumotda rasm image kaliti bilan berilishi kerak.")
        assert "data" in list(data.keys()), print("Berilgan ma'lumotda tekshiriladigan id lar data kaliti bilan berilishi kerak.")

        tek_idlar = list(data["data"])
        
        res = {key: self.databaza[key] for key in self.databaza.keys() & tek_idlar}
        
        ftlar = list(res.values())
        idlar = list(res.keys())
        print(idlar)

        rasm_yulagi = data["image"]

        soxta_haqiqiy_bashorat = np.zeros((1, 3))
        
        models_paths = glob(f"{self.models_path}/*.pth")
        for idx, model_path in enumerate(models_paths):
            # if idx == 0: continue
            soxta_haqiqiy_bashorat += self.antispoofing(rasm_yulagi = rasm_yulagi, model_path = model_path)
        print(soxta_haqiqiy_bashorat)
        bashorat = np.argmax(soxta_haqiqiy_bashorat)
        aniqlilik = soxta_haqiqiy_bashorat[0][bashorat]/2
        
        # if bashorat == 1 or bashorat == 2: 
        if bashorat == 1: 
            print(f"Rasmdagi insonning yuzi {aniqlilik*100:.2f}% aniqlik bilan HAQIQIY bo'lgani uchun databazadan qidirishni boshlaymiz...")
        else: print(f"Rasmdagi insonning yuzi {aniqlilik*100:.2f}% aniqlik bilan SOXTA!\n"); print("Bizning tizim HAQIQIY inson yuzinigina taniy oladi.\nNoqulayliklar uchun uzr so'raymiz!")
        
        
        yuz_koordinatalari, yuz_xususiyatlari = self.get_info(self.read_image(rasm_yulagi))
        yuz_nomlari = []

        # for yuz_xususiyati in yuz_xususiyatlari:
            
        #     topilgan_yuzlar = face_recognition.compare_faces(ftlar, yuz_xususiyati)
        #     natijalar = face_recognition.face_distance(ftlar, yuz_xususiyati)
        #     print(natijalar)
            
        #     aniqlangan_xodim_indeksi = np.argmin(natijalar)
        #     aniqlilik_darajasi = 1 - natijalar[aniqlangan_xodim_indeksi]
        #     if topilgan_yuzlar[aniqlangan_xodim_indeksi]: xodim_id = idlar[aniqlangan_xodim_indeksi]
        #     print(f"{(aniqlilik_darajasi * 100):.2f}% aniqlik bilan rasmdagi inson -> {os.path.splitext(os.path.basename(rasm_yulagi))[0]} | Databazadagi eng yaqin id -> {xodim_id}")

        print_aniqlilik, xodim_id = 0, None
        for yuz_xususiyati in yuz_xususiyatlari:

            for ft, id in zip(ftlar, idlar):

                natijalar = np.mean(face_recognition.face_distance(ft, yuz_xususiyati))
                aniqlilik_darajasi = 1 - natijalar
                # print(aniqlilik_darajasi)

                if aniqlilik_darajasi > print_aniqlilik:
                    print_aniqlilik = aniqlilik_darajasi
                    xodim_id = id               
                
            print(f"Rasmdagi inson -> {os.path.splitext(os.path.basename(rasm_yulagi))[0]} | {(print_aniqlilik * 100):.2f}% aniqlik bilan databazadagi eng yaqin id -> {xodim_id}")

            return xodim_id, print_aniqlilik


         




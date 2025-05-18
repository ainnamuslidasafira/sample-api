# import package
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel # parent class untuk buat schema di request body
import pandas as pd
from datetime import datetime # untuk mendapatkan waktu terkini

# membuat object FastAPI
app = FastAPI()

# API Authentication
# password
password = "kopiluwakgabikinkenyang123"


# membuat endpoint -> ketentuan untuk client membuat request
# function (get, put, post, delete)
# url (/...)


# endpoint pertama/root untuk mendapatkan pesan "selamat datang"
@app.get("/")
def getWelcome():
    return {
        "msg": "Selamat Datang!"
    }

# endpoint untuk menampilkan semua isi dataset
@app.get("/profile")
def getData():
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")
    # mengembalikan respon isi dataset
    return df.to_dict(orient="records")

# routing/path parameter -> url dinamis -> menyesuaikan dengan data yang ada di server
# endpoint untuk menampilkan data sesuai dengan lokasi
@app.get("/data/{location}")
def getData(location: str):
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")
    # filter data berdasarkan parameter lokasi
    result = df[df.location == location]
    # validate apakah hasilnya ada
    if len(result) == 0:
        # menampilkan pesan error -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data not found!")
    # mengembalikan respon isi dataset
    return result.to_dict(orient="records")

# endpoint untuk menghapus data berdasarkan id
@app.delete("/data/{id}")
def deleteData(id: int, api_key: str =  Header(None)):

    # PROSES AUTHENTICATION /  VERIFIKASI
    if api_key == None or api_key != password:
        # AUTHENTICATION tidak ada, kasih pesan error -> tidak ada akses
        raise HTTPException(status_code=401, detail="You don't have access!")
    
    # AUTHENTICATION kalau ada, lanjut ke proses delete dibawah ini
    
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")
    # cek apakah datanya ada
    result = df[df.id == id]
    if len(result) == 0:
        # menampilkan pesan error -> data tidak ditemukan
        raise HTTPException(status_code=404, detail="Data not found!")
    # proses hapus data
    # condition
    result = df[df.id != id]
    # update csv, supaya ngefek ke file csvnya
    result.to_csv('dataset.csv', index=False)
    return{
        "msg": "Data has been deleted!"
    }

# schema/model untuk request body
class Profile(BaseModel):
    id: int
    name: str
    age: int
    location: str

# endpoint untuk menambah data baru
# perlu ada request body -> perlu membuat schema/model
@app.post("/data")
def createData(profile: Profile):
    # melakukan proses pengambilan data dari csv
    df = pd.read_csv("dataset.csv")
    # proses menambah baris data
    newData = pd.DataFrame({
        "id": [profile.id],
        "name": [profile.name],
        "age": [profile.age],
        "location": [profile.location],
        "created_at": [datetime.now().date()],
    })

    print(newData)
    
    # concat
    df = pd.concat([df, newData])
     # update csv, supaya ngefek ke file csvnya
    df.to_csv('dataset.csv', index=False)

    return {
        "msg": "Data has been created!"
    }


# untuk matiin fastapi: di terminal ctrl + c 

# fastapi dev berlaku hanya untuk file main.py (default)
# kalau beda nama misal app.py di terminal run fastapi dev app.py

# SUMMARY
# setiap endpoint ada function
# setiap function ada return, berupa dict agar bisa diproses json
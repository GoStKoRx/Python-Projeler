from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)



def load_student_grades(filename):
    df = pd.read_excel(filename)
    student_grades = {}
    passwords = {}


    for _, row in df.iterrows():
        student_num = str(row["Öğrenci No"])
        student_grades[student_num] = int(row["Not"])
        passwords[student_num] = student_num

    return student_grades, passwords



def give_feedback(grade):
    if 90 <= grade <= 100:
        return "Mükemmel . Bolca deneme çöz ve testlere devam et."
    elif 75 <= grade <= 89:
        return "Çok iyi, ama daha da iyisi olabilir! Konuların büyük kısmını biliyorsun, ancak detayları kaçırmamak için eksiklerini gözden geçir. Sınav pratiği yap."
    elif 50 <= grade <= 74:
        return "Fena değil, ama geliştirebilirsin! Eksik olduğun konulara yoğunlaş. Daha fazla pratik yap ve temelini güçlendir. Özet çıkar, bol soru çöz."
    elif 30 <= grade <= 49:
        return "Temeli oturtmalısın, ama başarabilirsin! Konuları baştan al ve temel kavramları iyice anla. Önce kolaydan başla, sonra zor sorulara geç. Çalışma disiplinini artır."
    else:
        return "Şu an zorlanıyor olabilirsin, ama pes etme! En baştan, sıfırdan bir çalışma planı oluştur. Anlamadığın yerleri öğretmenine veya arkadaşlarına sor. Sabırlı ol ve adım adım ilerle."



@app.route('/', methods=['GET', 'POST'])
def login():
    student_grades, passwords = load_student_grades('Öğrenci Not.xlsx')

    if request.method == 'POST':
        student_num = request.form['student_num']
        student_password = request.form['student_password']


        if student_num in student_grades and passwords[student_num] == student_password:
            grade = student_grades[student_num]
            feedback = give_feedback(grade)
            return render_template('result.html', grade=grade, feedback=feedback)
        else:
            return render_template('login.html', error="Hatalı öğrenci numarası veya şifre!")

    return render_template('login.html')



if __name__ == "__main__":
    app.run(debug=True)
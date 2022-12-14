from tkinter import *
from tkinter import messagebox
import sqlite3, os

def catToNum(catStr):
    catStr = catStr.strip(' \t\n\r')
    if (catStr == 'Канцтовары'):
        return 1
    elif (catStr == 'Оргтехника'):
        return 2
    elif (catStr == 'Обслуживание'):
        return 3
    elif (catStr == 'Аренда'):
        return 4
    elif (catStr == 'Электроэнергия'):
        return 5
    elif (catStr == 'Заработ. плата'):
        return 6
    else:
        return 0

def numToCat(numCat):
    if (numCat == 0):
        return 'Разное'
    if (numCat == 1):
        return 'Канцтовары'
    if (numCat == 2):
        return 'Оргтехника'
    if (numCat == 3):
        return 'Обслуживание'
    if (numCat == 4):
        return 'Аренда'
    if (numCat == 5):
        return 'Электроэнергия'
    if (numCat == 6):
        return 'Заработ. плата'
    
def main():
    # Название файла базы данных
    DataBaseName = 'finances.db'
    
    # Подключаемся к базе данных
    con = sqlite3.connect(DataBaseName, timeout=1)
    cur = con.cursor()
    
    # Создаем базу данных
    sql = 'CREATE TABLE IF NOT EXISTS finances (ID integer primary key autoincrement, year integer, month integer, type integer, price integer, datetimestr text, title text)'
    cur.execute(sql)
    con.commit()
    
    def ShowBtn_Click():
        # Делаем запрос в базу
        sql = 'SELECT * FROM finances WHERE month = ' + MonthEdt.get().strip(' \t\n\r') + ' and year = ' + YearEdt.get().strip(' \t\n\r')
        cur.execute(sql)
        con.commit()
        Memo1.delete('1.0', END)
        Memo1.insert(END, "Год\tМесяц\tТип\t\tНазвание\t\t\tСумма\tДата и время\n")
        records = cur.fetchall()
        for row in records:
            Memo1.insert(END, str(row[1]) + "\t" + str(row[2]) + "\t" + numToCat(row[3]) + "\t\t" + row[6] + "\t\t\t" + str(row[4]) + "\t" + row[5] + "\n")
        #Edit1.delete(0, 'end')
        #Edit1.insert(END, 'test')

        #Memo1.delete('1.0', END)
        #Memo1.insert(END, 'test')

        #ListBox1.delete(0, END)
        #ListBox1.insert(END, 'test' "\n")

    def AddBtn_Click():
        if (ListBox1.curselection()):
            #messagebox.showinfo('App', str(catToNum(ListBox1.get(ListBox1.curselection()))))
            sql = 'INSERT INTO finances (year, month, type, price, datetimestr, title) VALUES (' + YearEdt.get() + ', ' + MonthEdt.get() + ', ' + str(catToNum(ListBox1.get(ListBox1.curselection()))) + ', ' + PriceEdt.get() + ', "' + DateEdt.get() + '", "' + NameEdt.get() + '")'
            cur.execute(sql)
            con.commit()
            ShowBtn_Click()

    def StatBtn_Click():
        sql = 'SELECT * FROM finances WHERE month = ' + MonthEdt.get() + ' and year = ' + YearEdt.get()
        cur.execute(sql)
        con.commit()
        monthSum = 0
        records = cur.fetchall()
        for row in records:
            monthSum += row[4]
        PriceMonthLbl.config(text = 'Потрачено за ' + MonthEdt.get() + ' месяц: ' + str(monthSum) + ' руб.')

        sql = 'SELECT * FROM finances WHERE year = ' + YearEdt.get()
        cur.execute(sql)
        con.commit()
        yearSum = 0
        records = cur.fetchall()
        for row in records:
            yearSum += row[4]
        Label8.config(text = 'Потрачено за ' + YearEdt.get() + ' год: ' + str(yearSum) + ' руб.')
        Label9.config(text = 'Вероятно за ' + str(int(YearEdt.get()) + 1) + ' год' + "\n" + 'будет потрачено: ' + str(yearSum * 1.05) + ' руб.')

        if (ListBox1.curselection()):
            sql = 'SELECT * FROM finances WHERE month = ' + MonthEdt.get() + ' and type = ' + str(catToNum(ListBox1.get(ListBox1.curselection())))
            cur.execute(sql)
            con.commit()
            typeSum = 0
            records = cur.fetchall()
            for row in records:
                typeSum += row[4]
            Label9.config(text = 'В категории "' + ListBox1.get(ListBox1.curselection()).strip(' \t\n\r') + "\"\n" + 'потрачено: ' + str(typeSum) + ' руб.')
            
        

    window = Tk()
    window.title("Финансы предприятия")

    AppWidth = 710
    AppHeight = 362

    ScreenWidth = window.winfo_screenwidth()
    ScreenHeight = window.winfo_screenheight()
    window.geometry('%dx%d+%d+%d' % (AppWidth, AppHeight, (ScreenWidth - AppWidth) / 2, (ScreenHeight - AppHeight) / 2))
    window.resizable(width=False, height=False)

    Label1 = Label(window, text="Введите месяц:")
    Label1.place(x=8,y=8,width=95,height=13)
    MonthEdt = Entry(window)
    MonthEdt.place(x=8,y=24,width=121,height=21)
    Label2 = Label(window, text="Введите год:")
    Label2.place(x=136,y=8,width=90,height=13)
    YearEdt = Entry(window)
    YearEdt.place(x=136,y=24,width=121,height=21)
    Memo1 = Text(window)
    Memo1.place(x=8,y=88,width=690,height=89)
    Label3 = Label(window, text="Расходы за месяц:")
    Label3.place(x=8,y=60,width=100,height=13)
    ShowBtn = Button(window, text="Показать", command=ShowBtn_Click)
    ShowBtn.place(x=112,y=56,width=75,height=25)
    Label4 = Label(window, text="Добавить запись:")
    Label4.place(x=80,y=184,width=95,height=13)
    DateEdt = Entry(window)
    DateEdt.place(x=136,y=224,width=120,height=21)
    Label5 = Label(window, text="Дата:")
    Label5.place(x=136,y=208,width=32,height=13)
    Label6 = Label(window, text="Категория:")
    Label6.place(x=8,y=208,width=64,height=13)
    ListBox1 = Listbox(window)
    ListBox1.place(x=8,y=224,width=121,height=97)
    Label7 = Label(window, text="Сумма:")
    Label7.place(x=136,y=296,width=45,height=13)
    PriceEdt = Entry(window)
    PriceEdt.place(x=136,y=314,width=121,height=21)

    Label10 = Label(window, text="Название:")
    Label10.place(x=136,y=256,width=55,height=13)
    NameEdt = Entry(window)
    NameEdt.place(x=136,y=272,width=121,height=21)
    
    AddBtn = Button(window, text="Добавить", command=AddBtn_Click)
    AddBtn.place(x=8,y=328,width=75,height=25)
    StatBtn = Button(window, text="Статистика", command=StatBtn_Click)
    StatBtn.place(x=328,y=16,width=75,height=25)
    PriceMonthLbl = Label(window, text="Потрачено за - месяц: 0 руб.")
    PriceMonthLbl.place(x=280,y=46,width=200,height=13)
    Label8 = Label(window, text="Потрачено за ---- год: 0 руб.")
    Label8.place(x=280,y=66,width=200,height=13)

    Label9 = Label(window, text="---------------")
    Label9.place(x=280,y=200,width=180,height=46)
    
    #ListBox1.delete(0, END)
    ListBox1.insert(END, "Канцтовары\n")
    ListBox1.insert(END, "Оргтехника\n")
    ListBox1.insert(END, "Обслуживание\n")
    ListBox1.insert(END, "Аренда\n")
    ListBox1.insert(END, "Электроэнергия\n")
    ListBox1.insert(END, "Заработ. плата\n")

    YearEdt.delete(0, 'end')
    YearEdt.insert(END, '2022')
    MonthEdt.delete(0, 'end')
    MonthEdt.insert(END, '12')
    
    ShowBtn_Click()
    StatBtn_Click()

    window.mainloop()

main()

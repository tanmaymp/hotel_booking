import pymysql
import tkinter as tk
from tkinter import messagebox as mbox
from tkinter import *
LARGE_FONT = ("Verdana", 12)


class HBS(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		container = tk.Frame(self)
		
		container.pack(side="top", fill="both", expand=True)
		
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		
		for F in (StartPage, Loginpage, Loggedin, SignUp, Admin):
		
			frame= F(container, self)
			
			self.frames[F] = frame
			
			frame.grid(row=0, column=0, sticky="nsew")
			
		self.show_frame(StartPage)
		
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
		
class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text="BOOK YOUR ROOM",font = LARGE_FONT, fg="White", bg="Maroon")
		label.pack(pady=10,padx=10, fill=X)
		
		Button1 = tk.Button(self,text="Enter",command= lambda: controller.show_frame(Loginpage))
		Button1.pack(padx=10, pady=10)
		
class Loginpage(tk.Frame):
			

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		
		def Login():
			conn=pymysql.connect(host='<server>',user='<username>',password='<password>',db='<dbname>')
			c=conn.cursor()
			
			usr = e1.get()
			addusr = 'insert into demo(username)values(%s)'
			c.execute(addusr,usr)
			conn.commit()
			passw = e2.get()
			if usr == 'admin' and passw == 'admin':controller.show_frame(Admin)
			else:
				sql = 'Select * from User where Password like %s'
				c.execute(sql,passw)
				data = c.fetchone()
				
				if not data:print('Error')
				
				elif passw == str(data[2]):controller.show_frame(Loggedin)
				else:print('Error')	
			
			
		label = tk.Label(self,text="LOGIN",font = LARGE_FONT, fg="White", bg="Maroon")
		label.grid(row=0)
		
		labelt = tk.Label(self,text="CHOOSE YOUR ROOM",fg="white",bg="purple",pady=10)
		label = tk.Label(self,text="Username",font = LARGE_FONT)
		label.grid(row=1, column=1)
		e1 = tk.Entry(self)
		e1.grid(row=1, column=2)
		
		label = tk.Label(self,text="Password",font = LARGE_FONT)
		label.grid(row=2, column=1)
		e2 = tk.Entry(self)
		e2.grid(row=2, column=2)
		
		label = tk.Label(self,text="",font = LARGE_FONT)
		label.grid(row=3, column=1)
		
		Loginb = tk.Button(self,text="LOGIN",command = Login)
		Loginb.grid(columnspan=4)
		
		label = tk.Label(self,text="",font = LARGE_FONT)
		label.grid(row=5, column=1)
		
		Signup = tk.Button(self,text="SIGN UP",command = lambda:controller.show_frame(SignUp))
		Signup.grid(columnspan=4)
		
class Loggedin(tk.Frame):
		
			

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		
		def Book():
			ch = str(drop1.get())
			if ch == 'Choose room':flag = 2
			ch1 = str(drop2.get())
			if ch1 == 'Choose room':flag = 1
			if flag == 1:
				
				getusr = 'select * from demo'
				c.execute(getusr)
				getu = c.fetchone()
				usr = str(getu[0])
				print(usr)
				uu = (usr,ch)
				sql='update rooms SET bookstatus="1",customer = %s where type = %s'
				c.execute(sql,uu) 
				print('yes')
				conn.commit()
				drop1.set('Choose room')
				mbox.showinfo("BOOKED")
				controller.show_frame(Loggedin)
	
			elif flag == 2:
				getusr = 'select * from demo'
				c.execute(getusr)
				getu = c.fetchone()
				usr = str(getu[0])
				print(usr)
				uu = (usr,ch1)
				sql='update roomsac SET bookstatusA= "1",customer = %s where typeA = %s'
				c.execute(sql,uu) 
				print('yes')
				conn.commit()
				drop2.set('Choose room')
				mbox.showinfo("BOOKED")
				controller.show_frame(Loggedin)
		
			else:mbox.showinfo("Choose")
			conn.commit()
			
		def logout():
			conn=pymysql.connect(host='<server>',user='<username>',password='<password>',db='<dbname>')
			c=conn.cursor()
			des = 'truncate table demo'
			c.execute(des)
			conn.commit()
			controller.show_frame(Loginpage)
			
		conn=pymysql.connect(host='<server>',user='<username>',password='<password>',db='<dbname>')
		c=conn.cursor()
		
		label = tk.Label(self,text="Choose your room",font = LARGE_FONT, bg="Maroon", fg="white")
		label.pack(fill=X)
		
		
		sqlr = 'Select * from Rooms where bookstatus = 0'
		c.execute(sqlr)
		d1 = c.fetchall()
		if not d1:OPTIONS=[rooms-full]
		else:
			OPTIONS = []
			for row in d1:
				OPTIONS.append(row[1])
			
			drop1 = StringVar(self)
			drop1.set('Choose room')
		
		
		lbl = tk.Label(self,text="Normal Room").pack(padx=10, pady=10)
		
		w = OptionMenu(self, drop1, *OPTIONS)
		w.pack(padx=10, pady=10)
		
		lbl2 = tk.Label(self,text="AC Room").pack(padx=10, pady=10)
		
		sqlra = 'Select * from Roomsac where bookstatusA = 0'
		c.execute(sqlra)
		d2 = c.fetchall()
		OPTIONS = []
		for row in d2:
			OPTIONS.append(row[1]) 
		
		drop2 = StringVar(self)
		drop2.set('Choose room')
		
		w = OptionMenu(self, drop2, *OPTIONS)
		w.pack(padx=10, pady=10)
			
		but = tk.Button(self, text="BOOK", command=Book).pack(padx=20, pady=20)
		but2 = tk.Button(self, text="Logout", command=logout).pack(padx=20, pady=20)
		
class SignUp(tk.Frame):
			

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		
		def register():
			conn=pymysql.connect(host='<server>',user='<username>',password='<password>',db='<dbname>')
			c=conn.cursor()
			
			nm = sn.get()
			unm = sun.get()
			pw = sp.get()
			
			if not nm:mbox.showerror("enter name")
			userdata=(nm,unm,pw)
			sql1 = 'select * from user where Username like %s'
			c.execute(sql1,unm)
			d = c.fetchone()
			if not d :
				sql='Insert into User (Name,Username,Password)values(%s,%s,%s)'
				c.execute(sql,userdata)
				controller.show_frame(Loginpage)
			else:mbox.showerror('username exists already')
			conn.commit()
		
		label = tk.Label(self,text="Name",font = LARGE_FONT)
		label.grid(row=0)
		label = tk.Label(self,text="username",font = LARGE_FONT)
		label.grid(row=1)
		label = tk.Label(self,text="Password",font = LARGE_FONT)
		label.grid(row=2)
		
		sn = tk.Entry(self)
		sn.grid(row=0,column=1)
		
		sun = tk.Entry(self)
		sun.grid(row=1,column=1)
		
		sp = tk.Entry(self)
		sp.grid(row=2,column=1)
		
		Reg = tk.Button(self,text="register",command = register)
		Reg.grid(columnspan=2)
		
class Admin(tk.Frame):
			

	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		
		conn=pymysql.connect(host='<server>',user='<username>',password='<password>',db='<dbname>')
		c=conn.cursor()
		
		def adminout():
			des = 'truncate table demo'
			c.execute(des)
			conn.commit()
			controller.show_frame(Loginpage)
		
		def restart():
			res1 = 'update rooms set bookstatus="0", customer=""'
			res2 = 'update roomsac set bookstatusA="0", customer=""'
			c.execute(res1)
			c.execute(res2)
			conn.commit()
			
		def ret():
			dis = 'Select * from rooms'
			diss = 'Select * from roomsac'
			c.execute(dis)
			d1 = c.fetchall()
			lbl = tk.Label(self,text="nonac rooms allotment").grid(row=0)
			lbl = tk.Label(self,text="roomid").grid(row=1, column=0)
			lbl = tk.Label(self,text="roomtype").grid(row=1, column=1)
			lbl = tk.Label(self,text="customer").grid(row=1, column=2)
			m=2
			for row in d1:
				
				lbl = tk.Label(self,text=row[0]).grid(row=m,column=0)
				lbl = tk.Label(self,text=row[1]).grid(row=m,column=1)
				lbl = tk.Label(self,text=row[3]).grid(row=m,column=2)
				m=m+1
			
			c.execute(diss)
			d2 = c.fetchall()
			lbl = tk.Label(self,text="").grid(row=m)
			
			lbl = tk.Label(self,text="roomid").grid(row=m+1, column=0)
			lbl = tk.Label(self,text="roomtype").grid(row=m+1, column=1)
			lbl = tk.Label(self,text="customer").grid(row=m+1, column=2)
			k=m+2
			for row in d2:
				
				lbl = tk.Label(self,text=row[0]).grid(row=k,column=0)
				lbl = tk.Label(self,text=row[1]).grid(row=k,column=1)
				lbl = tk.Label(self,text=row[3]).grid(row=k,column=2)
				k=k+1
			conn.commit()
		
		ret()
		
		res = tk.Button(self,text="reset",command=restart).grid(columnspan=2)
		out = tk.Button(self,text="Logout",command=adminout).grid(columnspan=2)

	
app = HBS()
app.mainloop()
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile

class billClass:
    def __init__(self,parent):
        self.parent=parent
        self.parent.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        
        #product frame
        

        ProductFrame1=Frame(self.parent,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=0,width=410,height=550)

        pTitle=Label(ProductFrame1,text="Productos",font=("goudy old style",15,"bold"),bg="#13278f",fg="white")
        pTitle.pack(side=TOP,fill=X)

        #Peoduct Search Frame
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=4,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Buscar Producto | Por Nombre",font=("goudy old style",15,"bold"),bg="white",fg="#13278f").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text="Nombre Producto",font=("goudy old style",15,"bold"),bg="white",fg="#13278f").place(x=5,y=45) 
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("goudy old style",15),bg="#FAEDEA").place(x=130,y=47,width=150,height=22) 
        btn_search=Button(ProductFrame2,text="Buscar",command=self.search,font=("goudy old style",15,"bold"),bg="white",fg="#13278f",cursor="hand2").place(x=285,y=45,width=95,height=25)
        btn_show_all=Button(ProductFrame2,text="Mostrar todos",command=self.show,font=("goudy old style",15,"bold"),bg="white",fg="#13278f",cursor="hand2").place(x=285,y=5,width=95,height=25)

  
        #Product Details
        
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=385)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
       

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","itemname","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview) #horizontal scrollbar
        scrolly.config(command=self.product_Table.yview) #vertical scrollbar

        self.product_Table.heading("pid",text="PID No.")
        self.product_Table.heading("itemname",text="Nombre")
        self.product_Table.heading("price",text="Precio")
        self.product_Table.heading("qty",text="Cantidad")

        
        
        #Tamaño de las columnas
        self.product_Table["show"]="headings"

        self.product_Table.column("pid",width=40)
        self.product_Table.column("itemname",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=40)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        #self.show()

        lbl_note=Label(ProductFrame1,text="Nota : Pon 0 para eliminar el producto del carrito",font=("goudy old style",11),anchor='w',bg="white",fg="red")
        lbl_note.pack(side=BOTTOM,fill=X)

###Customer Frame
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.parent,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=0,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Detalles Cliente",font=("goudy old style",15,"bold"),bg="#13278f",fg="white")
        cTitle.pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Nombre",font=("goudy old style",15,"bold"),bg="white",fg="#13278f").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("goudy old style",15),bg="#FAEDEA").place(x=80,y=35,width=180) 

        lbl_contact=Label(CustomerFrame,text="Telefono",font=("goudy old style",15,"bold"),bg="white",fg="#13278f").place(x=280,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("goudy old style",13),bg="#FAEDEA").place(x=360,y=35,width=140) 
        
        #cal cart frame
        Cal_cartFrame=Frame(self.parent,bd=4,relief=RIDGE,bg="white")
        Cal_cartFrame.place(x=420,y=80,width=530,height=330)
        
        #cal frame
        self.var_cal_input=StringVar()
        CalFrame=Frame(Cal_cartFrame,bd=9,relief=RIDGE,bg="white")
        CalFrame.place(x=5,y=10,width=268,height=300)

        txt_cal_input=Entry(CalFrame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,state='readonly',justify=RIGHT,relief=GROOVE)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(CalFrame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=0)
        btn_8=Button(CalFrame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=1)
        btn_9=Button(CalFrame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=2)
        btn_sum=Button(CalFrame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=3)


        btn_4=Button(CalFrame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=0)
        btn_5=Button(CalFrame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=1)
        btn_6=Button(CalFrame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=2)
        btn_sub=Button(CalFrame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=3)

        btn_1=Button(CalFrame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=0)
        btn_2=Button(CalFrame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=1)
        btn_3=Button(CalFrame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=2)
        btn_mul=Button(CalFrame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=3)

        btn_0=Button(CalFrame,text='0',font=('arial',14,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=9,cursor='hand2').grid(row=4,column=0)
        btn_c=Button(CalFrame,text='c',font=('arial',14,'bold'),command=lambda:self.clear_cal(),bd=5,width=4,pady=9,cursor='hand2').grid(row=4,column=1)
        btn_eq=Button(CalFrame,text='=',font=('arial',14,'bold'),command=lambda:self.perform_cal(),bd=5,width=4,pady=9,cursor='hand2').grid(row=4,column=2)
        btn_div=Button(CalFrame,text='/',font=('arial',14,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=9,cursor='hand2').grid(row=4,column=3)








         #cart frame

        CartFrame=Frame(Cal_cartFrame,bd=3,relief=RIDGE)
        CartFrame.place(x=280,y=2,width=245,height=300)
        self.cartTitle=Label(CartFrame,text="Carrito \t Productos Totales: [0]",font=("goudy old style",13,"bold"),bg="#13278f",fg="white")
        self.cartTitle.pack(side=TOP,fill=X)


        scrolly=Scrollbar(CartFrame,orient=VERTICAL)
        scrollx=Scrollbar(CartFrame,orient=HORIZONTAL)
       

        self.cartTable=ttk.Treeview(CartFrame,columns=("pid","itemname","price","qty","discount"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTable.xview) #horizontal scrollbar
        scrolly.config(command=self.cartTable.yview) #vertical scrollbar

        self.cartTable.heading("pid",text="PID No.")
        self.cartTable.heading("itemname",text="Nombre")
        self.cartTable.heading("price",text="Precio")
        self.cartTable.heading("qty",text="Cantidad")
        self.cartTable.heading("discount",text="Discount")
    
        

        self.cartTable["show"]="headings"

        self.cartTable.column("pid",width=30)
        self.cartTable.column("itemname",width=100)
        self.cartTable.column("price",width=90)
        self.cartTable.column("qty",width=30)
        self.cartTable.column("discount",width=100)
       
        self.cartTable.pack(fill=BOTH,expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        #self.show()


        #add cart widgets frame 
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        self.var_discount=StringVar()

        Add_cartwidgetsFrame=Frame(self.parent,bd=4,relief=RIDGE,bg="white")
        Add_cartwidgetsFrame.place(x=420,y=400,width=530,height=110)

        lbl_pname=Label(Add_cartwidgetsFrame,text="Nombre Producto",font=("goudy old style",13,"bold"),bg="white",fg="#13278f").place(x=5,y=5)
        txt_pname=Entry(Add_cartwidgetsFrame,textvariable=self.var_pname,font=("goudy old style",12),bg="#FAEDEA",state='readonly').place(x=5,y=30,width=190,height=22)

        lbl_p_price=Label(Add_cartwidgetsFrame,text="Precio por cantidad ",font=("goudy old style",13,"bold"),bg="white",fg="#13278f").place(x=230,y=5)
        txt_p_price=Entry(Add_cartwidgetsFrame,textvariable=self.var_price,font=("goudy old style",12),bg="#FAEDEA",state='readonly').place(x=230,y=30,width=150,height=22)

        lbl_p_qty=Label(Add_cartwidgetsFrame,text="Cantidad",font=("goudy old style",13,"bold"),bg="white",fg="#13278f").place(x=390,y=5)
        txt_p_qty=Entry(Add_cartwidgetsFrame,textvariable=self.var_qty,font=("goudy old style",12),bg="#FAEDEA").place(x=390,y=30,width=120,height=20)

        # self.lbl_inStock=Label(Add_cartwidgetsFrame,text="In Stock",font=("goudy old style",10,"bold"),bg="white",fg="#13278f").place(x=5,y=64)
        
        btn_clear_cart=Button(Add_cartwidgetsFrame,text="Limpiar",command=self.clear_cart,font=("goudy old style",10,"bold"),bg="#13278f",fg="white",cursor="hand2").place(x=180,y=70,width=150,height=30)
        
        btn_add_cart=Button(Add_cartwidgetsFrame,text="Añadir | Modificar Carrito",command=self.add_update_cart,font=("goudy old style",10,"bold"),bg="#13278f",fg="white",cursor="hand2").place(x=340,y=70,width=180,height=30)




    #-----------------------------billing area-----


        billFrame=Frame(self.parent,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=0,width=410,height=410)


        btitle=Label(billFrame,text="Boletas",font=("goudy old style",15,"bold"),bg="#13278f",fg="white")
        btitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

    #-------------------billing buttons

        billMenuFrame=Frame(self.parent,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=370,width=410,height=140)

        # self.lbl_amnt=Label(billMenuFrame,text='Bill Amount\n[0]',font=("goudy old style",15,"bold"),bg="#13278f",fg="white")
        # self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        # self.lbl_discount=Label(billMenuFrame,text='Discount\n[5%]',font=("goudy old style",15,"bold"),bg="#13278f",fg="white")
        # self.lbl_discount.place(x=124,y=5,width=120,height=70)

        # self.lbl_netpay=Label(billMenuFrame,text='Net Pay\n[0]',font=("goudy old style",15,"bold"),bg="#13278f",fg="white")
        # self.lbl_netpay.place(x=246,y=5,width=160,height=70)


        btn_generate_bill=Button(billMenuFrame,text='Generar/Guardar Boleta',command=self.generate_bill,font=("goudy old style",15,"bold"),bg="#13278f",fg="white",cursor="hand2")
        btn_generate_bill.place(x=2,y=5,width=200,height=70)

        btn_clear_all=Button(billMenuFrame,text='Limpiar',command=self.clear_all,font=("goudy old style",15,"bold"),bg="#13278f",fg="white",cursor="hand2")
        btn_clear_all.place(x=230,y=5,width=160,height=70)

        btn_print=Button(billMenuFrame,text='Imprimir boleta',command=self.print_bill,font=("goudy old style",12,"bold"),bg="#13278f",fg="white",cursor="hand2")
        btn_print.place(x=150,y=80,width=120,height=70)

        self.show()
        
        #functions

    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set(' ')


    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))


    def show(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            cur.execute("Select pid,itemname,price,qty from stock")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)} ",parent=self.parent)  

    def search(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search Input should be required",parent=self.parent)
            else:
                cur.execute("select pid,itemname,price,qty from stock where itemname LIKE '%"+self.var_search.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.parent)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)} ",parent=self.parent)  

    def get_data(self, ev):
        f = self.product_Table.focus()
        content = (self.product_Table.item(f))
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_stock.set(row[3])
            self.var_qty.set('1')
        else:
            messagebox.showerror("Error", "No se pudo obtener los datos del producto", parent=self.parent)
    
    def get_data_cart(self, ev):
        f = self.cartTable.focus()
        content = (self.cartTable.item(f))
        row = content['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])
            self.var_stock.set(row[3])
        else:
            messagebox.showerror("Error", "No se pudo obtener los datos del carrito", parent=self.parent)
        
    
    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Error', "Selecciona un producto de la lista", parent=self.parent)
        elif self.var_qty.get() == '':
            messagebox.showerror('Error', "Cantidad necesario", parent=self.parent)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Error', "Cantidad Invalida", parent=self.parent)
        else:
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get()]

            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1
            if present == 'yes':
                op = messagebox.askyesno('Confirmado', "Producto ya presente\nQuieres modificar/eliminar el producto de la lista?", parent=self.parent)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()
            self.show()  # Actualiza la tabla de productos


    def bill_updates(self):
        self.total_sales = 0
        self.actualprice = 0
        self.total_sales = 0
        self.total_invoice_amount = 0
        self.total_sgst = 0
        self.total_cgst = 0
        self.total_gst = 0

        for row in self.cart_list:
            if row[2] is not None and row[3] is not None:
                try:
                    self.actualprice += float(row[2]) * int(row[3])
                except ValueError:
                    messagebox.showerror("Error", "Error al convertir valores a float", parent=self.parent)
                    return
            try:
                self.total_sales += float(row[2]) * int(row[3])
            except ValueError:
                messagebox.showerror("Error", "Error al convertir valores a float", parent=self.parent)
                return

        self.total_sgst = self.total_sales * 0.09
        self.total_cgst = self.total_sales * 0.09
        self.total_gst = self.total_sgst + self.total_cgst
        self.total_invoice_amount = self.total_sales + self.total_gst

        print(str(self.total_sales))
        print(str(self.total_invoice_amount))

        self.cartTitle.config(text=f"Cart \t Total Products: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
               self.cartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)} ",parent=self.parent)  

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror('Error', "Customer Details are required", parent=self.parent)
        elif len(self.cart_list) == 0:
            messagebox.showerror('Error', "Please Add product to the cart", parent=self.parent)
        else:
            #-----Bill top---#
            self.bill_top()
            #-----Bill Middle--#
            self.bill_middle()
            #----Bill Bottom--#
            self.bill_bottom()
            #

            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been generated/Saved in backend", parent=self.parent)
            self.chk_print = 1
            self.show()  # Actualiza la tabla de productos
            self.show_cart()  # Actualiza la tabla del carrito


    
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tPlamparambil Power Tools
\n\t\tPazhavangadi P.O. Ranni
\t\tPhone No. 8075534104 
\t\tEmail:abrahamj4877@gmail.com

{str("="*47)}
Customer Name: {self.var_cname.get()}
Ph no: {self.var_contact.get()}
Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
Product Name\t\t\tHSN Code\tQTY\t\tPrice\tDiscount
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)


    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Total Sales(A)\t\t\t\tRs.{self.total_sales}
Total sgst(9%)\t\t\t\tRs.{self.total_sgst}
Total cgst(9%)\t\t\t\tRs.{self.total_cgst}
Total gst(18%)(B)\t\t\t\tRs.{self.total_gst}
Total Invoice Amount(A+B)\t\t\tRs.{self.total_invoice_amount} 
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'tbs.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[3])
                try:
                    price=float(row[2])*qty
                except ValueError:
                    messagebox.showerror("Error", "Error al convertir valores a float", parent=self.parent)
                    return
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[2]+"\t"+str(qty)+"\tRs."+price)
                #update qty in stock
                cur.execute('UPDATE stock SET qty = qty - ? WHERE pid = ?', (qty, pid))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)} ",parent=self.parent) 



    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        # self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')
        self.var_discount.set('')
    
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Products: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()  # Actualiza la tabla de productos
        self.show_cart()  # Actualiza la tabla del carrito
        self.chk_print = 0

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.parent)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showinfo('Print',"Please generate bill, to print the receipt",parent=self.parent)

    def logout(self):
        self.parent.destroy()
        os.system("python login.py")
            

if  __name__=="__main__":
    root=Tk()
    obj=billClass(root)
    root.mainloop()
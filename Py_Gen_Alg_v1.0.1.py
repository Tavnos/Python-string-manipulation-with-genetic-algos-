import tkinter as tk
import numpy as np
import random as rd


class Main_Varriables:
    i_pop, i_req, i_pat = 10000, 1, 'S0m37h1ng R4nd0m'
    c_ls, v_dc  = [], {}
    var_id = ('sv_t_pat', 'sv_t_pat_len', 'sv_t_pop', 'sv_t_req')
    def get_main_var(self):
        for i in self.var_id:
            self.v_dc[i] = tk.StringVar()
    def get_unicodes(self, u_amount, u_start_range):
        rd_ls = []
        for i in range(u_amount):
            rd_ls += [(chr(u_start_range+i))]
        return rd_ls
    def select_char(self, num_c=True, upper_c=True, lower_c=True):
        self.dna_char = [' ']
        if num_c  == True:
            self.dna_char += self.get_unicodes(10,48)
        if upper_c == True:
            self.dna_char += self.get_unicodes(26,65)
        if lower_c == True:
            self.dna_char += self.get_unicodes(26,97)
            
class Init_Methods:
    def reset_pool(self):    
        self.get_tk_var()
        self.hot_pool = self.get_custom()
    def add_pool(self):
        self.get_tk_var()
        self.hot_pool += self.get_custom()
    def add_req(self):
        next_pool = []
        self.i_req = str(int(self.i_req) + 1)
        self.v_dc['sv_t_req'].set(self.i_req)
        for i in self.hot_pool:
            if self.get_score(i) >= int(self.v_dc['sv_t_req'].get()):
                next_pool += [i]
        self.hot_pool = next_pool
    def get_stat(self):
        self.clear_display()
        self.hot_foo = self.get_score_str(self.hot_pool)
        self.hot_foo.sort()
        self.v_dc['t_display'].insert(float(), '\n')
        for i in (self.hot_foo):
            self.v_dc['t_display'].insert(float(), 
                                          'Score:'+ str(i[0]) + '/' + str(self.v_dc['sv_t_pat_len'].get()) +
                                          ' ,   in pct:'+
                                          str(round(((int(i[0])/int(self.v_dc['sv_t_pat_len'].get()))*100), 2)) + 
                                          '% \n Word:(' + ''.join(i[1])  + ') \n')
        self.basic_stat()
    def basic_stat(self):
        self.v_dc['t_display'].insert(float(), ('Population size: ' + str(len(self.hot_pool)) + ' \n'))
        self.v_dc['t_display'].insert(float(), ('Average pool fit: ' + str(self.get_average_fit(self.hot_pool)) + 
                                                ' / '              + str(self.v_dc['sv_t_pat_len'].get())   +' \n'))
        self.v_dc['t_display'].insert(float(), ('Total average in percentile:'+ 
                                      str(round(100*int(self.get_average_fit(self.hot_pool))/
                                                int(self.v_dc['sv_t_pat_len'].get()),2))) + '% ' + ' \n')
    def get_shuffle(self): 
        rd.shuffle(self.hot_pool)
class Base_Methods:    
    def get_anything(self):
        h_ls, t_len = [], len(self.i_pat)
        for i in range(t_len):
            h_ls+=rd.choices(self.dna_char)
        return h_ls  
    def get_custom(self):
        g_i, p_l =  0, []
        for i in range(int(self.i_pop)):
            while g_i < int(self.i_req):
                h_g = self.get_anything()
                g_i = self.get_score(h_g)
                if g_i >= int(self.i_req):
                    p_l+=[h_g]
            g_i = 0
        self.hot_pool = p_l
        return self.hot_pool 
    def get_average_fit(self, pool_array):
        h_arr = self.get_score_str(pool_array)
        p_ls = [(i[0]) for i in h_arr]
        return np.average(p_ls)
    def get_score(self, pool_str):
        score_int = 0
        for i in range(len(self.i_pat)):
            if (self.i_pat[i] == pool_str[i]):
                score_int += 1
        return score_int  
    def get_score_str(self, pool_array):
        h_ls = [(self.get_score(i), i) for i in pool_array]
        return h_ls

class Advanced_Methods:
    def do_slice(self, input_tgt):
        s_first = input_tgt[0:int(len(input_tgt)/2)]
        s_second = input_tgt[int(len(input_tgt)/2)::]
        return (s_first, s_second)
    def get_slice(self):
        print('get_slice')
        evo_pool = [self.do_slice(self.hot_pool[::-1][0])[0] + self.do_slice(self.hot_pool[0])[1]]
        for i in range(len(self.hot_pool)-1):
            evo_pool += [self.do_slice(self.hot_pool[i])[0] + self.do_slice(self.hot_pool[i+1])[1]]
        self.hot_pool = evo_pool
    def get_radiate(self):
        print('get_radiate')
        for i in range(len(self.hot_pool)):
            self.hot_pool[i][rd.randrange(0,int(self.v_dc['sv_t_pat_len'].get()))] = ''.join(rd.choices(self.dna_char))
    def do_shatter(self, input_tgt):
        s_first = input_tgt[0:int(len(input_tgt)/2)]
        s_second =  input_tgt[int(len(input_tgt)/2)::]
        s_first_c =  s_first[0:int(len(s_first)/2)]   , s_first[int(len(s_first)/2)::]
        s_second_c = s_second[0:int(len(s_second)/2)], s_second[int(len(s_second)/2)::]
        return s_first_c+ s_second_c
    def get_shatter(self):
        print('get_shatter')
        evo_pool = [(rd.choices([[self.do_shatter(self.hot_pool[::-1][0])[0]],
                                  [self.do_shatter(self.hot_pool[0])[0]]])[0])+
                    (rd.choices([[self.do_shatter(self.hot_pool[::-1][0])[1]],
                                 [self.do_shatter(self.hot_pool[0])[1]]])[0])+
                    (rd.choices([[self.do_shatter(self.hot_pool[::-1][0])[2]],
                                 [self.do_shatter(self.hot_pool[0])[2]]])[0])+
                    (rd.choices([[self.do_shatter(self.hot_pool[::-1][0])[3]],
                                 [self.do_shatter(self.hot_pool[0])[3]]])[0])]
        for i in range(len(self.hot_pool)-1):
            evo_pool += [((rd.choices([[self.do_shatter(self.hot_pool[i])[0]],
                                      [self.do_shatter(self.hot_pool[i+1])[0]]])[0])+
                         (rd.choices([[self.do_shatter(self.hot_pool[i])[1]],
                                      [self.do_shatter(self.hot_pool[i+1])[1]]])[0])+
                         (rd.choices([[self.do_shatter(self.hot_pool[i])[2]],
                                      [self.do_shatter(self.hot_pool[i+1])[2]]])[0])+
                         (rd.choices([[self.do_shatter(self.hot_pool[i])[3]],
                                      [self.do_shatter(self.hot_pool[i+1])[3]]])[0]))]
        st_hp = []
        for i in evo_pool:
            vt_hp = []
            for f in i:
                vt_hp += f
            st_hp += [vt_hp]
        self.hot_pool =  st_hp
    def get_double(self):
        print('get_double')
        self.hot_pool += self.hot_pool
    def get_halve(self):
        print('get_halve')
        self.hot_foo = self.get_score_str(self.hot_pool)
        self.hot_foo.sort()
        hot_slice = self.hot_foo[::-1][0:int(len(self.hot_foo)/2)]
        hot_slush = [(i[1]) for i in hot_slice]
        self.hot_pool = hot_slush
    def propagate(self):
        for i in range(1):
            self.get_halve()
            self.three_s()
        for i in range(1):
            self.get_double()
            self.three_s()
    def get_cycle(self):
        print('get_cycle')
        self.get_double()
        for i in range(2):
            self.propagate()
        self.get_stat()
    def three_s(self):
        for i in range(3):
            self.get_slice()
            self.get_shuffle()
            self.get_shatter()
            self.get_shuffle()
class Display_Objects:
    def get_interface(self):
        self.v_dc['lbl_set_btn'] = tk.Label(width=12, text='Start or restart')
        self.v_dc['lbl_set_btn'].grid(column=1,row=1)
        self.v_dc['lbl_pat_str'] = tk.Label(width=20, text='Pattern to match')
        self.v_dc['lbl_pat_str'].grid(column=2,row=1)
        self.v_dc['lbl_new_pool'] = tk.Label(width=12, text='Add population')
        self.v_dc['lbl_new_pool'].grid(column=3,row=1)
        self.v_dc['btn_reset_pop'] = tk.Button(self, text='Reset (-)', command=self.reset_pool)
        self.v_dc['btn_reset_pop'].grid(column=1,row=2)   
        self.v_dc['in_pat_str'] = tk.Entry(width=30, textvariable=self.v_dc['sv_t_pat'])
        self.v_dc['in_pat_str'].grid(column=2,row=2)
        self.v_dc['btn_add_pop'] = tk.Button(self, text='Add (+)', command=self.add_pool)
        self.v_dc['btn_add_pop'].grid(column=3,row=2)    
        self.v_dc['lbl_pat_len'] = tk.Label(width=10, text='Length')
        self.v_dc['lbl_pat_len'].grid(column=1,row=3)
        self.v_dc['lbl_pat_pop'] = tk.Label(width=10, text='Population')
        self.v_dc['lbl_pat_pop'].grid(column=2,row=3)
        self.v_dc['lbl_pat_req'] = tk.Label(width=10, text='Fit')
        self.v_dc['lbl_pat_req'].grid(column=3,row=3)
        self.v_dc['lbl_in_len'] = tk.Label(width=10, textvariable=self.v_dc['sv_t_pat_len'])
        self.v_dc['lbl_in_len'].grid(column=1,row=4)
        self.v_dc['in_pat_pop'] = tk.Entry(width=10, textvariable=self.v_dc['sv_t_pop'])
        self.v_dc['in_pat_pop'].grid(column=2,row=4)
        self.v_dc['in_pat_req'] = tk.Entry(width=5, textvariable=self.v_dc['sv_t_req'])
        self.v_dc['in_pat_req'].grid(column=3,row=4)
        self.v_dc['btn_get_stat'] = tk.Button(self, text='Stat (.)', command=self.get_stat)
        self.v_dc['btn_get_stat'].grid(column=1,row=5)
        self.v_dc['btn_get_size'] = tk.Button(self, text='Shuffle (,)', command=self.get_shuffle)
        self.v_dc['btn_get_size'].grid(column=2,row=5)
        self.v_dc['btn_get_step'] = tk.Button(self, text="Fit (')", command=self.add_req)
        self.v_dc['btn_get_step'].grid(column=3,row=5)
        self.v_dc['btn_get_slice'] = tk.Button(self, text='Slice (/)', command=self.get_slice)
        self.v_dc['btn_get_slice'].grid(column=1,row=6)
        self.v_dc['btn_get_shatter'] = tk.Button(self, text='Shatter (*)', command=self.get_shatter)
        self.v_dc['btn_get_shatter'].grid(column=2,row=6)
        self.v_dc['btn_get_radiate'] = tk.Button(self, text='Radiate (<)', command=self.get_radiate)
        self.v_dc['btn_get_radiate'].grid(column=3,row=6)
        self.v_dc['btn_get_double'] = tk.Button(self, text='Double (ø)', command=self.get_double)
        self.v_dc['btn_get_double'].grid(column=1,row=7)
        self.v_dc['btn_get_halve'] = tk.Button(self, text='Halve (æ)', command=self.get_halve)
        self.v_dc['btn_get_halve'].grid(column=2,row=7)
        self.v_dc['btn_get_cycle'] = tk.Button(self, text='Cycle (å)', command=self.get_cycle)
        self.v_dc['btn_get_cycle'].grid(column=3,row=7)
        self.v_dc['t_display'] = tk.Text(self, wrap="char", width=46, font=("Helvetica", 14))
        self.v_dc['t_display'].grid(column=1,row=8, columnspan=3)
    def clear_display(self):
        self.v_dc['t_display'].delete(1.0, tk.END)  
    def set_tk_var(self):                
        self.v_dc['sv_t_pat'].set(self.i_pat)
        self.v_dc['sv_t_pat_len'].set(len(self.i_pat))
        self.v_dc['sv_t_pop'].set(self.i_pop)
        self.v_dc['sv_t_req'].set(self.i_req)
    def get_tk_var(self):                
        self.i_pat = self.v_dc['sv_t_pat'].get()
        self.v_dc['sv_t_pat_len'].set(len(self.i_pat))
        self.i_pop = self.v_dc['sv_t_pop'].get()
        self.i_req = self.v_dc['sv_t_req'].get()

class Tk_Main(tk.Tk, Main_Varriables, Init_Methods, Base_Methods, Advanced_Methods, Display_Objects):
    def __init__(self):
        super().__init__()
        self.title("Simple GUI for quick gen algo exec")
        self.geometry("500x700")
        self.bind("<Key>", self.key_pressed)
        self.get_main_var()
        self.select_char()
        self.get_interface()
        self.set_tk_var()    
    def key_pressed(self, tk_command):
        if tk_command.char == "-":
            self.reset_pool() 
            self.get_stat() 
        elif tk_command.char == "+":
            self.add_pool() 
            self.get_stat() 
        elif tk_command.char == ".":
            self.get_stat() 
        elif tk_command.char == ",":
            self.get_shuffle() 
        elif tk_command.char == "'":
            self.add_req()
            self.get_stat() 
        elif tk_command.char == "/":
            self.get_slice()
            self.get_stat() 
        elif tk_command.char == "*":
            self.get_shatter()
            self.get_stat() 
        elif tk_command.char == "<":
            self.get_radiate()
            self.get_stat() 
        elif tk_command.char == "ø":
            self.get_double()
            self.get_stat() 
        elif tk_command.char == "æ":
            self.get_halve()
            self.get_stat() 
        elif tk_command.char == "å":
            self.get_cycle()
            self.get_stat() 

tk_init = Tk_Main()
tk_init.mainloop()
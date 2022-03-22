import tkinter as tk
import numpy as np
import random as rd


class Tk_Main(tk.Tk):
    def __init__(self, i_pat= 'S0m3 P4773rn', i_pop=2000, i_req=2, num_c=1, upper_c=1, lower_c=1):
        super().__init__()
        self.title("Simple GUI for quick gen algo exec")
        self.geometry("500x800")
        self.c_ls, self.v_dc, self.dna_char,  = [], {}, [' ']
        self.i_pat, self.i_pop, self.i_req, self.num_c, self.upper_c, self.lower_c = (i_pat, i_pop, i_req, num_c, upper_c, lower_c)
        var_id = ('sv_t_pat', 'sv_t_pat_len', 'sv_t_pop', 'sv_t_req')
        for i in var_id:
            self.v_dc[i] = tk.StringVar()
        if num_c  == True:
            self.dna_char += self.get_unicodes(10,48)
        if upper_c == True:
            self.dna_char += self.get_unicodes(26,65)
        if lower_c == True:
            self.dna_char += self.get_unicodes(26,97)
            
        self.set_tk_var()
        self.get_interface()
        
    def get_unicodes(self, u_amount, u_start_range):
        rd_ls = []
        for i in range(u_amount):
            rd_ls += [(chr(u_start_range+i))]
        return rd_ls
    
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
    
    def clear_display(self):
        self.v_dc['t_display'].delete(1.0, tk.END)  
        
    def get_anything(self):
        h_ls, t_len = [], len(self.i_pat)
        for i in range(t_len):
            h_ls+=rd.choices(self.dna_char)
        return h_ls  
    
    def get_custom(self):
        self.get_tk_var()
        self.clear_display()
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
  
        
    def reset_pool(self):
        self.clear_display()
        self.get_tk_var()
        self.hot_pool = self.get_custom()
        for i in self.hot_pool:
            self.v_dc['t_display'].insert(float(), (str(i) + ' \n'))
        self.basic_stat()
        
    def add_pool(self):
        self.get_tk_var()
        self.hot_pool += self.get_custom()
        self.clear_display()
        self.get_tk_var()
        for i in self.hot_pool:
            self.v_dc['t_display'].insert(float(), (str(i) + ' \n'))
        self.basic_stat()

    def get_score(self, pool_str):
        score_int = 0
        for i in range(len(self.i_pat)):
            if (self.i_pat[i] == pool_str[i]):
                score_int += 1
        return score_int  
    def get_score_str(self, pool_array):
        h_ls = [(self.get_score(i), i) for i in pool_array]
        return h_ls
    
    def get_average_fit(self, pool_array):
        h_arr = self.get_score_str(pool_array)
        p_ls = [(i[0]) for i in h_arr]
        return np.average(p_ls)
    
    def get_size(self): 
        self.clear_display()
        self.v_dc['t_display'].insert(float(), str(len(self.hot_pool)))
        self.get_stat()
    def basic_stat(self):
        self.v_dc['t_display'].insert(float(), ('Population size: ' + str(len(self.hot_pool)) + ' \n'))
        self.v_dc['t_display'].insert(float(), ('Average pool fit: ' + str(self.get_average_fit(self.hot_pool)) + 
                                                ' / '              + str(self.v_dc['sv_t_pat_len'].get())   +' \n'))
        self.v_dc['t_display'].insert(float(), ('in percentile: '+ 
                                      str(round(100*int(self.get_average_fit(self.hot_pool))/
                                                int(self.v_dc['sv_t_pat_len'].get()),2))) + '% ' + ' \n')
    def get_stat(self):
        self.clear_display()
        self.hot_foo = self.get_score_str(self.hot_pool)
        self.hot_foo.sort()
        for i in (self.hot_foo):
            self.v_dc['t_display'].insert(float(), 
                                          'Score:'+ str(i[0]) + '/' + str(self.v_dc['sv_t_pat_len'].get()) +
                                          ' in percentile:'+
                                          str(round(((int(i[0])/int(self.v_dc['sv_t_pat_len'].get()))*100), 2)) +
                                          '%  Word:(' + ''.join(i[1])  + ') \n')
        self.basic_stat()
    def add_req(self):
        self.clear_display()
        next_pool = []
        self.i_req = str(int(self.i_req) + 1)
        self.v_dc['sv_t_req'].set(self.i_req)
        self.clear_display()
        for i in self.hot_pool:
            if self.get_score(i) >= int(self.v_dc['sv_t_req'].get()):
                next_pool += [i]
        self.hot_pool = next_pool
        self.get_stat()

    def get_shatter(self):
        print('Coming Soon!')
    def get_radiate(self):
        print('Also coming soon, and more :D')
        
    def do_slice(self, input_tgt):
        s_first = input_tgt[0:int(len(input_tgt)/2)]
        s_second = input_tgt[int(len(input_tgt)/2)::]
        return (s_first, s_second)
    def get_slice(self):
        self.clear_display()
        evo_pool = [self.do_slice(self.hot_pool[::-1][0])[0] + self.do_slice(self.hot_pool[0])[1]]
        for i in range(len(self.hot_pool)-1):
            evo_pool += [self.do_slice(self.hot_pool[i])[0] + self.do_slice(self.hot_pool[i+1])[1]]
        self.hot_pool = evo_pool
        self.get_stat()
    def get_interface(self):
        self.v_dc['lbl_set_btn'] = tk.Label(width=12, text='Start or restart')
        self.v_dc['lbl_set_btn'].grid(column=1,row=1)
        self.v_dc['lbl_pat_str'] = tk.Label(width=20, text='Pattern to match')
        self.v_dc['lbl_pat_str'].grid(column=2,row=1)
        self.v_dc['lbl_new_pool'] = tk.Label(width=12, text='Add population')
        self.v_dc['lbl_new_pool'].grid(column=3,row=1)
        self.v_dc['btn_reset_pop'] = tk.Button(self, text='Reset', command=self.reset_pool)
        self.v_dc['btn_reset_pop'].grid(column=1,row=2)   
        self.v_dc['in_pat_str'] = tk.Entry(width=30, textvariable=self.v_dc['sv_t_pat'])
        self.v_dc['in_pat_str'].grid(column=2,row=2)
        self.v_dc['btn_add_pop'] = tk.Button(self, text='Add', command=self.add_pool)
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
        self.v_dc['btn_get_stat'] = tk.Button(self, text='Stat', command=self.get_stat)
        self.v_dc['btn_get_stat'].grid(column=1,row=5)
        self.v_dc['btn_get_size'] = tk.Button(self, text='Size', command=self.get_size)
        self.v_dc['btn_get_size'].grid(column=2,row=5)
        self.v_dc['btn_get_step'] = tk.Button(self, text='Fit', command=self.add_req)
        self.v_dc['btn_get_step'].grid(column=3,row=5)
        self.v_dc['btn_get_slice'] = tk.Button(self, text='Slice', command=self.get_slice)
        self.v_dc['btn_get_slice'].grid(column=1,row=6)
        self.v_dc['btn_get_shatter'] = tk.Button(self, text='Shatter', command=self.get_shatter)
        self.v_dc['btn_get_shatter'].grid(column=2,row=6)
        self.v_dc['btn_get_radiate'] = tk.Button(self, text='Radiate', command=self.get_radiate)
        self.v_dc['btn_get_radiate'].grid(column=3,row=6)
        self.v_dc['t_display'] = tk.Text(self, wrap="char", width=46, font=("Helvetica", 14))
        self.v_dc['t_display'].grid(column=1,row=7, columnspan=3)

        
tk_init = Tk_Main()
tk_init.mainloop()
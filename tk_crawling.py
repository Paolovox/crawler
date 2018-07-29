import Tkinter as tk
import ttk, time

def crawling(crawler):
    V = {'go':False,'url':None,'start_time':0,'prev_time':0,
         'pages':0,'errs':0,'perrs':0,'links':0,'speed':0,
         'size':0,'sizeB':0}
    L = ([None,'Pages'],[None,'Parse Errs'],[None,'Errors'],
         [None,'Links'],[None,'Speed (KB/s)'],
         [None,'Size (MB)'])
    win = tk.Tk()
    win.title('Crawler')
    win.rowconfigure(0, weight=1)
    win.columnconfigure(0, weight=1)
    frm = ttk.Frame(win)
    frm.grid(row=0, column=0, sticky='nsew')
    frm.rowconfigure(10, weight=1)
    frm.columnconfigure(1, weight=1)
    start_url = ttk.Entry(frm)
    start_url.grid(row=0, column=0, columnspan=2, sticky='ew')
    def do_btn():
        if not V['go']:
            url = start_url.get()
            if url != V['url']:
                V['pages'], V['errs'], V['perrs'] = 0, 0, 0
                V['links'], V['speed'], V['size'] = 0, 0, 0
                V['sizeB'] = 0
                V['url'] = url
                V['prev_time'] = 0
                stats()
                log_add('START CRAWLING '+V['url'])
            V['go'] = True
            V['start_time'] = time.time()
            crawler.set_url(url)
            btn.config(text='Stop')
        else:
            V['go'] = False
            V['prev_time'] += time.time() - V['start_time']
            btn.config(text='Go')
    btn = ttk.Button(frm, width=8, text='Go', command=do_btn)
    btn.grid(row=1, column=0)
    domain_var = tk.IntVar(0)
    def do_check_domain():
        crawler.config(domain=(domain_var.get() == 1))
    domain = ttk.Checkbutton(frm, text='Domain', variable=domain_var,
                             command=do_check_domain)
    domain.grid(row=2, column=0, sticky='w')
    noquery_var = tk.IntVar(0)
    def do_check_noquery():
        crawler.config(noquery=(noquery_var.get() == 1))
    noquery = ttk.Checkbutton(frm, text='No Query', variable=noquery_var,
                              command=do_check_noquery)
    noquery.grid(row=3, column=0, sticky='w')
    for e, r in zip(L, range(4, 10)):
        e[0] = ttk.Label(frm, width=15)
        e[0].grid(row=r, column=0, sticky='w')
    log = tk.Text(frm, wrap='none')
    log.grid(row=1, rowspan=10, column=1, sticky='nsew')
    def stats():
        s = (V['pages'], V['perrs'], V['errs'],
             V['links'], V['speed'], V['size'])
        for e, a in zip(L, s):
            e[0].config(text=e[1]+' '+str(a))
    def log_add(text):
        log.insert('end', text+'\n')
        log.see('end')
    def update():
        if not V['go']:
            win.after(50, update)
            return
        p = crawler.get_page()
        
        if p == None:
            log_add('END CRAWLING '+V['url'])
            btn.config(text='Go')
            V['go'] = False
        else:
            url, page, err = p
            if url:
                if page != None:
                    pre = 'LOADED'
                    V['pages'] += 1
                    V['sizeB'] += len(page)
                    if err:
                        V['perrs'] += 1
                        pre += ' '+err
                else:
                    V['errs'] += 1
                    pre = err
                log_add(pre+'  '+url)
            t = time.time() - V['start_time'] + V['prev_time']
            V['speed'] = int(round((V['sizeB']/1024.0)/t))
            V['size'] = int(round(V['sizeB']/1000000))
            V['links'] = crawler.n_links()
            stats()
        win.after(50, update)

    win.after(50, update)
    win.mainloop()

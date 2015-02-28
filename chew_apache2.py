### This is a python script for analysing the Apache2 log files
### Put your options here.  Read the comments to the right if unclear ##########
log_filename = 'other_vhosts_access.log'  # your Apache log file
cut_ip = ['123.125', '66', '220.181', '157.55'] # IP addresses to exclude
N  = 10  # maximum number of top items to display
period = '=2015-02-28' # period to look at.  Acceptable formats: 2015-02-15 ~ 2015-02-22, <2015-02-15, >2015-02-15
#period = ' ' # uncomment this line to remove restrictions on time 
show_only_page_with_words = ['html', 'pdf', 'txt'] # only show visited links that contain at least one of the words in the list
show_only_page_with_words = [] # uncomment this line to restrictions on links

### BLACK BOX. YOU CAN SAFELY IGNORE. ##########################################
def in_exclude_list(a, lst):
    
    ''' Return True if a (an ip) is in list, return False otherwise '''
    
    L = a.split('.')
    for i in range(1,5):
        s = '.'.join(L[0:i])
        if s in lst:
            return True

    return False


def convert_to_time_range(period):
    
    ''' Return a list with two items given a string period.  The first item is a 
    string start_time of format yyyy-mm-dd, and the second item is a string 
    end_time of format yyyy-mm-dd. Valid formats for period include =yyyy-mm-dd, 
    <yyyy-mm-dd, >yyyy-mm-dd, and yyyy-mm-dd ~ yyyy-mm-dd.  Note that both < and 
    > are inclusive. '''
    
    time_range = []
    if len(period) < 1:
        return ['1900-01-01', '2090-12-31']
    if period[0] == '=':
        t = period[1:]
        x = t.split('-')
        time_range.append('%4d-%2d-%2d' % (int(x[0]), int(x[1]), int(x[2])))
        time_range.append('%4d-%2d-%2d' % (int(x[0]), int(x[1]), int(x[2])))
        return time_range
    if period[0] == '>':
        t = period[1:]
        x = t.split('-')
        time_range.append('%4d-%2d-%2d' % (int(x[0]), int(x[1]), int(x[2])))
        time_range.append('2090-12-31')
        return time_range
    if period[0] == '<':
        t = period[1:]
        x = t.split('-')
        time_range.append('1900-01-01')
        time_range.append('%4d-%2d-%2d' % (int(x[0]), int(x[1]), int(x[2])))
        return time_range    
    if '~' in period:
        t = period.split('~')
        x = t[0].strip().split('-')
        y = t[1].strip().split('-')
        s1 = '%4d-%2d-%2d' % (int(x[0]), int(x[1]), int(x[2]))
        s2 = '%4d-%2d-%2d' % (int(y[0]), int(y[1]), int(y[2]))
        if s1 < s2:
            time_range.append(s1)
            time_range.append(s2)
        else:
            time_range.append(s2)
            time_range.append(s1)
        return time_range
    return ['1900-01-01', '2090-12-31']


def in_range(date, time_range):
    
    ''' Return True if string date is within two-item list time_range. Return 
    False otherwise. date has format yyyy-mm-dd '''
    
    low = time_range[0]
    high = time_range[1]
    if date <= high and date >= low:
        return True
    return False


def digit_month(month_name):
    
    ''' Return a numeric value for a string month_name.  month_name are the first
    three letters of a month, e.g., Jan for January.  If month_name is Jan, then
    the function returns 1.  If month_name is Dec, then the function returns 12. 
    If month_name is invalid, the function returns 0. '''
    
    m = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', \
         'nov', 'dec']
    return m.index(month_name.lower()) + 1

    
def fmt_date(old_date):
    
    ''' Return a string in format yyyy-mm-dd, given string old_date in a format, 
    e.g.,  15/Feb/2015:09:50:35 '''
    
    x = old_date.split('/')
    dd = x[0]
    mm = '%2d' % digit_month(x[1])
    yy = x[2]
    yy = yy[0:4]
    return '-'.join([yy, mm, dd])


def read_apached_log_file(filename, mode, cut_ips, time_range):
    
    ''' mode=0, read all visits, mode=1, read all visits that satisfy certain 
    conditions '''

    f = open(filename)
    all = []
    for line in f:
        L = line.split()
        visit_date = L[4]
        visit_date = visit_date[1:] # remove [
        if mode == 0:
            all.append([L[1], L[7]])
        elif mode == 1 and not in_exclude_list(L[1], cut_ips) \
             and in_range(fmt_date(visit_date), time_range):
            all.append([L[1], L[7]])
    return all

    
def unique_ip(L):

    ''' Return a list of unique ip sorted by visit frequency given a list L of 
    IPs '''

    def freq_first(t):
        """return tuple in reverse order"""
        return t[1], t[0]    

    d = {}
    for x in L:
        if not x[0] in d:
            d[x[0]] = 1
        else:
            d[x[0]] += 1

    top_ips = sorted(d.items(), key=freq_first, reverse=True)[:]
    lst = []
    for x in top_ips:
        lst = lst + [x]
    return lst

    
def print_ip(L):
    for x in L:
        print('%s \t %s' % (x[1], x[0]))
     
     
def hot_page(L):
    ''' return a list of unique ip sorted by visit frequency'''
    def freq_first(t):
        """return tuple in reverse order"""
        return t[1], t[0]    

    d = {}
    for x in L:
        if not x[1] in d:
            d[x[1]] = 1
        else:
            d[x[1]] += 1

    top_ips = sorted(d.items(), key=freq_first, reverse=True)[:]
    lst = []
    for x in top_ips:
        lst = lst + [x]
    return lst


def contain_word(s, L):
    ''' Return true if s contain at least one word from L, or if L is empty '''

    if len(L) == 0:
        return True
    
    for x in L:
        if x in s:
            return True
    return False


def print_page(L, filter_word_list):
    
    for x in L:
        if contain_word(x[0], filter_word_list):
            print('%s \t %s' % (x[1], x[0]))

### FUNCION DEFINTION END ###################################################### 

all_visits = read_apached_log_file(log_filename, 0, cut_ip, convert_to_time_range(''))
slim_all = read_apached_log_file(log_filename, 1, cut_ip, convert_to_time_range(period))
L = unique_ip(slim_all)
print('*** %d, %d, %d ***' % (len(all_visits), len(slim_all), len(L)))
print('(1st number=total visits, 2nd number=total included visits, 3rd number=unique included visits)')
print('Total all: ' + str(len(all_visits)))
print('Slim all (unwanted ip excluded): ' + str(len(slim_all)))
print('Slim all unique #ip: ' + str(len(L)))
print('\n** Most frequent IPs:')
print_ip(L[0:min(N, len(L))])
print('\n** Most visited pages:')
hot_lst = hot_page(slim_all)
print_page(hot_lst[0:min(N, len(hot_lst))], show_only_page_with_words)
print('\n朝气蓬勃社出品')

### 朝气蓬勃社出品 ############################################################## 

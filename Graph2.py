import datetime
import xlsxwriter

#import xlsreader

class FRay:
    def __init__(self,i0,i1,K,B):
        self.i0=i0
        self.i1=i1

def create_headers(workbook,par_year):
   
    worksheet = workbook.add_worksheet("{0}".format(par_year))

    worksheet.write(0,0, 'Num')
    worksheet.write(0,1, 'Date')
    worksheet.write(0,2, 'MinTemp')

    worksheet.write(0,3, 'RayFrom')
    worksheet.write(0,4, 'RayTo')

    worksheet.write(0,5, 'dx')
    worksheet.write(0,6, 'dy')
    worksheet.write(0,7, 'K')
    worksheet.write(0,8, 'B')
    worksheet.write(0,9, 'FLiine')
    return worksheet
    

workbook = xlsxwriter.Workbook(r'E:\Diploma\WWWW.xlsx')
worksheet = create_headers(workbook,1981)

fin=open(r'E:\Diploma\daily-min-temperatures.csv','r')
row=0
col=0
count=0
start_year = 1981

while True:
    count+=1
    row+=1
        # Get next line from file 
    line = fin.readline() 
    # if line is empty 
    # end of file is reached 
    if not line: 
        break
    print("Line{}: {}".format(count, line.strip())) 
    date1,temp=line.split(',')
    date2=date1.split('"')[1]
   # print(date2)
    print("Line{}: {}  {}".format(count, date2, temp))
    #print(date)
    date_time = datetime.datetime.strptime(date2, '%Y-%m-%d')
    print(date_time)
    cur_year = date_time.year
    #print(year)
    if cur_year != start_year:
        start_year = cur_year
        worksheet = create_headers(workbook,cur_year)
        
        row = 1
        # posible to change count (0 or count+1)
    worksheet.write(row,col,count)
    #date_format = workbook.add_format({'num_format': 'd mmmm yyyy'})
    worksheet.write(row,col+1,date2)
    worksheet.write(row,col+2,float(temp))
     
fin.close()

workbook.close()


print(row)



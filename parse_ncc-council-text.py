import csv, os
from datetime import datetime

'''todo:

1) read in a text file, parse its contents to memory

On each line
    1) Determine if it is 'ORDINANCE', 'RESOLUTION', 'AGENDA'

    2) For agendas:
    	Prepend '19' or '20' to the 4th column
	Prepend 'AGDA' to the 4th column
	Trim the last three characters of the 4th column
	Prepend '19' or '20' to the  7th column
	In the 7th column, revert the date from yy-mm-dd to mm-dd-yyyy

    3) For ordinance:
    	Prepend 'ORD' to the 4th column

    4) For resolution:
        Prepend 'RES' to the 4th column
'''

curdir = os.path.dirname(os.path.abspath(__file__))
input_text_file = '{}\\NCC_input.txt'.format(curdir)
output_text_file = '{}\\NCC_output.txt'.format(curdir)


def read_text(csvfile):
    """reads a csv/text file, returns a list of its lines"""
    content = []
    with open(csvfile, newline='') as csvf:
        reader = csv.reader(csvf)
        for row in reader:
            content.append(row)
            modify_by_type(row)
        return(content)


def modify_by_type(line):
    """reads the line's type by looking at the 7th column"""
    if line[9].find('AGENDAS') != -1:
        agenda_date = datetime.strptime(line[3], '%y-%m-%d')
        
        if agenda_date.year > 2020:
            agenda_date = agenda_date.replace(year=agenda_date.year-100)

        line[6] = '{}'.format(agenda_date.strftime('%m-%d-%Y'))
        line[3] = '{}{}{}'.format('AGDA', str(agenda_date.year)[0:2], line[3][:-3])

        
    elif line[9].find('RESOLUTION') != -1:
        line[3] = 'RES{}'.format(line[3])
        
    elif line[9].find('ORDINANCE') != -1:
        line[3] = 'ORD{}'.format(line[3])


def write_output(data, output_path):
    """writes a list of lists out to a CSV"""
    with open(output_path, 'w', newline='') as output:
        wr = csv.writer(output, delimiter=',', quoting=csv.QUOTE_ALL, dialect='excel')
        for line in data:
            wr.writerow(line)
        output.close()
        print('Wrote file out to {} successfully'.format(output_path))
        return(True)



if __name__ == "__main__":
    data = read_text(input_text_file)
    write_output(data, output_text_file)

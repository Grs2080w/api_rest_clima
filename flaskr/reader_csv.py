import csv

city_code = {}
def code(city):

    with open("C:/Users/Gabriel Santos/workspace/api_clima/flaskr/citys.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        lines = list(reader) 
    
        for i in range(0, len(lines), 2):  
            name = lines[i][0].strip()
            code = lines[i+1][0].strip()
            city_code[name] = code
    
    code_city = city_code.get(city, "Not Found!")
    return code_city





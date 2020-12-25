import pandas
import requests
import re 
from bs4 import BeautifulSoup
from datetime import date
import math

df = pandas.read_csv('planilha.csv')

url = df['Zoom Link']  #Lista com as urls dos produtos

CurrentWeb = []  #Lista com os precos atuais dos produtos

for i in df.index:
    page = requests.get(url[i])
    soup = BeautifulSoup(page.content, 'html.parser')

    price = (soup.select_one("span[data-testid*=integer]").text)
    
    price = re.sub('[R$.]', '', price)
        
    CurrentWeb.append(int(price))

    LowestLocal = df["Preco Mais Baixo"]
    CurrentLocal = df['Preco Atual']  
    
    productName = df.at[i,'Produto'] 

          

    if(LowestLocal[i]>CurrentWeb[i]):  #Altera o preco mais baixo caso o atual seja ainda mais baixo
        today = date.today()
        date_time = today.strftime("%d/%m/%Y")
        
        print(productName, "teve uma queda de preco e esta no seu preco mais baixo! Preco: R$",CurrentWeb[i])   
        
        df.at[i,'Preco Mais Baixo']=CurrentWeb[i]
        df.at[i,'Preco Atual']=CurrentWeb[i]        
        df.at[i,'Data']=date_time      
    
    if(CurrentLocal[i]>CurrentWeb[i]):      
        print(productName, "teve uma queda de preco! Preco: R$",CurrentWeb[i])        
    elif(CurrentLocal[i]<CurrentWeb[i]):              
        print(productName, "teve um aumento de preco! Preco: R$",CurrentWeb[i])   
    elif(CurrentLocal[i]==CurrentWeb[i]):     
        print(productName, "nao teve alteracao de preco.")
    else:
        print(productName, "foi adicionado!")            

    df.at[i,'Preco Atual']=CurrentWeb[i]    #Altera o preco atual       

df.to_csv('planilha.csv',index=False)                

print("OK!")




	

         

    
    







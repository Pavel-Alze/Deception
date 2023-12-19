token ='6320810642:AAHXboreX9oz3o3T59F4ftjOOyNUJ-RG4AQ'
chat_id='-1002004518874'
import urllib.request
urllib.request.urlopen('https://api.telegram.org/bot'+token+'/sendMessage?chat_id='+chat_id+'&text=Entry+detected!')

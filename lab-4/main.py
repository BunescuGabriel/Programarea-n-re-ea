import requests as req
import warnings
warnings.filterwarnings("ignore")
#warning sa nu apara prentimpinari
resp = req.get("https://localhost:44370/swagger/index.html",verify=False)

BASE_URL = "https://localhost:44370/api/"

def get_categories():
    categr= req.get(BASE_URL + "Category/categories",verify=False)
    if categr.status_code == 200:
        categories = categr.json()
        for category in categories:
            name = category.get('name')
            id= category.get("id")
            print(f'{id}:{name}')
    else:
        print("Request failed with status code:", categr.status_code)

def category_detail():
    id=input("Introduceti id-ul pentru categoria dorita: ")
    url= BASE_URL + f'Category/categories/{id}'
    cat_det=req.get(url,verify=False)
    if cat_det.status_code==200:
        cat_details=cat_det.json
        print(cat_det.text)
        
def post_category():
    category_name=''
    category_name=input("Give a name for new category: ")
    print(category_name)
    data = {"title": category_name}
    url = BASE_URL + "Category/categories"
    response = req.post(url, json=data,verify=False)
    if response.status_code == 200:
        print("Request successful!")
        print(response.json())
        get_categories()
    else:
        print("Request failed with status code:", response.status_code)
                
def category_delete():
    id = input("Introduceti id-ul pentru categoria dorita: ")
    url = BASE_URL + f'Category/categories/{id}'
    cat_dell = req.delete(url, verify=False)
    if cat_dell.status_code == 200:
        print('category deleted successfully')
    else:
        print('Failed to delete category:', cat_dell.status_code)

def category_put():
    id = input("Introduceti id-ul pentru categoria dorita: ")
    url = BASE_URL + f'Category/{id}'
    category_name=input("Give a new name for this category:")
    data = {"title": category_name}
    cat_put = req.put(url,json=data, verify=False)
    if cat_put.status_code == 200:
        print('category renamed successfully')
    else:
        print('Failed to delete category:', cat_put.status_code)

def post_products():
    id = input("Introduceti id-ul pentru categoria dorita: ")
    prod_name=input("introduceti numele noului produs:")
    pret=input("pretul:")
    data={"title":prod_name,"price":str(pret),"categoryId":id}
    categr= req.post( BASE_URL + f"Category/categories/{id}/products",json=data,verify=False)
    if categr.status_code == 200:
        print('Success')
    else:
        print("Request failed with status code:", categr.status_code)

def get_products():
    id = input("Introduceti id-ul pentru categoria dorita: ")
    categr= req.get( BASE_URL + f"Category/categories/{id}/products",verify=False)
    if categr.status_code == 200:
        categories = categr.json()
        for category in categories:
            print(category)
    else:
        print("Request failed with status code:", categr.status_code)

def rules():
    print()
    print(f'1: Get the list of categories\n'
          f'2: Create a new category \n'
          f'3: Show details about a category\n'
          f'4: Delete a category\n'
          f'5: Modify title of a category\n'
          f'6: Create a new product\n'
          f'7: Show list of products from a category\n'
          f'/actions: Show the actions\n' )


def run():
    print("###################################")
    print("#     Laborator HTTP client       #")
    print("###################################")
    while True:
        rules()
        print('Choose an action and type the number of it:')
        user_input=input()
        if user_input == '1':
            get_categories()
        elif user_input =='2':
            post_category()
        elif user_input =='3':
            category_detail()
        elif user_input =='4':
            category_delete()
        elif user_input =='5':
            category_put()
        elif user_input =='6':
            post_products()
        elif user_input =='7':
            get_products()
        if user_input =='/actions':
            continue

if __name__ == '__main__':
    run()


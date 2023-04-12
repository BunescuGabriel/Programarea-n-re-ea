import requests as req
import warnings
warnings.filterwarnings("ignore")
#warning sa nu apara prentimpinari
resp = req.get("https://localhost:44370/swagger/index.html",verify=False)

#1
def get_categories():
    categr= req.get("https://localhost:44370/api/Category/categories",verify=False)
    if categr.status_code == 200:
        categories = categr.json()
        for category in categories:
            name = category.get('name')
            id= category.get("id")
            print(f'{id}:{name}')
    else:
        print("Request failed with status code:", categr.status_code)

#3
def post_category():
    category_name=''
    category_name=input("Give a name for new category: ")
    print(category_name)
    data = {"title": category_name}
    url = "https://localhost:44370/api/Category/categories"
    response = req.post(url, json=data,verify=False)
    if response.status_code == 200:
        print("Request successful!")
        print(response.json())
        get_categories()
    else:
        print("Request failed with status code:", response.status_code)
#2
def category_detail():
    id=input("Introduceti id-ul pentru categoria dorita: ")
    url=f'https://localhost:44370/api/Category/categories/{id}'
    cat_det=req.get(url,verify=False)
    if cat_det.status_code==200:
        cat_details=cat_det.json
        print(cat_det.text)
#4
def category_delete():
    id = input("Introduceti id-ul pentru categoria dorita: ")
    url = f'https://localhost:44370/api/Category/categories/{id}'
    cat_dell = req.delete(url, verify=False)
    if cat_dell.status_code == 200:
        print('category deleted successfully')
    else:
        print('Failed to delete category:', cat_dell.status_code)

#5
def category_put():
    id = input("Introduceti id-ul pentru categoria dorita: ")
    url = f'https://localhost:44370/api/Category/{id}'
    category_name=input("Give a new name for this category:")
    data = {"title": category_name}
    cat_put = req.put(url,json=data, verify=False)
    if cat_put.status_code == 200:
        print('category renamed successfully')
    else:
        print('Failed to delete category:', cat_put.status_code)

#6
def post_products():
    id = input("Introduceti id-ul pentru categoria dorita: ")
    prod_name=input("introduceti numele noului produs:")
    pret=input("pretul:")
    data={"title":prod_name,"price":str(pret),"categoryId":id}
    categr= req.post(f"https://localhost:44370/api/Category/categories/{id}/products",json=data,verify=False)
    if categr.status_code == 200:
        print('este contact')
    else:
        print("Request failed with status code:", categr.status_code)
#https://localhost:44370/api/Category/categories/4/products

#7
def get_products():
    id = input("Introduceti id-ul pentru categoria dorita: ")
    categr= req.get(f"https://localhost:44370/api/Category/categories/{id}/products",verify=False)
    if categr.status_code == 200:
        categories = categr.json()
        for category in categories:
            print(category)
    else:
        print("Request failed with status code:", categr.status_code)

def rules():
    print(f'1: Get the list of categories\n'
          f'2: Show details about a category\n'
          f'3: Create a new category\n'
          f'4: Delete a category\n'
          f'5: Modify title of a category\n'
          f'6: Create a new product\n'
          f'7: Show list of products from a category\n'
          f'/actions: Show the actions\n' )


def run():
    print("###################################")
    print("#     Laborator HTTP client       #")
    print("###################################")
    rules()
    while True:
        print('Choose an action and type the number of it:')
        user_input=input()
        if user_input == '1':
            get_categories()
        elif user_input =='2':
            category_detail()
        elif user_input =='3':
            post_category()
        elif user_input =='4':
            category_delete()
        elif user_input =='5':
            category_put()
        elif user_input =='6':
            post_products()
        elif user_input =='7':
            get_products()
        if user_input =='/actions':
            rules()

if __name__ == '__main__':
    run()

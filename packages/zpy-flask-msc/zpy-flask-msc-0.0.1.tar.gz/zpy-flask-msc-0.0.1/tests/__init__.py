from resources.greeting_resoource import GreetingResource
from config.api_configuration import apiConfig
from zpy.api import ZResource, api



@api(base="/api", config=apiConfig)
def create_api():
    return [ZResource("/greeting", GreetingResource())]



app = create_api()

# 🚨 Only use it in local tests 💻
if __name__ == "__main__":
    app.run(host="localhost", debug=True)

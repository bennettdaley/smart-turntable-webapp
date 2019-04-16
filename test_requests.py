import requests

def main():
    album_get = requests.get('https://smart-turntable-webapp.herokuapp.com/api/albums/1')
    print(album_get.json())
    track_get = requests.get('https://smart-turntable-webapp.herokuapp.com/api/albums/1/1')
    print(track_get.json())
    track_put = requests.put('https://smart-turntable-webapp.herokuapp.com/api/albums/1/1', data={"test":test})
    print(track_put)



if __name__ == "__main__":
    main()
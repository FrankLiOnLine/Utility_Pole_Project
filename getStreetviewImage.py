import requests
import shutil
import urllib
import os
import json
from urllib import parse
from tqdm import tqdm

key = 'USE_YOUR_OWN_KEY_HERE'

def get_image_info(loc):
    data = {}
    data['size'] = '640x640'                 # max 640
    #loc = '42.4293,-71.0926048'              # 4th digit after . will change camera position
    data['location'] = loc
    data['heading'] = '-45'      # horizontal parameter -90 -> counter clockwise 90 degree
    data['pitch'] = '0'         # vertical parameter  0 front -> positive angle = camera up view
    data['fov'] = '100'          # zoom parameter
    data['key'] = key
    url_metadata = 'https://maps.googleapis.com/maps/api/streetview/metadata?' + urllib.parse.urlencode(data)
    url = 'https://maps.googleapis.com/maps/api/streetview?' + urllib.parse.urlencode(data)

    r_metadata = requests.get(url_metadata, allow_redirects=True)
    r_metadata_jason = r_metadata.json()
    return url, r_metadata_jason

def download_img(latti_list, logi_list):
    try:
        shutil.rmtree('pictures_downloaded')
    except FileNotFoundError:
        pass
    finally:
        path = os.getcwd()
        path = path + '/pictures_downloaded'
        folder = os.mkdir(path)
    camera_idx = []
    counter = 0
    pbar = tqdm(total=10000)
    for i in latti_list:
        for j in logi_list:
            loc = str(i) + ',' + str(j)
            url, meta_json = get_image_info(loc)
            if meta_json['status'] == 'OK' :
                if meta_json['pano_id'] == camera_idx:
                    pass
                else:
                    img = requests.get(url).content
                    open(path + '/' + str(counter) + '.jpg','wb').write(img)
                    outputfile_json = open(path + '/' + str(counter) + '.json', 'w')
                    json.dump(meta_json, outputfile_json)
                    camera_idx = meta_json['pano_id']
                    counter += 1
            else:
                pass
            pbar.update(1)
    pbar.close()

def location_split(loc):
    latti = float(loc.split(',')[0])
    logi = float(loc.split(',')[1])
    latti_min = latti - 0.0001*50
    logi_min = logi - 0.0001*50
    latti_list = []
    logi_list = []
    for i in range(100):
        latti_list.append(latti_min + 0.0001*i)
        logi_list.append(logi_min + 0.0001*i)
    return latti_list, logi_list


def main():
    loc = '42.4293,-71.0926048'
    latti_list, logi_list = location_split(loc)
    print('files downloading')
    download_img(latti_list, logi_list)
    print('download complete.')




if __name__ == '__main__':
    main()


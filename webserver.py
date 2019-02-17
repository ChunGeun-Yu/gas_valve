#from flask import Flask
from flask import Flask, render_template, url_for
import inotify.adapters
import os
app = Flask(__name__)

#@app.route('/')
#def index():
#    return 'Hello world'
def trigger(trigger_file_path):
    cmd_str = 'touch {}'.format(trigger_file_path)
    os.system(cmd_str)
    i = inotify.adapters.Inotify()

    file_path = '/home/ubuntu/iot/done/'
    i.add_watch(file_path)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event


        # PATH=[/tmp] FILENAME=[a.txt] EVENT_TYPES=['IN_OPEN']
        # PATH=[/tmp] FILENAME=[a.txt] EVENT_TYPES=['IN_ATTRIB']
        # PATH=[/tmp] FILENAME=[a.txt] EVENT_TYPES=['IN_CLOSE_WRITE']

        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              path, filename, type_names))
        if 'IN_OPEN' in type_names:
            return filename

@app.route('/', methods=['GET', 'POST'])
def lionel():
    photo_file = trigger('/home/ubuntu/iot/trigger/trigger.txt')
    print('photo_file: {}'.format(photo_file))
    # capture_20190216_222420.jpg
#    _, date1, date2 = photo_file.split('_')
    p = {
#            'date': date1,
#            'time': date2[:-4],
            'file': 'static/{}'.format(photo_file)
        }
    return render_template('index.html', param = p)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

import os
import subprocess

'''
python doanload3.py data/kinetics-400_test.csv download
youtube-dl -o 1.mp4 -f mp4 https://www.youtube.com/watch?v=--6bJUbfpnQ

'''

def download_job(youtube_id,
    path,
	num_attempts=5,
    url_base='https://www.youtube.com/watch?v='):    
    path = os.path.join(path,''.join([youtube_id,".mp4"]) )
    if os.path.exists(path) == True:
        print path
        return True
    #print path
    command = ['youtube-dl',
               '--quiet', '--no-warnings',
               '-f', 'mp4',
               '-o', path,
               '"%s"' % (url_base + youtube_id)]
    command = ' '.join(command)
    # print(command)
    #print command
    attempts = 0
    while True:
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            attempts += 1
            if attempts == num_attempts:
                return False#status, err.output
        else:
            break
    #os.system( ' '.join(command) )    

if __name__ == '__main__':
    path = 'G:\\Crawler\\Kinetics'
    download_job('--6bJUbfpnQ',path)
	
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
from datetime import datetime


def main():
	gauth = GoogleAuth()
	gauth.LoadCredentialsFile("mycreds.txt")

	if gauth.credentials is None:
		gauth.LocalWebserverAuth()
	elif gauth.access_token_expired:
		gauth.Refresh()
	else:
		gauth.Authorize()
	gauth.SaveCredentialsFile("mycreds.txt")

	drive = GoogleDrive(gauth)

	path = r"/home/mab/PycharmProjects/mab_szuka_mieszkania"

	today = datetime.today().strftime('%d%B%Y')

	for x in os.listdir(path + "/data"):
		f = drive.CreateFile({'title': f"{today}_{x}"})
		f.SetContentFile(os.path.join(path + "/data", x))
		f.Upload()
		f = None


if __name__ == '__main__':
	main()

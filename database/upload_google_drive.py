from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
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

	today = datetime.today().strftime('%d%B%Y')

	f = drive.CreateFile({'title': f"flats_{today}"})
	f.SetContentFile("../data/flats.db")
	f.Upload()
	f = None

	print("Uploaded")


if __name__ == '__main__':
	main()

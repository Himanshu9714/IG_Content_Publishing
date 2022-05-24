from dotenv import load_dotenv
import os
from instagrapi import Client
import logging

load_dotenv()


def login():
    cl = Client()
    try:
        cl.login(os.environ.get("USERNAME"), os.environ.get("PASSWORD"))
    except:
        raise RuntimeError("Provide Username and password or may be they are invalid")
    return cl


def upload_photo_to_story(cl):
    """

    IMAGE_PATH_TO_STORY: This is an environment variable, which is declared in the .env file.
    It must has to be specified to upload image to the story. Also, it is recommended to upload jpg or jpeg format.
    Warning: It doesn't support other image format instead of jpg.

    Method: photo_upload_to_story(path: Path, caption: str, upload_id: str, mentions: List[Usertag], locations: List[StoryLocation], links: List[StoryLink], hashtags: List[StoryHashtag], stickers: List[StorySticker], extra_data: Dict[str, str] = {})
    Warning: (Support JPG files)

    """
    try:
        cl.photo_upload_to_story(
            os.environ.get("IMAGE_PATH_TO_STORY"), caption="Jay Shree Ram!"
        )
    except:
        logging.error(
            "Please provide image path or may be you've not passed the image object!"
        )


def upload_image_post(cl):
    """

    Method: photo_upload(path: Path, caption: str, upload_id: str, usertags: List[Usertag], location: Location, extra_data: Dict = {})
    Warning: (Support JPG files)

    """
    try:
        cl.photo_upload(
            os.environ.get("IMAGE_PATH_TO_POST"),
            os.environ.get("CAPTION"),
        )
    except Exception as e:
        logging.error("May be provided path is not image type!")


def upload_video_post(cl):
    """

    Method: video_upload(path: Path, caption: str, thumbnail: Path, usertags: List[Usertag], location: Location, extra_data: Dict = {})
    Warning: (Support MP4 files)

    """
    try:
        cl.video_upload(
            os.environ.get("VIDEO_PATH_TO_POST"),
            os.environ.get("CAPTION"),
        )
    except Exception as e:
        print("Failed Inside Video post")
        logging.error("May be provided path is not video type!")


def upload_carousel_object(cl):
    """

    Method: album_upload(paths: List[Path], caption: str, usertags: List[Usertag], location: Location, extra_data: Dict = {})
    Warning: (Support JPG/MP4 files)

    """
    try:
        cl.album_upload(
            [
                os.environ.get("MEDIA_URL_1"),
                os.environ.get("MEDIA_URL_2"),
                os.environ.get("MEDIA_URL_3"),
            ],
            os.environ.get("CAPTION"),
        )
    except:
        logging.error("May be provided paths are not valid!")


def upload_igtv(cl):
    """

    Method: igtv_upload(path: Path, title: str, caption: str, thumbnail: Path, usertags: List[Usertag], location: Location, extra_data: Dict = {})
    Warning: (Support MP4 files)

    """
    try:
        cl.igtv_upload(
            os.environ.get("IGTV_PATH"),
            title="Jay Shree Ram",
            caption=os.environ.get("CAPTION"),
        )
    except Exception as e:
        logging.error("May be provided path is not valid for IGTV!")

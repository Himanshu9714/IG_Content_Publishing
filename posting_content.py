import time
from utils import getCreds, makeApiCall
from dotenv import load_dotenv
import os

load_dotenv()


def createMediaObject(params):
    """Create media object

    Args:
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v13.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
            https://graph.facebook.com/v13.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}

    Returns:
            object: data from the endpoint

    """

    url = params["endpoint_base"] + params["instagram_account_id"] + "/media"

    endpointParams = dict()
    endpointParams["caption"] = params["caption"]
    endpointParams["access_token"] = params["access_token"]

    # IMAGE Media Type
    if "IMAGE" == params["media_type"]:
        endpointParams["image_url"] = params["media_url"]
    # VIDEO Media Type
    else:
        endpointParams["media_type"] = params["media_type"]
        endpointParams["video_url"] = params["media_url"]

    return makeApiCall(url, endpointParams, "POST")


def createCarouselMediaObject(params):
    """Create media object

    Args:
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v13.0/{ig-user-id}/media?image_url={image-url}&is_carousel_item=true&access_token={access-token}

    Returns:
            object: data from the endpoint

    """
    url = params["endpoint_base"] + params["instagram_account_id"] + "/media"

    endpointParams = dict()
    endpointParams["access_token"] = params["access_token"]

    # IMAGE Media Type
    if "IMAGE" == params["media_type"]:
        objects = []
        endpointParams["image_url"] = params["media_url_1"]
        objects.append(makeApiCall(url, endpointParams, "POST"))
        endpointParams["image_url"] = params["media_url_2"]
        objects.append(makeApiCall(url, endpointParams, "POST"))

        return objects
    return None


def getMediaObjectStatus(mediaObjectId, params):
    """Check the status of a media object

    Args:
            mediaObjectId: id of the media object
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code

    Returns:
            object: data from the endpoint

    """

    url = params["endpoint_base"] + "/" + mediaObjectId

    endpointParams = dict()
    endpointParams["fields"] = "status_code"
    endpointParams["access_token"] = params["access_token"]

    return makeApiCall(url, endpointParams, "GET")  # make the api call


def publishMedia(mediaObjectId, params):
    """Publish content

    Args:
            mediaObjectId: id of the media object
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}

    Returns:
            object: data from the endpoint

    """

    url = (
        params["endpoint_base"] + params["instagram_account_id"] + "/media_publish"
    )  # endpoint url

    endpointParams = dict()
    endpointParams["creation_id"] = mediaObjectId
    endpointParams["access_token"] = params["access_token"]

    return makeApiCall(url, endpointParams, "POST")


def getContentPublishingLimit(params):
    """Get the api limit for the user

    Args:
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage

    Returns:
            object: data from the endpoint

    """

    url = (
        params["endpoint_base"]
        + params["instagram_account_id"]
        + "/content_publishing_limit"
    )

    endpointParams = dict()
    endpointParams["fields"] = "config,quota_usage"
    endpointParams["access_token"] = params["access_token"]

    return makeApiCall(url, endpointParams, "GET")


def createCarouselContainer(params, imageMediaObjectsResponse):
    """Create Container

    Args:
            mediaObjectId: id of the media object
            params: dictionary of params

    API Endpoint:
            https://graph.facebook.com/v13.0/{ig-user-id}/media?caption={caption}&media_type={CAROUSEL}&children={object_id}%2C{object_id2}...&access_token={access-token}

    Returns:
            object: data from the endpoint

    """
    url = params["endpoint_base"] + params["instagram_account_id"] + "/media"

    endpointParams = dict()
    endpointParams["caption"] = "Default"
    endpointParams["media_type"] = "CAROUSEL"
    endpointParams["children"] = ""
    endpointParams["access_token"] = params["access_token"]
    for obj in imageMediaObjectsResponse:
        if endpointParams["children"] == "":
            endpointParams["children"] += f"{obj['json_data']['id']}"
        else:
            endpointParams["children"] += f"%2C{obj['json_data']['id']}"
    url += f"?caption={endpointParams['caption']}&media_type={endpointParams['media_type']}&children={endpointParams['children']}&access_token={endpointParams['access_token']}"

    return makeApiCall(url, endpointParams, "POST")


# def publishContent():
params = getCreds()
params["media_type"] = os.environ.get("MEDIA_TYPE")
params["media_url"] = os.environ.get("MEDIA_URL")
params["caption"] = os.environ.get("CAPTION")

# create a media object through the api
imageMediaObjectResponse = createMediaObject(params)

params["media_url_1"] = os.environ.get("MEDIA_URL_1")
params["media_url_2"] = os.environ.get("MEDIA_URL_2")
imageMediaObjectsResponse = createCarouselMediaObject(params)
carouselContainerResponse = createCarouselContainer(params, imageMediaObjectsResponse)
carouselContainerId = carouselContainerResponse["json_data"]["id"]
# id of the media object that was created
imageMediaObjectId = imageMediaObjectResponse["json_data"]["id"]
imageMediaStatusCode = "IN_PROGRESS"

print(f"\n---- IMAGE MEDIA OBJECT -----\n\tID:\t {imageMediaObjectId}")

while (
    imageMediaStatusCode != "FINISHED"
):  # keep checking until the object status is finished
    imageMediaObjectStatusResponse = getMediaObjectStatus(imageMediaObjectId, params)
    imageMediaStatusCode = imageMediaObjectStatusResponse["json_data"]["status_code"]
    if carouselContainerId:
        carouselContainerStatusResponse = getMediaObjectStatus(
            carouselContainerId, params
        )
        carouselMediaStatusCode = carouselContainerStatusResponse["json_data"][
            "status_code"
        ]
        print(
            f"\n---- IMAGE MEDIA OBJECT STATUS -----\n\tStatus Code:\t{carouselMediaStatusCode}"
        )

    print(
        f"\n---- IMAGE MEDIA OBJECT STATUS -----\n\tStatus Code:\t{imageMediaStatusCode}"
    )

    # wait 5 seconds if the media object is still being processed
    time.sleep(5)

# publish the post to instagram
if carouselContainerId:
    publishCarouselResponse = publishMedia(carouselContainerId, params)
publishImageResponse = publishMedia(imageMediaObjectId, params)
# json response from ig api
print(
    f'\n---- PUBLISHED IMAGE RESPONSE -----\n\tResponse:{publishImageResponse["json_data_pretty"]}'
)
if publishCarouselResponse:
    print(
        f'\n---- PUBLISHED CAROUSEL RESPONSE -----\n\tResponse:{publishCarouselResponse["json_data_pretty"]}'
    )

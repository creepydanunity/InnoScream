from fastapi import HTTPException
import os
import random
import httpx
import logging

logger = logging.getLogger("app_fastapi.tools")

IMGFLIP_API_URL = "https://api.imgflip.com/caption_image"
IMGFLIP_TEMPLATE_IDS = ["181913649", "87743020", "112126428", "217743513", "124822590", "222403160", "131087935", 
                       "97984", "131940431", "252600902", "135256802", "438680", "322841258", "188390779", "102156234", 
                       "161865971", "247375501", "309868304", "91538330", "93895088", "79132341", "110163934", 
                       "178591752", "100777631", "61579", "180190441", "224015000", "148909805", "55311130", "124055727", 
                       "61544", "91545132", "101470", "252758727", "27813981", "1035805", "558880671", "99683372", 
                       "177682295", "370867422", "427308417", "155067746", "67452763", "166969924", "135678846", 
                       "316466202", "89370399", "84341851", "101956210", "284929871", "77045868", "221578498", 
                       "226297822", "354700819", "171305372", "533936279", "61520", "119215120", "21735", "114585149", 
                       "206151308", "234202281", "5496396", "61556", "259237855", "247113703", "187102311", "101288", 
                       "14371066", "216523697", "50421420", "123999232", "134797956", "137501417", "142009471", 
                       "342785297", "247756783", "6235864", "61532", "196652226", "175540452", "110133729", "20007896", 
                       "360597639", "309668311", "92084495", "72525473"]

IMGFLIP_USERNAME = os.getenv("IMGFLIP_API_USERNAME")
IMGFLIP_PASSWORD = os.getenv("IMGFLIP_API_PASSWORD")


async def generate_meme_url(content: str) -> str:
    """
    Generate a meme URL by sending a request to the Imgflip API using the provided content.

    Args:
        content (str): The text content to split and use for meme generation.

    Returns:
        str: URL of the generated meme image.

    Raises:
        HTTPException: If the meme generation request fails or returns an error.

    Behavior:
        - Splits the input content into two halves for the top and bottom meme text.
        - Randomly selects a meme template ID from predefined options.
        - Posts a request to the Imgflip API to generate the meme.
        - Extracts and returns the meme image URL on success.
    """
    try:
        logger.debug(f"Generating meme for user: {user[:5]}..., content: {content[:20]}...")

        async with httpx.AsyncClient() as client:
            content = content.replace(",.! ", "").strip().split()
            part_1, part_2 = content[:len(content)//2], content[len(content)//2:]
            response = await client.post(
                IMGFLIP_API_URL,
                data={
                    "template_id": random.choice(IMGFLIP_TEMPLATE_IDS),
                    "username": IMGFLIP_USERNAME,
                    "password": IMGFLIP_PASSWORD,
                    "text0": (' '.join(part_1[:6])) + "..." if len(part_1) > 6 else part_1,
                    "text1": (' '.join(part_2[:6])) + "..." if len(part_2) > 6 else part_2,
                    "max_font_size": 18,
                },
            )
            response_json = response.json()
            if not response_json.get("success"):
                error = response_json.get("error", "Unknown error")
                raise HTTPException(status_code=500, detail=f"Meme generation failed: {error}")
            return response_json["data"]["url"]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate meme: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate meme")

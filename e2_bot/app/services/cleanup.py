from e2_bot.app.use_cases import CleanSavedMedia


def cleanup_media_files():
    CleanSavedMedia.execute()

from datetime import datetime, timezone
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime, timezone


# Setup logging
logger = logging.getLogger("cleanup")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# Cleanup expired tokens function
async def cleanup_expired_tokens(session: AsyncSession):
    try:
        # Log the start of cleanup
        logger.info("Starting cleanup of expired tokens.")

        # Current time in UTC
        now = datetime.now(timezone.utc)

        # Query to delete expired access tokens
        result = await session.execute(
            text("DELETE FROM access_tokens WHERE expires_at < :now RETURNING *"),
            {"now": now},
        )

        # Fetch all deleted tokens
        deleted_tokens = result.fetchall()

        if deleted_tokens:
            # Log each deleted token's information
            for token in deleted_tokens:
                logger.info(f"Deleted token: {token}")

            # Commit the transaction
            await session.commit()
            logger.info(f"Cleanup complete. {len(deleted_tokens)} tokens deleted.")
        else:
            # Log when no tokens were found for deletion
            logger.info("No expired tokens found to delete.")

    except Exception as e:
        # Log any exceptions that occur
        logger.error(f"Error occurred during cleanup: {e}")
        # Rollback in case of error
        await session.rollback()

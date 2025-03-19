from app import create_app
import logging
import sys
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    app = create_app()

    if __name__ == '__main__':
        app.run(debug=True)
except SystemExit as e:
    # Handle normal system exits with status code
    exit_code = e.code if isinstance(e.code, int) else 1
    logger.info(f"Application is shutting down with exit code: {exit_code}")
    sys.exit(exit_code)
except SQLAlchemyError as e:
    logger.error(f"Database error: {str(e)}")
    sys.exit(1)
except KeyboardInterrupt:
    logger.info("Application interrupted by user")
    sys.exit(0)
except Exception as e:
    logger.error(f"Failed to start the application: {str(e)}")
    sys.exit(1)
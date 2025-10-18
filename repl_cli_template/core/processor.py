"""
Example processor module - demonstrates core business logic pattern.
Replace this with your actual business logic.
"""

import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def process_data(input_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example core function: process data from input file.

    This function is framework-agnostic and can be called from:
    - REPL commands
    - CLI commands
    - API endpoints
    - Web UI handlers
    - Test code

    Args:
        input_path: Path to input file
        config: Configuration dictionary

    Returns:
        Dictionary with results:
        {
            'status': 'success' | 'error',
            'rows': int,
            'output': str,
            'message': str,
            'errors': List[str] (optional)
        }

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input file is invalid format
    """
    logger.info(f"Processing file: {input_path}")

    # Validate input file exists
    input_file = Path(input_path)
    if not input_file.exists():
        error_msg = f"Input file not found: {input_path}"
        logger.error(f"{__name__}:{55} - {error_msg}")
        raise FileNotFoundError(error_msg)

    # Get output path from config or use default
    output_dir = config.get("paths", {}).get("output_dir", "data/output")
    output_path = Path(output_dir) / f"{input_file.stem}_processed{input_file.suffix}"

    try:
        # Example processing logic
        # TODO: Replace with actual business logic
        with open(input_file, "r") as f:
            lines = f.readlines()

        # Simulate processing
        processed_lines = [line.upper() for line in lines]

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write output
        with open(output_path, "w") as f:
            f.writelines(processed_lines)

        result = {
            "status": "success",
            "rows": len(processed_lines),
            "output": str(output_path),
            "message": f"Successfully processed {len(processed_lines)} rows",
        }

        logger.info(f"Processing complete: {result['rows']} rows -> {output_path}")
        return result

    except Exception as e:
        error_msg = f"Processing failed: {str(e)}"
        logger.exception(f"{__name__}:{89} - {error_msg}")
        raise ValueError(error_msg)

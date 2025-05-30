import click
from pathlib import Path
from typing import List, Optional
from cloud_splitter.tui.app import CloudSplitterApp
from cloud_splitter.config import Config
from cloud_splitter.utils.logging import setup_logging, get_logger
from cloud_splitter.exceptions import CloudSplitterError

logger = get_logger()

@click.group()
@click.option('--debug/--no-debug', default=False, help='Enable debug logging')
@click.option('--config', '-c', type=click.Path(exists=True), help='Path to config file')
def cli(debug: bool, config: Optional[str]):
    """Cloud Splitter - Audio download and stem separation tool"""
    # Set up logging
    log_level = "DEBUG" if debug else "INFO"
    setup_logging()
    logger.setLevel(log_level)
    
    if config:
        logger.info(f"Using config file: {config}")

@cli.command()
def tui():
    """Launch the TUI application"""
    try:
        logger.info("Starting TUI application")
        app = CloudSplitterApp()
        app.run()
    except Exception as e:
        logger.error(f"TUI application error: {str(e)}", exc_info=True)
        raise click.ClickException(str(e))

@cli.command()
@click.argument('urls', nargs=-1, required=True)
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--keep/--no-keep', default=True, help='Keep original files')
def process(urls: List[str], output: Optional[str], keep: bool):
    """Process URLs directly from command line"""
    try:
        logger.info(f"Processing {len(urls)} URLs")
        if output:
            output_path = Path(output)
            logger.info(f"Using custom output directory: {output_path}")
        
        # TODO: Implement direct processing
        logger.info("Direct processing not yet implemented")
        
    except CloudSplitterError as e:
        logger.error(f"Processing error: {str(e)}")
        raise click.ClickException(str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise click.ClickException(str(e))

def main():
    try:
        cli()
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    main()

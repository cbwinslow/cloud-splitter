#!/usr/bin/env python3
"""
Batch processing example for Cloud Splitter
"""
import asyncio
import sys
from pathlib import Path
from cloud_splitter.core.workflow import ProcessingWorkflow
from cloud_splitter.core.config_loader import ConfigLoader
from cloud_splitter.utils.logging import setup_logging

async def process_urls_from_file(file_path: Path) -> None:
    # Set up logging
    logger = setup_logging()
    
    # Load configuration
    config = ConfigLoader.load_config()
    
    # Enable batch processing
    config.download.batch_enabled = True
    
    # Create workflow
    workflow = ProcessingWorkflow(config)
    
    try:
        # Read URLs from file
        with open(file_path) as f:
            urls = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Processing {len(urls)} URLs from {file_path}")
        
        # Add URLs to queue
        items = await workflow.add_urls(urls)
        
        # Process queue
        results = await workflow.process_queue()
        
        # Print summary
        print("\nProcessing Summary:")
        print(f"Total URLs: {len(urls)}")
        print(f"Successful: {len(results)}")
        print(f"Failed: {len(urls) - len(results)}")
        
        # Print details for each successful result
        print("\nProcessed Files:")
        for result in results:
            print(f"\n{result['title']} by {result['artist']}")
            print(f"Output directory: {result['output_dir']}")
            print("Stems:")
            for stem_name, stem_path in result['stems'].items():
                print(f"  - {stem_name}")
        
    except Exception as e:
        logger.error(f"Batch processing failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: batch_processing.py <urls_file>")
        sys.exit(1)
    
    urls_file = Path(sys.argv[1])
    if not urls_file.exists():
        print(f"Error: File not found: {urls_file}")
        sys.exit(1)
    
    asyncio.run(process_urls_from_file(urls_file))
